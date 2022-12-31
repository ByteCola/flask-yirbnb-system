# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present ByteCola
"""

import os

from datetime import datetime

from flask import render_template, redirect, request, url_for
from flask_login import login_required, current_user

from apps import db
from apps.temp import blueprint
from apps.temp.models import Temp

from apps.config import Config


@blueprint.route('/temp/photo/<filename>', methods=['GET', 'POST'])
@login_required
def profile_photo(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)
