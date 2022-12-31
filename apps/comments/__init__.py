# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present ByteCola
"""

from flask import Blueprint

# 房间或行程评论模块

blueprint = Blueprint(
    'comments_blueprint',
    __name__,
    url_prefix=''
)
