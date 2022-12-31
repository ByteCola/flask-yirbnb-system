# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present ByteCola
"""

from flask import Blueprint

# 房间预定模块
blueprint = Blueprint(
    'book_blueprint',
    __name__,
    url_prefix=''
)
