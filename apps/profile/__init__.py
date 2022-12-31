# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present ByteCola
"""

from flask import Blueprint

# 用户个人信息模块

blueprint = Blueprint(
    'profile_blueprint',
    __name__,
    url_prefix=''
)
