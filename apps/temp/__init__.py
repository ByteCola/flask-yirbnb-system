# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present ByteCola
"""

from flask import Blueprint

blueprint = Blueprint(
    'temp_blueprint',
    __name__,
    url_prefix=''
)
