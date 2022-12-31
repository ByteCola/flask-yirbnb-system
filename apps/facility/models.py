# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present ByteCola
"""

from apps import db

# 房间便利设施实体定义

class Facility(db.Model):
    __tablename__ = 'facility'

    id = db.Column(db.Integer, primary_key=True)
    # 设施编码
    facility_code = db.Column(db.String(32))

    # 所属房间
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"))
    room = db.relationship("Rooms",  backref="facilities")

    def __repr__(self):
        return str(self.facility_code)
