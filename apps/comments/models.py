# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present ByteCola
"""

from apps import db

# 评价实体

class Comments(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)

    clean = db.Column(db.Integer)  # 干净卫生 分值
    truth = db.Column(db.Integer)  # 如实描述 分值
    communication = db.Column(db.Integer)  # 沟通顺畅 分值
    location = db.Column(db.Integer)  # 位置便利 分值
    checkin = db.Column(db.Integer)  # 入住便捷 分值
    cost = db.Column(db.Integer)  # 高性价比 分值

    content = db.Column(db.String(500))  # 评价内容
    comment_date = db.Column(db.DateTime) # 评价时间

    # 评价人
    users_id = db.Column(db.Integer, db.ForeignKey("Users.id"))
    user = db.relationship("Users", foreign_keys=[users_id], backref="my_comments")

    # 评价房间
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"))
    room = db.relationship("Rooms", backref="comments")

    # 评价房东
    landlord_id = db.Column(db.Integer, db.ForeignKey("Users.id"))
    landlord = db.relationship("Users",foreign_keys=[landlord_id], backref="comments")

    # 评价行程
    trip_id = db.Column(db.Integer, db.ForeignKey("trips.id"))
    trips = db.relationship("Trips", backref="comments")

    def __repr__(self):
        return str(self.id)
