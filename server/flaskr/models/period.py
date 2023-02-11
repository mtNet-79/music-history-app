from flaskr import db
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy_utils import IntRangeType
# from .composer import Composer


class Period(db.Model):
    __tablename__ = 'periods'
    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    years = Column(IntRangeType)
    composers = db.relationship(
        'Composer', backref=db.backref('periods', lazy=True))

    def __repr__(self):
        return f'<Period {self.name}>'