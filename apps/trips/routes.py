# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present ByteCola
"""
import traceback
import datetime

from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradeRefundModel import AlipayTradeRefundModel
from alipay.aop.api.request.AlipayTradeRefundRequest import AlipayTradeRefundRequest
from alipay.aop.api.response.AlipayTradeRefundResponse import AlipayTradeRefundResponse
from sqlalchemy import or_, desc

from apps import db
from apps.api.alipay_demo import logger
from apps.book.alipay_client_config import alipay_client_config
from apps.rooms.util import set_pagination
from apps.trips import blueprint
from flask import render_template, request, session, jsonify
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound

from apps.trips.models import Trips


# 行程模块路由定义与实现

# 我的出行订单
@blueprint.route('/trips')
@login_required
def trips():
    """
    我的行程
    :return:
    """
    if "ITEMS_PER_PAGE" not in session:
        session["ITEMS_PER_PAGE"] = 10

    search = request.args.get("search")
    if search:
        ITEMS_PER_PAGE = session["ITEMS_PER_PAGE"]
        page = request.args.get('page', 1, type=int)

        total_items = Trips.query.count()
        paginated_data = Trips.query.filter_by(users_id=current_user.id).order_by(Trips.order_date.desc()).paginate(
            page, ITEMS_PER_PAGE, False)
    else:
        ITEMS_PER_PAGE = session["ITEMS_PER_PAGE"]
        page = request.args.get('page', 1, type=int)

        total_items = Trips.query.count()
        paginated_data = Trips.query.filter_by(users_id=current_user.id).order_by(Trips.order_date.desc()).paginate(
            page, ITEMS_PER_PAGE, False)

    pagination = set_pagination(page, ITEMS_PER_PAGE, total_items, paginated_data)

    return render_template('trips/my-trips.html',
                           data_list=paginated_data.items,
                           pagination=pagination,
                           segment="trips")


# 房东查看预定订单
@blueprint.route('/landlord_trips')
@login_required
def landlord_trips():
    """
    房东订单
    :return:
    """
    if "ITEMS_PER_PAGE" not in session:
        session["ITEMS_PER_PAGE"] = 10

    search = request.args.get("search")
    if search:
        ITEMS_PER_PAGE = session["ITEMS_PER_PAGE"]
        page = request.args.get('page', 1, type=int)

        total_items = Trips.query.count()
        paginated_data = Trips.query.filter_by(landlord_users_id=current_user.id).order_by(Trips.order_date.desc()).paginate(
            page, ITEMS_PER_PAGE, False)
    else:
        ITEMS_PER_PAGE = session["ITEMS_PER_PAGE"]
        page = request.args.get('page', 1, type=int)

        total_items = Trips.query.count()
        paginated_data = Trips.query.filter_by(landlord_users_id=current_user.id).order_by(Trips.order_date.desc()).paginate(
            page, ITEMS_PER_PAGE, False)

    pagination = set_pagination(page, ITEMS_PER_PAGE, total_items, paginated_data)

    return render_template('trips/landlord-trips.html',
                           data_list=paginated_data.items,
                           pagination=pagination,
                           segment="trips")



# 房东查看订单详情
@blueprint.route('/trip_detail/<id>', methods=["GET", "POST"])
@login_required
def trip_detail(id):
    """
    房东订单
    :return:
    """
    trip = Trips.query.get(id)

    return render_template('trips/trip-detail.html',
                           trip=trip,
                           segment="trips")


# 房东对预定支付的订单进行退款
@blueprint.route('/trip_refund/<id>', methods=["GET","POST"])
@login_required
def trip_refund(id):
    """
    房东对预订支付的订单进行退款
    :return:
    """
    trips = Trips.query.get(id)

    # 调用支付宝退款接口进行退款

    # 实例化客户端
    client = DefaultAlipayClient(alipay_client_config, logger)

    model = AlipayTradeRefundModel()
    model.out_trade_no = trips.order_no
    model.refund_amount = trips.order_total_fees
    model.refund_reason = "房东退款"

    request = AlipayTradeRefundRequest(biz_model=model)
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
        response = AlipayTradeRefundResponse()
        response.parse_response_content(response_content)
        # 响应成功的业务处理
        if response.is_success():
            # 如果业务成功，可以通过response属性获取需要的值
            order_status = True
            print("get response trade_no:" + response.trade_no)
            print("调用支付宝退款成功")

            # 修改支付状态
            trips.pay_status = 'refund'
            db.session.add(trips)
            db.session.commit()
            res = {'valid': 'success', 'message': '退款成功', 'redirect_url': None}
            return jsonify(res)

        # 响应失败的业务处理
        else:
            # 如果业务失败，可以从错误码中可以得知错误情况，具体错误码信息可以查看接口文档
            print(response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)

    res = {'valid': 'failed', 'message': '退款失败', 'redirect_url': None}
    return jsonify(res)

# 房间预定统计
@blueprint.route('/room_trips/<room_id>', methods=["GET", "POST"])
@login_required
def room_trips(room_id):

    # 查询已当前房间已成功预定的日期列表
    booked_dates = []
    trips = Trips.query.filter(Trips.room_id == room_id, Trips.pay_status == 'paid').all()
    for trip in trips:
        print(trip.start_date)
        sd = trip.start_date
        ed = trip.end_date
        delta = ed - sd
        for i in range(0, delta.days + 1):
            booked_dates.append(sd + datetime.timedelta(days=i))

    return render_template('trips/statistics.html',
                           booked_dates=booked_dates,
                           segment="trips")