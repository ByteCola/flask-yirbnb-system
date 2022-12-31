# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present ByteCola
"""
import random
import traceback
from datetime import datetime

from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.domain.AlipayTradeQueryModel import AlipayTradeQueryModel
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest
from alipay.aop.api.request.AlipayTradeQueryRequest import AlipayTradeQueryRequest
from alipay.aop.api.response.AlipayTradePagePayResponse import AlipayTradePagePayResponse
from alipay.aop.api.response.AlipayTradeQueryResponse import AlipayTradeQueryResponse
from sqlalchemy import func

from apps import db
from apps.api.alipay_demo import logger
from apps.book import blueprint
from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from apps.book.alipay_client_config import alipay_client_config
from apps.book.forms import BookForm
from apps.comments.models import Comments
from apps.rooms.dict import category_dicts
from apps.rooms.models import Rooms
from apps.trips.models import Trips


# 房源预定路由方法定义

@blueprint.route('/book', methods=["POST"])
@login_required
def book():
    """
    预定提交
    :return:
    """
    trips = Trips()
    book_form = BookForm(request.form)
    room_id = request.form['room_id']
    start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d')
    end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d')
    guest_no = request.form['guest_no']

    # 查询房源数据
    room = Rooms.query.get(room_id)

    # 检查是否可以预定
    # ...

    # 保存数据
    trips.room_id = room_id
    trips.start_date = start_date

    trips.end_date = end_date
    trips.guest_no = guest_no
    trips.order_date = datetime.today()

    trips.pay_status = 'not_pay'
    trips.users_id = current_user.id
    trips.room_title = room.title
    trips.room_title_image = room.title_photo
    trips.night = (trips.end_date - trips.start_date).days
    trips.order_total_fees = trips.night * room.price
    trips.room_price = room.price
    trips.order_no = gen_order_no()
    trips.check_person = request.form['check_person']
    trips.check_phone = request.form['check_phone']
    trips.landlord_users_id = room.users_id

    db.session.add(trips)
    db.session.commit()

    # 房间评价数量
    comments_num = Comments.query.filter(Comments.room_id == room_id).count() or 0

    # 房间评价数据

    score = db.session.query(func.avg(Comments.clean).label('s_clean'),
                             func.avg(Comments.truth).label('s_truth'),
                             func.avg(Comments.communication).label('s_communication'),
                             func.avg(Comments.location).label('s_location'),
                             func.avg(Comments.checkin).label('s_checkin'),
                             func.avg(Comments.cost).label('s_cost')).filter(
        Comments.room_id == room_id)



    for clean, truth, communication, location, checkin, cost in score:
        score_dict = {'clean': clean or 0, 'truth': truth or 0, 'communication': communication or 0,
                      'location': location or 0,
                      'checkin': checkin or 0, 'cost': cost or 0,
                      'avg_score': sum(
                          [clean or 0, truth or 0, communication or 0, location or 0, checkin or 0, cost or 0]) / 6}



    return render_template('book/bill.html', room=room, trips=trips, segment="book", score=score_dict,
                           comments_num=comments_num, category_dicts=category_dicts)


# 支付宝支付
# @blueprint.route('/book_pay/<id>', methods=["GET", "POST"])
# @login_required
# def alipay_pay():
#


@blueprint.route('/book_pay_simulation/<id>', methods=["GET", "POST"])
@login_required
def book_pay_simulation(id):
    """
    模拟支付提交
    :param id:
    :return:
    """
    trips = Trips.query.get(id)
    trips.pay_status = 'paid'
    db.session.add(trips)
    db.session.commit()

    # 跳转到出行订单页面
    return redirect(url_for('trips_blueprint.trips'))


@blueprint.route('/book_pay/<id>', methods=["GET", "POST"])
@login_required
def book_pay(id):
    """
    支付宝支付提交
    :param id:
    :return:
    """

    # 跳转到出行订单页面
    return alipay_trade_page_pay_html(id)


# 出行预定订单支付完成后 回跳的页面 return_url
@blueprint.route('/book_pay_return/<id>', methods=["GET", "POST"])
@login_required
def book_pay_return(id):
    """
    订单支付回跳页面 实现订单状态查询，更新出行订单数据的支付状态
    :return:
    """

    trips = Trips.query.get(id)

    # 实例化客户端
    client = DefaultAlipayClient(alipay_client_config, logger)

    model = AlipayTradeQueryModel()
    model.out_trade_no = trips.order_no
    request = AlipayTradeQueryRequest(biz_model=model)

    # 执行API调用
    response_content = False
    try:
        response_content = client.execute(request)
    except Exception as e:
        print(traceback.format_exc())
    if not response_content:
        print("failed execute")
    else:
        order_status = False
        # 解析响应结果
        response = AlipayTradeQueryResponse()
        response.parse_response_content(response_content)
        # 响应成功的业务处理
        if response.is_success():
            # 如果业务成功，可以通过response属性获取需要的值
            order_status = True
            print("get response trade_no:" + response.trade_no)

        # 响应失败的业务处理
        else:
            # 如果业务失败，可以从错误码中可以得知错误情况，具体错误码信息可以查看接口文档
            print(response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)

        # 更新出行订单状态
        trips.pay_way = 'alipay'
        if order_status:
            trips.pay_status = 'paid'
        else:
            trips.pay_status = 'failed'
        db.session.add(trips)
        db.session.commit()

    return redirect(url_for('trips_blueprint.trips'))


def alipay_trade_page_pay_html(trip_id):
    trips = Trips.query.get(trip_id)
    # 实例化客户端
    client = DefaultAlipayClient(alipay_client_config, logger)

    # 测试统一收单下单并支付页面接口
    model = AlipayTradePagePayModel()
    model.out_trade_no = trips.order_no
    model.total_amount = trips.order_total_fees
    model.subject = trips.room_title
    model.product_code = "FAST_INSTANT_TRADE_PAY"

    request = AlipayTradePagePayRequest(biz_model=model)

    # request.return_url = "http://localhost:5000/trips"
    request.return_url = "http://localhost:5000/" + url_for('book_blueprint.book_pay_return', id=trips.id)
    request.notify_url = ""

    # 执行支付宝API调用
    response_content = False
    try:
        response_content = client.page_execute(request)
    except Exception as e:
        print(traceback.format_exc())
    if not response_content:
        print("failed execute")
    else:
        # 返回html页面
        return response_content


# 订单号生成方法  生成规则：时间+随机数
def gen_order_no():
    return datetime.now().strftime('%Y%m%d%H%M%S') + str(random.randint(100, 999))
