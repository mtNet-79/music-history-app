from . import db
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy_utils import IntRangeType
from typing import Optional
# from .composer import Composer


class Period(db.Model):
    __tablename__ = 'periods'
    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    years = Column(IntRangeType)
    composers = db.relationship(
        'Composer', backref=db.backref('periods', lazy=True))
    
    def __init__(
        self, 
        name: str, 
        years: int, 
        composers: Optional[list] = []
    ):
        self.name = name,
        self.years = years,
        self.composers = composers
        
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Period {self.name}>'