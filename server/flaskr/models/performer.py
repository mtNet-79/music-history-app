from . import db
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from . import composer_performer, performer_style, performer_title, performer_contemporaries
# from sqlalchemy_utils import IntRangeType
from datetime import datetime
from typing import Optional, List


class Performer(db.Model):
    __tablename__ = 'performers'
    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    title = Column(String(250))
    year_born = Column(Integer)
    year_deceased = Column(Integer)
    composers = db.relationship(
        'Composer', secondary=composer_performer, back_populates='performers')
    contemporaries = db.relationship(
        "Performer", 
        secondary=performer_contemporaries, 
        primaryjoin=(id == performer_contemporaries.c.performer_id),
        secondaryjoin=(id == performer_contemporaries.c.contemporary_id),
        backref=db.backref('contemporaries_of', lazy='dynamic'),
        lazy='dynamic'
    )
    nationality = Column(String)
    titles = db.relationship(
        "Title", secondary=performer_title, back_populates='performers')
    styles = db.relationship(
        "Style", secondary=performer_style, back_populates='performers')
    recordings = db.relationship(
        'Recording', backref=db.backref('performers', lazy=True))
    rating = Column(Integer)
    timestamp = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __init__(
        self,
        name: str,
        year_born: int,
        nationality: str,
        year_deceased: Optional[int] = None,        
        composers: Optional[List[int]] = None,
        titles: Optional[List[int]] = None,
        styles: Optional[List[int]] = None,
        recordings: Optional[List[int]] = None,
        rating: Optional[int] = None
    ):
        self.name = name
        self.year_born = year_born
        self.year_deceased = year_deceased
        self.nationality = nationality 
        self.composers = composers or []
        self.styles = styles or []
        self.titles = titles or []
        self.recordings = recordings or []
        self.rating = rating

    def insert(self):
        print(f"Here is SELF {self}")
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()    
        
    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'years': [self.year_born, self.year_deceased],
            'composers': self.composers,
            'nationality': self.nationality,
            'styles': self.styles,
            'titles': [t.name for t in self.titles],
            'recordings': self.recordings,
            'contemporaries': [c.to_dict() for c in self.contemporaries.all()]
        }

    def __repr__(self):
        return f'<Performer {self.name}>'
