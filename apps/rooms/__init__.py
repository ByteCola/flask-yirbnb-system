# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present ByteCola
"""

from flask import Blueprint

# 房源（房间）模块

blueprint = Blueprint(
    'rooms_blueprint',
    __name__,
    url_prefix=''
)
