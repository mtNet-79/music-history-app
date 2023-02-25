from __future__ import annotations
from . import db
from sqlalchemy import Column, String, Integer, DateTime, Date, ForeignKey
from datetime import datetime, date
from typing import Optional, List, Any

from . import (composer_contemporaries, composer_performer,
               composer_style, composer_title)


class Composer(db.Model):  # type: ignore
    __tablename__ = 'composers'
    # Autoincrementing, unique primary key
    id = Column(Integer, primary_key=True)  # type: ignore
    name = Column(String(120))  # type: ignore
    year_born = Column(Date)  # type: ignore
    year_deceased = Column(Date)  # type: ignore
    performers = db.relationship(
        'Performer', secondary=composer_performer, back_populates='composers')  # type: ignore
    titles = db.relationship(
        "Title", secondary=composer_title, back_populates='composers')  # type: ignore
    styles = db.relationship(
        'Style', secondary=composer_style, back_populates='composers')  # type: ignore
    nationality = Column(String)  # type: ignore
    period_id = Column(Integer, ForeignKey('periods.id'))  # type: ignore
    compostitions = db.relationship(
        'Composition', backref=db.backref('composer_compositions', lazy=True))  # type: ignore
    contemporaries = db.relationship(
        'Composer',
        secondary=composer_contemporaries,
        primaryjoin=(id == composer_contemporaries.c.composer_id),
        secondaryjoin=(id == composer_contemporaries.c.contemporary_id),
        backref=db.backref('contemporaries_of', lazy='dynamic'),
        lazy='dynamic'
    )  # type: ignore
    timestamp = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )  # type: ignore

    def __init__(
        self,
        name: Column[str],
        year_born: Column[date],
        nationality: Column[str],
        year_deceased: Column[date],
        period_id: Column[Optional[int]] = None,  # type: ignore
        performers: Column[Optional[List[int]]] = None,  # type: ignore
        titles: Column[Optional[list[object]]] = None,  # type: ignore
        styles: Column[Optional[list[object]]] = None,  # type: ignore
        compostitions: Column[Optional[list[object]]] = None,  # type: ignore
        contemporaries: Column[Optional[List[object]]] = None  # type: ignore
    ) -> None:
        self.name = name
        self.year_born = year_born
        self.year_deceased = year_deceased
        self.nationality = nationality
        self.period_id = period_id
        self.performers = performers or [] # type: ignore
        self.styles = styles or [] # type: ignore
        self.titles = titles or [] # type: ignore
        self.compostitions = compostitions or [] # type: ignore
        self.contemporaries = contemporaries or [] # type: ignore

    def insert(self) -> None:
        db.session.add(self)
        db.session.commit()

    def update(self) -> None:
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    # period = Period.query.get(period_id)

    def format(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'years': [self.year_born, self.year_deceased],
            'period_id': self.period_id,
            'performers': self.performers,
            'nationality': self.nationality,
            'styles': self.styles,
            'titles': self.titles,
            'compostitions': self.compostitions,
            'contemporaries': [c.to_dict() for c in self.contemporaries.all()]
        }

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"{self.name!r}, {self.year_born!r} - {self.year_deceased!r}"
            f")"
        )
# def get_composers():
#     composers = Composer.query.all()
#     all_composers: List["Composer"] = []
#     for composer in composers:
#         all_composers.append((str(composer.id), composer.name))

#     all_composers.sort(key=lambda x: x[1], reverse=True)
#     return all_composers
