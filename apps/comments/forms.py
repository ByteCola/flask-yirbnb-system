# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present ByteCola
"""

from flask_wtf import FlaskForm
from wtforms import IntegerField, TextAreaField, SelectField
from wtforms.validators import Email, DataRequired


# 评价FlaskForm表单定义

class CommentForm(FlaskForm):
    # 干净卫生评分
    clean = SelectField('clean score', id='clean', validators=[DataRequired()],
                        choices=[5, 4, 3, 2, 1])
    # 如实描述评分
    truth = SelectField('truth score', id='truth', validators=[DataRequired()],
                        choices=[5, 4, 3, 2, 1])
    # 沟通顺畅评分
    communication = SelectField('communication score', id='communication', validators=[DataRequired()],
                                choices=[5, 4, 3, 2, 1])
    # 位置便利评分
    location = SelectField('location score', id='location', validators=[DataRequired()],
                           choices=[5, 4, 3, 2, 1])
    # 入住便捷评分
    checkin = SelectField('checkin score', id='checkin', validators=[DataRequired()],
                          choices=[5, 4, 3, 2, 1])
    # 高性价比评分
    cost = SelectField('cost score', id='cost', validators=[DataRequired()],
                       choices=[5, 4, 3, 2, 1])
    # 评价内容
    content = TextAreaField('content', id='content', validators=[DataRequired()])
