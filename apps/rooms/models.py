# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present ByteCola
"""

from apps import db


# 房源（房间）实体定义

class Rooms(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    # 房源标题
    title = db.Column(db.String(200))
    # 国家
    country = db.Column(db.String(64))
    # 省份、州
    state = db.Column(db.String(64))
    # 城市
    city = db.Column(db.String(64))
    # 详细地址
    address = db.Column(db.String(128))
    # 最大居住人数
    max_guest = db.Column(db.Integer)
    # 房源类型
    category = db.Column(db.String(32))
    # 房间价格
    price = db.Column(db.FLOAT)
    # 卧室数
    bedroom = db.Column(db.Integer)
    # 洗手间数
    washroom = db.Column(db.Integer)
    # 床位数
    bed = db.Column(db.Integer)
    # 房源介绍详情
    detail = db.Column(db.Text)
    # 房源标题图 列表页展示用
    title_photo = db.Column(db.String(255))
    # 房间图集
    photos = db.Column(db.String(2000))
    # 房间电话
    phone = db.Column(db.String(32))
    # 房源标签
    tags = db.Column(db.String(200))
    # 房源入住/退房提示说明
    check_tips = db.Column(db.String(255))
    # 发布时间
    create_date = db.Column(db.DateTime)
    # 房源状态 正常入住、暂定入住
    status = db.Column(db.String(10), default='1', comment='房源状态  1 正常入住  2 暂停入住  3 房源已被删除')
    # 查看统计
    views = db.Column(db.Integer, default=0, comment='访问统计数量')
    # 点赞统计
    loves = db.Column(db.Integer, default=0, comment='点赞统计数量')

    users_id = db.Column(db.Integer, db.ForeignKey("Users.id"))
    user = db.relationship("Users", backref="rooms")

    # facilities = db.relationship("Facility")

    # __mapper_args__ = {
    #     'order_by': create_date.desc()
    # }

    def __repr__(self):
        return str(self.id)
