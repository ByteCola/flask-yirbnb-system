# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present ByteCola
"""

from apps import db

# 用户房间点赞喜欢

class Like(db.Model):
    __tablename__ = 'like'

    id = db.Column(db.Integer, primary_key=True)


    # 喜欢的房间
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"))
    room = db.relationship("Rooms",  backref="likes")

    # 用户

    users_id = db.Column(db.Integer, db.ForeignKey("Users.id"))
    user = db.relationship("Users", backref="likes")

    def __repr__(self):
        return str(self.facility_code)
