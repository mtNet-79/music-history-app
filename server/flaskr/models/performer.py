from flaskr import db
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from . import composer_performer, performer_style, performer_title
from sqlalchemy_utils import IntRangeType
# from datetime import datetime
# from typing import Optional


class Performer(db.Model):
    __tablename__ = 'performers'
    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    title = Column(String(250))
    years = Column(IntRangeType)
    composers = db.relationship(
        'Composer', secondary=composer_performer, back_populates='performers')
    nationality = Column(String)
    titles = db.relationship(
        "Title", secondary=performer_title, back_populates='performers')
    styles = db.relationship(
        "Style", secondary=performer_style, back_populates='performers')
    recordings = db.relationship(
        'Recording', backref=db.backref('performers', lazy=True))
    rating = Column(Integer)

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Performer {self.name}>'
