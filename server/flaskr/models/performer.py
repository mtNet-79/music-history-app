# flake8: noqa
from . import db
from sqlalchemy import Column, String, Integer, DateTime, Date
from . import composer_performer, performer_style, performer_title, performer_contemporaries
# from sqlalchemy_utils import IntRangeType
from datetime import datetime, date
from typing import Optional, List


class Performer(db.Model):  # type: ignore
    __tablename__ = 'performers'
    id = Column(Integer, primary_key=True)  # type: ignore
    name = Column(String(120))  # type: ignore
    year_born = Column(Date)  # type: ignore
    year_deceased = Column(Date)  # type: ignore
    composers = db.relationship(
        'Composer', secondary=composer_performer, back_populates='performers')  # type: ignore
    contemporaries = db.relationship(
        "Performer",
        secondary=performer_contemporaries,  # type: ignore
        primaryjoin=(id == performer_contemporaries.c.performer_id),  # type: ignore
        secondaryjoin=(id == performer_contemporaries.c.contemporary_id),  # type: ignore
        backref=db.backref('contemporaries_of', lazy='dynamic'),
        lazy='dynamic'
    )  # type: ignore
    nationality = Column(String)  # type: ignore
    titles = db.relationship( 
        "Title", secondary=performer_title, back_populates='performers')  # type: ignore
    styles = db.relationship(
        "Style", secondary=performer_style, back_populates='performers')  # type: ignore
    recordings = db.relationship(
        'Recording', backref=db.backref('performers', lazy=True))  # type: ignore
    rating = Column(Integer)  # type: ignore
    timestamp = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )  # type: ignore

    def __init__(
        self,
        name: Column[str],
        year_born: Column[date],
        nationality: Column[str],
        year_deceased: Column[date] = None,  # type: ignore
        composers: Column[List[object]] = None,  # type: ignore
        titles: Column[List[object]] = None,  # type: ignore
        styles: Column[List[object]] = None,  # type: ignore
        recordings: Column[Optional[List[object]]] = None,  # type: ignore
        rating: Column[int] = None  # type: ignore
    ) -> None:
        self.name = name
        self.year_born = year_born
        self.year_deceased = year_deceased
        self.nationality = nationality
        self.composers = composers or []  # type: ignore
        self.styles = styles or []  # type: ignore
        self.titles = titles or []  # type: ignore
        self.recordings = recordings or []  # type: ignore
        self.rating = rating  # type: ignore

    def insert(self) -> None:
        print(f"Here is SELF {self}")
        db.session.add(self)
        db.session.commit()

    def update(self) -> None:
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    def format(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'years': [self.year_born, self.year_deceased],
            'composers': self.composers,
            'nationality': self.nationality,
            'styles': self.styles,
            'titles': [t.name for t in self.titles], # type: ignore
            'recordings': self.recordings,
            'contemporaries': [c.to_dict() for c in self.contemporaries.all()]
        }

    def __repr__(self) -> str:
        return f'<Performer {self.name}>'
