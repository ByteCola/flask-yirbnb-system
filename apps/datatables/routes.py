# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present ByteCola
"""

from flask import render_template, request, jsonify, url_for, redirect, session
from sqlalchemy import or_

from apps import db

from apps.datatables import blueprint
from apps.home.models import Data
from apps.datatables.util import set_pagination
from apps.datatables.forms import DatatableForm


@blueprint.route('/transactions.html')
def transactions():

    if "ITEMS_PER_PAGE" not in session:
        session["ITEMS_PER_PAGE"] = 10

    search = request.args.get("search")
    if search:
        ITEMS_PER_PAGE = session["ITEMS_PER_PAGE"]
        page = request.args.get('page', 1, type=int)

        total_items = Data.query.count()
        paginated_data = Data.query.filter(or_(Data.name.like(search), Data.value.like(search))).paginate(page, ITEMS_PER_PAGE, False)
    else:
        ITEMS_PER_PAGE = session["ITEMS_PER_PAGE"]
        page = request.args.get('page', 1, type=int)

        total_items = Data.query.count()
        paginated_data = Data.query.paginate(page, ITEMS_PER_PAGE, False)

    pagination = set_pagination(page, ITEMS_PER_PAGE, total_items, paginated_data)

    return render_template('datatables/list.html',
                           data_list=paginated_data.items,
                           pagination=pagination,
                           segment="datatables")
