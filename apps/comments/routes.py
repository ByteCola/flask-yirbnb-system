# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present ByteCola
"""
from datetime import datetime

from sqlalchemy import or_, desc

from apps import db
from apps.comments.forms import CommentForm
from apps.comments.models import Comments
from apps.rooms.models import Rooms
from apps.rooms.util import set_pagination
from apps.comments import blueprint
from flask import render_template, request, session
from flask_login import login_required, current_user

# 评价模块路由方法定义与实现
from apps.trips.models import Trips


@blueprint.route('/my_comments.html', methods=['GET', 'POST'])
@login_required
def my_comments():
    """
    我的评价
    :return:
    """
    if "ITEMS_PER_PAGE" not in session:
        session["ITEMS_PER_PAGE"] = 10

    ITEMS_PER_PAGE = session["ITEMS_PER_PAGE"]
    page = request.args.get('page', 1, type=int)

    total_items = Comments.query.filter(Comments.users_id == current_user.id).order_by(
        Comments.comment_date.desc()).count()
    paginated_data = Comments.query.filter(Comments.users_id == current_user.id).order_by(
        Comments.comment_date.desc()).paginate(
        page, ITEMS_PER_PAGE, False)

    pagination = set_pagination(page, ITEMS_PER_PAGE, total_items, paginated_data)

    return render_template('comments/my_comments.html',
                           comment_list=paginated_data.items,
                           pagination=pagination,
                           segment="comments")


@blueprint.route('/comments/add', methods=['GET', 'POST'])
@login_required
def add_comment():
    """
    发布评价
    :return:
    """
    trip_id = request.args.get("trip_id")
    trips = Trips.query.get(trip_id)
    room_id = trips.room_id
    rooms = Rooms.query.get(room_id)
    comment_exists = Comments.query.filter_by(users_id=current_user.id, trip_id=trip_id).first()

    if not comment_exists:

        comment_form = CommentForm()
        comment = Comments()

        if 'comment' in request.form:
            # check if file added and upload

            comment_form.populate_obj(comment)

            comment.users_id = current_user.id
            # convert date str into python datetime object
            comment.comment_date = datetime.now()
            comment.room_id = rooms.id
            comment.trip_id = trip_id

            comment.landlord_id = rooms.users_id
            db.session.add(comment)
            db.session.commit()

            return render_template('comments/add_comment.html',
                                   form=comment_form,
                                   rooms=rooms,
                                   trips=trips,
                                   msg='评价成功',
                                   segment='comments')

        return render_template('comments/add_comment.html', form=comment_form, rooms=rooms, trips=trips,
                               segment='comments')

    if comment_exists:

        comment_form = CommentForm(obj=comment_exists)

        if 'comment' in request.form:
            comment_form.populate_obj(comment_exists)
            comment_exists.comment_date = datetime.now()
            comment_exists.room_id = rooms.id
            comment_exists.landlord_id = rooms.users_id
            comment_exists.trip_id = trip_id
            db.session.add(comment_exists)
            db.session.commit()

            return render_template('comments/add_comment.html',
                                   form=comment_form,
                                   rooms=rooms,
                                   trips=trips,
                                   msg='评价提交成功',
                                   segment='comment')

        return render_template('comments/add_comment.html', form=comment_form, rooms=rooms, trips=trips,
                               segment='comments')
