# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present ByteCola
"""

from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField

from wtforms.validators import DataRequired


# 房间预定FlaskForm定义

class BookForm(FlaskForm):
    # 房源编号
    room_id = IntegerField('Room id', id='room_id', validators=[DataRequired()])
    # 预定入住日期
    start_date = StringField('Book start_date', id='start_date', validators=[DataRequired()])
    # 预定退房日期
    end_date = StringField('Book end_date', id='end_date', validators=[DataRequired()])
    # 预定入住人数
    guest_no = IntegerField('Book guest_no', id='guest_no', validators=[DataRequired()])
