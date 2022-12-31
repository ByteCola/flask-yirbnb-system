# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present ByteCola
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FileField
from wtforms.validators import Email, DataRequired


# 用户个人信息FlaskForm表单定义

class ProfileForm(FlaskForm):

    # 姓名
    fullname = StringField('Full Name', id='full_name', validators=[DataRequired()])
    # 出生日期
    birthday = StringField('Birthday', id='birthday', validators=[DataRequired()])
    # 性别
    gender = SelectField('Gender', id='gender', choices=[("1", "男"), ("2", "女")])
    # 邮箱
    email = StringField('Email', id='email', validators=[DataRequired(), Email()])
    # 手机
    phone = StringField('Phone', id='phone', validators=[DataRequired()])
    # 居住地址
    address = StringField('Address', id='address', validators=[DataRequired()])
    #number = StringField('Number', id='number', validators=[DataRequired()])
    # 城市
    city = StringField('City', id='city', validators=[DataRequired()])
    #state = StringField('State', id='state', validators=[DataRequired()])
    # 国家
    country = StringField('Country', id='country', validators=[DataRequired()])
    # 邮编
    zipcode = StringField('Zip Code', id='zipcode', validators=[DataRequired()])
    # 头像
    photo = FileField('Profile Photo', id='photo')


# 收付款账号设置
class BillingForm(FlaskForm):
    account = StringField('Account', id='account', validators=[DataRequired()])


# 房东实名信息认证
class LandlordForm(FlaskForm):
    id_name = StringField('id name', id='id_name', validators=[DataRequired()])
    id_no = StringField('id no', id='id_no', validators=[DataRequired()])
    id_pic_1 = StringField('id pic 1', id='id_pic_1', validators=[DataRequired()])
    id_pic_2 = StringField('id pic 2', id='id_pic_2', validators=[DataRequired()])