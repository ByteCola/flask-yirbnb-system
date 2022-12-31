# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present ByteCola
"""

from apps.home import blueprint
from flask import render_template, request, session, redirect, url_for
from jinja2 import TemplateNotFound

from apps.rooms.models import Rooms
from apps.rooms.util import set_pagination

# 网站主页面路由定义与实现


@blueprint.route('/')
def route_default():
    """
    网站访问默认跳转至index首页
    :return:
    """
    return redirect(url_for('home_blueprint.index'))


@blueprint.route('/index')
def index():
    """
    网站首页实现
    :return:
    """
    if "ITEMS_PER_PAGE" not in session:
        session["ITEMS_PER_PAGE"] = 10

    ITEMS_PER_PAGE = session["ITEMS_PER_PAGE"]
    page = request.args.get('page', 1, type=int)

    total_items = Rooms.query.count()
    paginated_data = Rooms.query.filter().order_by(
        Rooms.title.desc()).paginate(page, ITEMS_PER_PAGE, False)

    pagination = set_pagination(page, ITEMS_PER_PAGE, total_items, paginated_data)

    return render_template('home/index.html',
                           room_list=paginated_data.items,
                           pagination=pagination,
                           segment="index")


@blueprint.route('/<template>')
def route_template(template):
    """
    其他静态页面实现
    :param template:
    :return:
    """
    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):
    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
