# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present ByteCola
"""

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, FileField, IntegerField, DecimalField, TextAreaField
from wtforms.validators import DataRequired


# 房源（房间）FlaskForm表单定义

class RoomForm(FlaskForm):
    # 房源标题
    title = StringField('Room Title', id='title', validators=[DataRequired()])
    # 国家
    country = StringField('Room country', id='country', validators=[DataRequired()])
    # 省份、州
    state = StringField('Room state', id='state', validators=[DataRequired()])
    # 城市
    city = StringField('Room city', id='city', validators=[DataRequired()])
    # 居住地址
    address = StringField('Room address', id='address', validators=[DataRequired()])
    # 最大入住人数
    max_guest = IntegerField('Room max_guest', id='max_guest', validators=[DataRequired()], default=1)
    # 房源类型
    category = SelectField('Room category', id='category', validators=[DataRequired()],
                           choices=[("1", "普通公寓"), ("2", "乡间小屋"), ("3", "度假村"), ("4", "别墅"), ("5", "茅屋")])
    # 价格
    price = DecimalField('Room price', id='price', validators=[DataRequired()])
    # 卧室数
    bedroom = IntegerField('Room bedroom', id='bedroom', validators=[DataRequired()], default=1)
    # 洗手间数
    washroom = IntegerField('Room washroom', id='washroom', validators=[DataRequired()], default=1)
    # 床位数
    bed = IntegerField('Room bed', id='bed', validators=[DataRequired()], default=1)
    # 房源描述
    detail = TextAreaField('Room detail', id='detail', validators=[DataRequired()])
    # 房源标题图 列表展示用
    title_photo = FileField('Room title_photo', id='title_photo')
    # photos = MultipleFileField('Room photos', id='photos', validators=[DataRequired()])
    # 房源图集 详情页展示用
    photos = StringField('Room photos', id="photos", validators=[DataRequired()])
    # 手机号
    phone = StringField('Room phone', id='phone', validators=[DataRequired()])
    # 房源标签 多个标签以英文逗号分隔
    tags = StringField('Room tags', id='tags', validators=[DataRequired()])
    # 方便入住/退房提示说明
    check_tips = StringField('Room check_tips', id='check_tips', validators=[DataRequired()])

    # facilities = FieldList(FormField(Facility))
