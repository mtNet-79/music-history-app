from . import db
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
# from sqlalchemy_utils import IntRangeType
from datetime import datetime
from typing import Optional, List
from . import composer_contemporaries, composer_performer, composer_style, composer_title


class Composer(db.Model):
    __tablename__ = 'composers'
    # Autoincrementing, unique primary key
    id = Column(Integer, primary_key=True)
    name = Column(db.String(120))
    year_born = Column(Integer)
    year_deceased = Column(Integer)
    performers = db.relationship(
        'Performer', secondary=composer_performer, back_populates='composers')
    titles = db.relationship(
        "Title", secondary=composer_title, back_populates='composers')
    styles = db.relationship(
        'Style', secondary=composer_style, back_populates='composers')
    nationality = Column(String)
    period_id = Column(Integer, ForeignKey('periods.id'))
    compostitions = db.relationship(
        'Composition', backref=db.backref('composer_compositions', lazy=True))
    contemporaries = db.relationship(
        'Composer',
        secondary=composer_contemporaries,
        primaryjoin=(id == composer_contemporaries.c.composer_id),
        secondaryjoin=(id == composer_contemporaries.c.contemporary_id),
        backref=db.backref('contemporaries_of', lazy='dynamic'),
        lazy='dynamic'
    )
    timestamp = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __init__(
        self,
        name: str,
        year_born: int,
        nationality: str,
        year_deceased: Optional[int] = None, 
        period_id: Optional[int] = None,
        performers: Optional[List[int]] = None,
        titles: Optional[List[int]] = None,
        styles: Optional[List[int]] = None,
        compostitions: Optional[List[int]] = None,
        contemporaries: Optional[List[int]] = None
    ):
        self.name = name
        self.year_born = year_born
        self.year_deceased = year_deceased
        self.nationality = nationality
        self.period_id = period_id
        self.performers = performers or []
        self.styles = styles or []
        self.titles = titles or []
        self.compostitions = compostitions or []
        self.contemporaries = contemporaries or []

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
