# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present ByteCola
"""

from flask import Blueprint

# 行程模块

blueprint = Blueprint(
    'trips_blueprint',
    __name__,
    url_prefix=''
)
