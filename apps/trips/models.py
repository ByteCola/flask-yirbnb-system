# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present ByteCola
"""

from apps import db


# 行程实体定义

class Trips(db.Model):
    __tablename__ = 'trips'

    id = db.Column(db.Integer, primary_key=True)
    # 订单号
    order_no = db.Column(db.String(200), comment="订单号")
    # 预定房源标题
    room_title = db.Column(db.String(200), comment="预定房源标题")
    # 预定房源标题图
    room_title_image = db.Column(db.String(255), comment="预定房源标题图")
    # 预定入住人数
    guest_no = db.Column(db.Integer, comment="预定入住人数")
    # 订单总金额
    order_total_fees = db.Column(db.FLOAT, comment="订单总金额")
    # 预定入住日期
    start_date = db.Column(db.DateTime, comment="预定入住日期")
    # 预定退房日期
    end_date = db.Column(db.DateTime, comment="预定退房日期")
    # 预定时间
    order_date = db.Column(db.DateTime, comment="预定时间")
    # 支付状态 notpay:未支付  paid: 已支付
    pay_status = db.Column(db.String(30), comment="付状态 notpay:未支付  paid: 已支付")
    # 支付方式 默认为alipay: 支付宝
    pay_way = db.Column(db.String(30), comment="支付方式 默认为alipay: 支付宝")
    # 预定天数（几晚）
    night = db.Column(db.Integer, comment="预定天数（几晚）")
    # 预定房源价格
    room_price = db.Column(db.Float, comment="预定房源价格")
    # 入住登记人员姓名
    check_person = db.Column(db.String(30), comment="入住登记人员姓名")
    # 入住登记人员手机号
    check_phone = db.Column(db.String(30), comment="入住登记人员手机号")

    # 预定用户 关联用户实体
    users_id = db.Column(db.Integer, db.ForeignKey("Users.id"), comment="预定用户id")
    user = db.relationship("Users", foreign_keys=[users_id], backref="trips")
    # 预定的房源关联
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), comment="预定房源id")
    room = db.relationship("Rooms", backref="trips")

    # 预定的房东关联
    landlord_users_id = db.Column(db.Integer, db.ForeignKey("Users.id"), comment="房东编号")
    landlord = db.relationship("Users", foreign_keys=[landlord_users_id], backref="landlord_trips")

    def __repr__(self):
        return str(self.id)
