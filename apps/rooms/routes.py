# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present ByteCola
"""
import os
import uuid
import datetime

from flask import render_template, request, jsonify, url_for, redirect, session, current_app
from flask_login import login_required, current_user
from sqlalchemy import or_, desc, func

from apps import db
from apps.book.forms import BookForm
from apps.comments.models import Comments
from apps.config import Config
from apps.facility.dict import facility_dicts
from apps.facility.models import Facility
from apps.like.models import Like
from apps.profile.forms import LandlordForm
from apps.profile.models import Landlord
from apps.profile.util import allowed_image_file

from apps.rooms import blueprint
from apps.rooms.forms import RoomForm
from apps.rooms.models import Rooms
from apps.datatables.util import set_pagination
from apps.rooms.dict import category_dicts, bed_dicts

# 房源（房间）路由方法定义与实现
from apps.trips.models import Trips


@blueprint.route('/photo/<filename>', methods=['GET', 'POST'])
def rooms_photo(filename):
    """
    房间照片读取
    :param filename:
    :return:
    """
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


@blueprint.route('/searchs', methods=['GET', 'POST'])
def searchs():
    """
    房间搜索
    :return:
    """
    if "ITEMS_PER_PAGE" not in session:
        session["ITEMS_PER_PAGE"] = 10

    keywords = request.args.get("keywords")
    filter = []
    query = Rooms.query.filter()
    if keywords:
        # Rooms.query.filter()
        query = query.filter(or_(Rooms.title.like('%'+keywords+'%'), Rooms.category.like('%'+keywords+'%'), Rooms.city.like('%'+keywords+'%')))
        # filter.append(or_(Rooms.title.like(search), Rooms.category.like(search),Rooms.city.like(search)))

        # paginated_data = Rooms.query.filter(or_(Rooms.title.like(search), Rooms.category.like(search)),
        #                                     Rooms.city.like(search)).paginate(page,
        #                                                                       ITEMS_PER_PAGE,
        #                                                                       False)

    categorys = request.args.getlist('category')

    if 'all' not in categorys:
        print(categorys)
        if categorys:
            query = query.filter(Rooms.category.in_(categorys))
            # filter.append(Rooms.category == category)

    bednums = request.args.getlist('bednum')

    if 'all' not in bednums:
        print(bednums)
        if bednums:
            query = query.filter(Rooms.bed.in_(bednums))
            # filter.append(Rooms.category == category)

    min_price = request.args.get("min_price")
    if min_price:
        query = query.filter(Rooms.price >= min_price)
        # filter.append(Rooms.price >= min_price)

    max_price = request.args.get("max_price")
    if max_price:
        query = query.filter(Rooms.price <= max_price)
        # filter.append(Rooms.price <= max_price)

    ITEMS_PER_PAGE = session["ITEMS_PER_PAGE"]
    page = request.args.get('page', 1, type=int)

    # 仅显示正常入住的房源
    query.filter(Rooms.status == '1')

    total_items = query.count()

    # filter_2 = [or_(Rooms.title.like(search), Rooms.category.like(search),Rooms.city.like(search)),Rooms.price <= 1000]
    paginated_data = query.paginate(page, ITEMS_PER_PAGE, False)

    pagination = set_pagination(page, ITEMS_PER_PAGE, total_items, paginated_data)

    return render_template('rooms/searchs.html',
                           room_list=paginated_data.items,
                           pagination=pagination,
                           keywords=keywords,
                           categorys=categorys,
                           bednums = bednums,
                           min_price=min_price,
                           max_price=max_price,
                           category_dicts=category_dicts,
                           bed_dicts = bed_dicts,
                           segment="rooms")


@blueprint.route('/my_rooms.html', methods=['GET', 'POST'])
@login_required
def my_rooms():
    """
    我的房源
    :return:
    """

    # 判断是否进行房东信息认证 如无 跳转至房东认证页面
    landlord_exists = Landlord.query.filter_by(users_id=current_user.id).first()
    if not landlord_exists:
        landlord_form = LandlordForm()
        user_landlord = Landlord()
        return render_template('profile/landlord.html', form=landlord_form, landlord=user_landlord, segment='landlord')

    if "ITEMS_PER_PAGE" not in session:
        session["ITEMS_PER_PAGE"] = 10

    search = request.args.get("keywords")
    if search:
        ITEMS_PER_PAGE = session["ITEMS_PER_PAGE"]
        page = request.args.get('page', 1, type=int)

        total_items = Rooms.query.filter(Rooms.users_id == current_user.id, Rooms.status != '3',
                                         or_(Rooms.title.like('%' + search + '%'),
                                             Rooms.category.like('%' + search + '%')),
                                         ).count()
        paginated_data = Rooms.query.filter(Rooms.users_id == current_user.id, Rooms.status != '3',
                                            or_(Rooms.title.like('%' + search + '%'),
                                                Rooms.category.like('%' + search + '%'))).order_by(
            Rooms.title.desc()).paginate(page,
                                         ITEMS_PER_PAGE,
                                         False)
    else:
        ITEMS_PER_PAGE = session["ITEMS_PER_PAGE"]
        page = request.args.get('page', 1, type=int)

        total_items = Rooms.query.filter(Rooms.users_id == current_user.id, Rooms.status != '3').count()
        paginated_data = Rooms.query.filter(Rooms.users_id == current_user.id, Rooms.status != '3').order_by(
            Rooms.title.desc()).paginate(
            page, ITEMS_PER_PAGE, False)

    if not search:
        search = ''
    pagination = set_pagination(page, ITEMS_PER_PAGE, total_items, paginated_data)

    return render_template('rooms/my-items.html',
                           room_list=paginated_data.items,
                           pagination=pagination,
                           keywords=search,
                           segment="rooms")


@blueprint.route('/rooms/add', methods=["GET", "POST"])
@login_required
def rooms_add():
    """
    房东发布房源
    :return:
    """

    rooms = Rooms()
    form = RoomForm(obj=rooms)

    if form.is_submitted():

        # check if file added and upload
        file = request.files['title_photo']
        if file and allowed_image_file(file.filename):
            # create a secure filename and save file in Uploads folder
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = str(uuid.uuid4()) + "." + ext
            file.save(os.path.join(Config.basedir + Config.UPLOAD_FOLDER, filename))

        # 检测房间图集是否上传
        # room_photos = ''
        # for fp in request.files.getlist('photos'):
        #     # 检查文件类型
        #     if fp and allowed_image_file(fp.filename):
        #         ext = fp.filename.rsplit('.', 1)[1].lower()
        #         filename = str(uuid.uuid4()) + "." + ext
        #         fp.save(os.path.join(Config.basedir + Config.UPLOAD_FOLDER, filename))
        #         room_photos += filename + ','

        form.populate_obj(rooms)
        # add saved filename into user profile column
        if file and allowed_image_file(file.filename):
            rooms.title_photo = filename
        else:
            rooms.title_photo = ""

        # 保存房间图集
        # rooms.photos = room_photos
        rooms.create_date = datetime.datetime.now()
        rooms.users_id = current_user.id

        db.session.add(rooms)
        db.session.commit()

        return redirect(url_for('rooms_blueprint.my_rooms'))
    return render_template('rooms/add-item.html', form=form, data=rooms, segment="rooms")


@blueprint.route('/edit/<id>', methods=["GET", "POST"])
@login_required
def edit(id):
    """
    编辑房源信息
    :param id:
    :return:
    """
    rooms = Rooms.query.get(id)
    form = RoomForm(obj=rooms)

    if form.is_submitted():
        old_title_photo = rooms.title_photo
        # check if file added and upload
        file = request.files['title_photo']
        if file and allowed_image_file(file.filename):
            # create a secure filename and save file in Uploads folder
            ext = file.filename.rsplit('.', 1)[1].lower()
            filename = str(uuid.uuid4()) + "." + ext
            file.save(os.path.join(Config.basedir + Config.UPLOAD_FOLDER, filename))

        # 检测房间图集是否上传
        # room_photos = ''
        # for fp in request.files.getlist('photos'):
        #     # 检查文件类型
        #     if fp and allowed_image_file(fp.filename):
        #         ext = fp.filename.rsplit('.', 1)[1].lower()
        #         filename = str(uuid.uuid4()) + "." + ext
        #         fp.save(os.path.join(Config.basedir + Config.UPLOAD_FOLDER, filename))
        #         room_photos += filename + ','

        form.populate_obj(rooms)

        # add saved filename into user profile column
        if file and allowed_image_file(file.filename):
            rooms.title_photo = filename
        else:
            rooms.title_photo = old_title_photo

        # 保存房间图集

        # rooms.photos = room_photos

        # clean old facility and save new rooms facility

        Facility.query.filter(Facility.room_id == rooms.id).delete()

        facilities_code = request.form.getlist('facilities')
        facilities = []
        for code in facilities_code:
            print(code)
            f = Facility(facility_code=code, room_id=rooms.id, room=rooms)
            facilities.append(f)

        db.session.add_all(facilities)
        db.session.commit()

        return redirect(url_for('rooms_blueprint.my_rooms'))
    return render_template('rooms/edit-item.html', form=form, data=rooms, facility_dicts=facility_dicts,
                           segment="rooms")


@blueprint.route('/room/<id>')
def room_detail(id):
    """
    房间详情页面 展示房源评分及评价信息
    :param id:
    :return:
    """
    room = Rooms.query.get(id)

    if not room:
        return render_template('rooms/room-not-found.html')
    if room.status == '3':
        # 房源状态为3时 代表删除状态
        return render_template('rooms/room-not-found.html')

    book_form = BookForm()
    book_form.room_id = id
    # 房间评价数据
    # sums = Comments.query(func.sum(Comments.clean).label('a1')).subquery()
    # sums = db.session.query(
    #     func.sum(Comments.clean).label('clean')
    #                         , func.sum(Comments.truth).label('truth')
    #                         , func.sum(Comments.communication).label('communication')
    #                         , func.sum(Comments.location).label('location')
    #                         , func.sum(Comments.checkin).label('checkin')
    #                         , func.sum(Comments.cost).label('cost')).filter(
    #     Comments.room_id == id).subquery()
    # score = db.session.query(func.avg(sums.c.clean).label('s_clean'),
    #                          func.avg(sums.c.truth).label('s_truth'),
    #                          func.avg(sums.c.communication).label('s_communication'),
    #                          func.avg(sums.c.location).label('s_location'),
    #                          func.avg(sums.c.checkin).label('s_checkin'),
    #                          func.avg(sums.c.cost).label('s_cost')).all()

    score = db.session.query(func.avg(Comments.clean).label('s_clean'),
                             func.avg(Comments.truth).label('s_truth'),
                             func.avg(Comments.communication).label('s_communication'),
                             func.avg(Comments.location).label('s_location'),
                             func.avg(Comments.checkin).label('s_checkin'),
                             func.avg(Comments.cost).label('s_cost')).filter(
        Comments.room_id == id)

    for clean, truth, communication, location, checkin, cost in score:
        score_dict = {'clean': clean or 0, 'truth': truth or 0, 'communication': communication or 0,
                      'location': location or 0,
                      'checkin': checkin or 0, 'cost': cost or 0,
                      'avg_score': sum(
                          [clean or 0, truth or 0, communication or 0, location or 0, checkin or 0, cost or 0]) / 6}

    # 房间评价数量
    comments_num = Comments.query.filter(Comments.room_id == id).count() or 0
    # 房东评价数量
    landlord_comments_num = Comments.query.filter(Comments.landlord_id == room.users_id).count() or 0
    # 房间评论内容 取前五条数据
    comments = Comments.query.filter(Comments.room_id == id).order_by(desc(Comments.comment_date)).limit(5)

    # 查询已当前房间已成功预定的日期列表
    booked_dates = []
    trips = Trips.query.filter(Trips.room_id == id, Trips.pay_status == 'paid').all()
    for trip in trips:
        print(trip.start_date)
        sd = trip.start_date
        ed = trip.end_date
        delta = ed - sd
        for i in range(0, delta.days + 1):
            booked_dates.append(sd + datetime.timedelta(days=i))

    # 是否喜欢

    is_like = '0'
    print(current_user)
    if hasattr(current_user,id) :
        like = Like.query.filter(Like.room_id == id, Like.users_id == current_user.id).first()
        if like:
            is_like = '1'

    # 自增房源的浏览量
    Rooms.query.filter(Rooms.id == room.id).update({'views': (room.views + 1)})
    db.session.commit()

    return render_template('rooms/room.html', form=book_form, data=room, score=score_dict, comments_num=comments_num,
                           landlord_comments_num=landlord_comments_num,
                           comments=comments, booked_dates=booked_dates, facility_dicts=facility_dicts,like=is_like)


# 暂定入住、开启入住方法
@blueprint.route('/status_update/<id>', methods=["GET"])
@login_required
def status_update(id):
    """
    暂停、开启房源入住
    :param id:
    :return:
    """
    data = Rooms.query.get(id)

    status = False

    if data.status == '1':
        status = '2'
    else:
        status = '1'

    Rooms.query.filter(Rooms.id == id).update({'status': status})

    db.session.commit()

    return redirect(url_for('rooms_blueprint.my_rooms'))


# 房源删除 伪删除 数据仍存储在数据库中
@blueprint.route('/room_delete/<id>', methods=["DELETE"])
@login_required
def delete(id):
    """
    删除房源
    :param id:
    :return:
    """
    Rooms.query.filter(Rooms.id == id).update({'status': '3'})
    db.session.commit()

    response = {'valid': 'success', 'message': 'Item deleted successfully', 'redirect_url': None}
    return jsonify(response)


# 房源删除 伪删除 数据仍存储在数据库中
@blueprint.route('/like/<id>', methods=["POST"])
@login_required
def like(id):
    """
    点赞（喜欢）、取消点赞房间
    :param id:
    :return:
    """

    is_like = '0'
    like = Like.query.filter(Like.room_id == id, Like.users_id == current_user.id).first()
    if like:
        Like.query.filter(Like.room_id == id, Like.users_id == current_user.id).delete()

    else:
        like = Like()
        like.room_id = id
        like.users_id = current_user.id
        db.session.add(like)
        is_like = '1'

    db.session.commit()

    response = {'valid': 'success', 'message': 'update successfully', 'redirect_url': None, 'like': is_like}
    return jsonify(response)
