# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - present ByteCola
"""

from apps import db

class Temp(db.Model):

    __tablename__ = 'temp'

    id = db.Column(db.Integer, primary_key=True)

    firstname = db.Column(db.String(64))
    lastname  = db.Column(db.String(64))
    birthday  = db.Column(db.DateTime)
    gender    = db.Column(db.Integer)
    phone     = db.Column(db.String(32))
    address   = db.Column(db.String(128))
    number    = db.Column(db.String(64))
    city      = db.Column(db.String(64))
    state     = db.Column(db.String(64))
    country   = db.Column(db.String(64))
    zipcode   = db.Column(db.String(16))
    photo     = db.Column(db.String(512))

    def __repr__(self):
        return str(self.id)
