# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present ByteCola
"""

from apps import db


# 用户个人信息实体定义

class Profiles(db.Model):
    __tablename__ = 'profiles'

    id = db.Column(db.Integer, primary_key=True)

    # firstname = db.Column(db.String(64))
    # lastname = db.Column(db.String(64))
    # 姓名
    fullname = db.Column(db.String(64))
    # 出生日期
    birthday = db.Column(db.DateTime)
    # 性别
    gender = db.Column(db.Integer)
    # 手机
    phone = db.Column(db.String(32))
    # 居住地址
    address = db.Column(db.String(128))
    #
    # number = db.Column(db.String(64))
    # 城市
    city = db.Column(db.String(64))
    # 省份
    # state = db.Column(db.String(64))
    # 国家
    country = db.Column(db.String(64))
    # 邮编
    zipcode = db.Column(db.String(16))
    # 头像
    photo = db.Column(db.String(512))

    # 关联用户
    users_id = db.Column(db.Integer, db.ForeignKey("Users.id"))
    user = db.relationship("Users", uselist=False, backref="profiles")

    def __repr__(self):
        return str(self.id)


# 个人收款实体
class Billing(db.Model):
    __tablename__ = 'billing'

    id = db.Column(db.Integer, primary_key=True)

    # 收款账号
    account = db.Column(db.String(64))

    # 关联用户
    users_id = db.Column(db.Integer, db.ForeignKey("Users.id"))
    user = db.relationship("Users", uselist=False, backref="billing")

    def __repr__(self):
        return str(self.id)


# 房东信息认证实体

class Landlord(db.Model):
    __tablename__ = 'landlord'
    id = db.Column(db.Integer,primary_key=True)

    # 真实姓名
    id_name = db.Column(db.String(30))
    # 真实身份证号
    id_no = db.Column(db.String(20))
    # 身份证人像面
    id_pic_1 = db.Column(db.String(300))
    # 身份证国徽面
    id_pic_2 = db.Column(db.String(300))

    # 关联用户
    users_id = db.Column(db.Integer, db.ForeignKey("Users.id"))
    user = db.relationship("Users", uselist=False, backref="landlord")

    def __repr__(self):
        return str(self.id)