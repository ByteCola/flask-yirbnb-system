# -*- encoding: utf-8 -*-
"""
注册与登录等认证模块
Copyright (c) 2022 - present ByteCola
"""

from flask import Blueprint

blueprint = Blueprint(
    'authentication_blueprint',
    __name__,
    url_prefix=''
)
