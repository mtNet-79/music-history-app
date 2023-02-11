from flaskr import db
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy_utils import IntRangeType
from datetime import datetime
from typing import Optional
from . import contemporaries, composer_performer, composer_style, performer_style


class Composer(db.Model):
    __tablename__ = 'composers'
    # Autoincrementing, unique primary key
    id = Column(Integer, primary_key=True)
    name = Column(db.String(120))
    years = Column(IntRangeType)
    performers = db.relationship(
        'Performer', secondary=composer_performer, back_populates='composers')
    styles = db.relationship(
        'Style', secondary='composer_style', back_populates='composers')
    nationality = Column(String)
    period_id = Column(Integer, ForeignKey('periods.id'))
    compostitions = db.relationship(
        'Composition', backref=db.backref('composer_compositions', lazy=True))
    contemporaries = db.relationship(
        'Composer',
        secondary='contemporaries',
        primaryjoin=(id == contemporaries.c.composer_id),
        secondaryjoin=(id == contemporaries.c.contemporary_id),
        backref=db.backref('contemporaries_of', lazy='dynamic'),
        lazy='dynamic'
    )
    # contemporaries=db.relationship('Composer',
    #                              secondary = contemporaries,
    #                              primaryjoin = id == contemporaries.c.composer_id,
    #                              secondaryjoin = id == contemporaries.c.contemporary_id,)
    timestamp = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __init__(
        self, name: str,
        years: "IntRangeType",
        nationality: str,
        period_id: Optional[int] = None,
        performers: Optional[list[int]] = [],
        styles: Optional[list[int]] = [],
        compostitions: Optional[list[int]] = [],
        contemporaries: Optional[list[int]] = []
    ):
        self.name = name
        self.years = years
        self.nationality = nationality
        self.period_id = period_id
        self.performers = performers
        self.styles = styles
        self.compostitions = compostitions
        self.contemporaries = contemporaries

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # period = Period.query.get(period_id)

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'years': [self.years.lower, self.years.upper],
            'period_id': self.period_id,
            'performers': self.performers,
            'nationality': self.nationality,
            'styles': self.styles,
            'compostitions': self.compostitions,
            'contemporaries': [c.to_dict() for c in self.contemporaries.all()]
        }
    print("IN CLASS LINE 140")

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}("
            f"{self.name!r}, {self.years.lower!r} - {self.years.upper!r}"
            f")"
        )
def get_composers():
    composers = Composer.query.all()
    all_composers: List["Composer"] = []
    for composer in composers:
        all_composers.append((str(composer.id), composer.name))

    all_composers.sort(key=lambda x: x[1], reverse=True)
    return all_composers