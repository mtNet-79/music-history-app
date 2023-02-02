import os
from sqlalchemy import Column, String, Integer, UniqueConstraint, relationship, back_populates, ForeignKey, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
from sqlalchemy_utils import IntRangeType
from datetime import datetime

# declare db to use ORM
# declare flask migrate for version control
db = SQLAlchemy()
migrate = Migrate()

"""
setup_db(app)
    binds flask application to SQLAlchemy service
    called in flaskr package at __init__.py
"""


def setup_db(app):

    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)
    db.create_all()


composer_performer = db.Table('composer_performer',
                              Column('composer_id', Integer, db.ForeignKey(
                                  'composers.id'), primary_key=True),
                              Column('performer_id', Integer, db.ForeignKey(
                                  'performers.id'), primary_key=True)
                              )

contemporaries = db.Table('contemoparaies',
                          Column('composer_id', Integer, db.ForeignKey(
                              'composers.id'), index=True),
                          Column('contemporary_id', Integer,
                                 db.ForeignKey('composers.id'), index=True),
                          UniqueConstraint('composer_id', 'contemporary_id',
                                           name='unique_contemoparaies')
                          )


class Composer(db.Model):
    __tablename__ = 'composers'
    # Autoincrementing, unique primary key
    id = Column(Integer, primary_key=True)
    name = Column(db.String(120))
    years = Column(IntRangeType)
    performers = relationship('Performer',
                              secondary=composer_performer,
                              backref=back_populates('composers', lazy=True))
    nationality = Column(String)
    styles: relationship(
        "Style", backref=back_populates('composers', lazy=True))
    period_id:  Column(Integer, ForeignKey('periods.id'))
    compostitions: relationship(
        'Composition', backref=back_populates('composers', lazy=True))
    contemporaries: relationship('Composer',
                                 sedondary=contemporaries,
                                 primaryjoin=id == contemporaries.c.composer_id,
                                 secondaryjoin=id == contemporaries.c.contemporary_id,)
    timestamp = db.Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __init__(self, name: str, years: "IntRangeType", performers: list["id"],
                 nationality: str, styles: list["id"], period_id: int, compostitions: list["id"], contemporaries: list["id"]):
        self.name = name
        self.years = years
        self.performers = performers
        self.nationality = nationality
        self.styles = styles
        self.period_id = period_id
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
            'years': self.years,
            'performers': self.performers,
            'nationality': self.nationality,
            'styles': self.styles,
            'period_id': self.period_id,
            'compostitions': self.compostitions,
            'contemporaries': self.contemporaries
        }

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


class Performer(db.Model):
    __tablename__ = 'performers'
    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    title = Column(String(250))
    years = Column(IntRangeType)
    composers = relationship('Composer',
                             secondary=composer_performer,
                             backref=back_populates('performers', lazy=True))
    nationality = Column(String)
    styles: relationship(
        "Style", backref=back_populates('performers', lazy=True))
    recordings: relationship(
        'Recording', backref=back_populates('performers', lazy=True))
    rating: Column(Integer)

    def __repr__(self):
        return f'<Performer {self.name}>'


class Period(db.Model):
    __tablename__ = 'periods'
    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    years = Column(IntRangeType)
    composers: relationship(
        'Composer', backref=back_populates('periods', lazy=True))

    def __repr__(self):
        return f'<Period {self.name}>'


class Compositions(db.Model):
    __tablename__ = 'compositions'
    id = Column(Integer, primary_key=True)
    name = Column(String(300))
    year: Column(Integer)
    composer_id: Column(Integer, ForeignKey('composers.id'))

    def __repr__(self):
        return f'<Composition {self.name}>'


class Recording(db.Model):
    __tablename__ = 'recordings'
    id = Column(Integer, primary_key=True)
    name = Column(String(300))
    year: Column(Integer)
    performer_id: Column(Integer, ForeignKey('performers.id'))

    def __repr__(self):
        return f'<Recording {self.name}>'
