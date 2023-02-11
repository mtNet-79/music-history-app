import os
from typing import Optional
from sqlalchemy import Column, String, Integer, UniqueConstraint, DateTime, ForeignKey, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json
from sqlalchemy_utils import IntRangeType
from datetime import datetime
# from app import db

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
    # db.create_all()


def setup_test_db(app):
    db.init_app(app)


contemporaries = db.Table('contemporaries',
                          db.Column('composer_id', db.Integer, db.ForeignKey(
                              'composers.id'), primary_key=True, index=True),
                          db.Column('contemporary_id', db.Integer, db.ForeignKey(
                              'composers.id'), primary_key=True, index=True),
                          UniqueConstraint('composer_id', 'contemporary_id',
                                           name='unique_contemporaries')

                          )


composer_performer = db.Table('composer_performer',
                              Column('composer_id', Integer, db.ForeignKey(
                                  'composers.id'), primary_key=True),
                              Column('performer_id', Integer, db.ForeignKey(
                                  'performers.id'), primary_key=True)
                              )

composer_style = db.Table('composer_style',
                          db.Column('composer_id', db.Integer, db.ForeignKey(
                              'composers.id'), primary_key=True),
                          db.Column('style_id', db.Integer, db.ForeignKey(
                              'styles.id'), primary_key=True)
                          )
performer_style = db.Table('performer_style',
                           db.Column('performers_id', db.Integer, db.ForeignKey(
                               'performers.id'), primary_key=True),
                           db.Column('style_id', db.Integer, db.ForeignKey(
                               'styles.id'), primary_key=True)
                           )

print("IN MODELS LINE 65")
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


class Performer(db.Model):
    __tablename__ = 'performers'
    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    title = Column(String(250))
    years = Column(IntRangeType)
    composers = db.relationship(
        'Composer', secondary=composer_performer, back_populates='performers')
    nationality = Column(String)
    styles = db.relationship(
        "Style", secondary=performer_style, back_populates='performers')
    recordings = db.relationship(
        'Recording', backref=db.backref('performers', lazy=True))
    rating = Column(Integer)

    def __repr__(self):
        return f'<Performer {self.name}>'


class Style(db.Model):
    __tablename__ = 'styles'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    composers = db.relationship(
        'Composer', secondary='composer_style', back_populates='styles')
    performers = db.relationship(
        'Performer', secondary='performer_style', back_populates='styles')


class Period(db.Model):
    __tablename__ = 'periods'
    id = Column(Integer, primary_key=True)
    name = Column(String(120))
    years = Column(IntRangeType)
    composers = db.relationship(
        'Composer', backref=db.backref('periods', lazy=True))

    def __repr__(self):
        return f'<Period {self.name}>'


class Composition(db.Model):
    __tablename__ = 'compositions'
    id = Column(Integer, primary_key=True)
    name = Column(String(300))
    year = Column(Integer)
    composer_id = Column(Integer, ForeignKey('composers.id'))

    def __repr__(self):
        return f'<Composition {self.name}>'


class Recording(db.Model):
    __tablename__ = 'recordings'
    id = Column(Integer, primary_key=True)
    name = Column(String(300))
    year = Column(Integer)
    performer_id = Column(Integer, ForeignKey('performers.id'))

    def __repr__(self):
        return f'<Recording {self.name}>'
