# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present ByteCola
"""

from flask import Blueprint

# 网站主页面模块

blueprint = Blueprint(
    'home_blueprint',
    __name__,
    url_prefix=''
)
