from . import db
from sqlalchemy import Table, Column, String, Integer, UniqueConstraint, ForeignKey


composer_contemporaries = db.Table('composer_contemporaries',
                                   Column('composer_id', Integer, ForeignKey(
                                       'composers.id'), primary_key=True, index=True),
                                   Column('contemporary_id', Integer, ForeignKey(
                                       'composers.id'), primary_key=True, index=True),
                                   UniqueConstraint('composer_id', 'contemporary_id',
                                                    name='unique_composer_contemporaries')

                                   )
performer_contemporaries = db.Table('performer_contemporaries',
                                    Column('performer_id', Integer, ForeignKey(
                                        'performers.id'), primary_key=True, index=True),
                                    Column('contemporary_id', Integer, ForeignKey(
                                        'performers.id'), primary_key=True, index=True),
                                    UniqueConstraint('performer_id', 'contemporary_id',
                                                     name='unique_performer_contemporaries')

                                    )


composer_performer = db.Table('composer_performer',
                              Column('composer_id', Integer, ForeignKey(
                                  'composers.id'), primary_key=True),
                              Column('performer_id', Integer, ForeignKey(
                                  'performers.id'), primary_key=True)
                              )

composer_style = db.Table('composer_style',
                          Column('composer_id', Integer, ForeignKey(
                              'composers.id'), primary_key=True),
                          Column('style_id', Integer, ForeignKey(
                              'styles.id'), primary_key=True)
                          )
performer_style = db.Table('performer_style',
                           Column('performers_id', Integer, ForeignKey(
                               'performers.id'), primary_key=True),
                           Column('style_id', Integer, ForeignKey(
                               'styles.id'), primary_key=True)
                           )
composer_title = db.Table('composer_title',
                          db.Column('composer_id', db.Integer, db.ForeignKey(
                              'composers.id'), primary_key=True),
                          db.Column('title_id', db.Integer, db.ForeignKey(
                              'titles.id'), primary_key=True)
                          )
performer_title = db.Table('performer_title',
                           db.Column('performers_id', db.Integer, db.ForeignKey(
                               'performers.id'), primary_key=True),
                           db.Column('title_id', db.Integer, db.ForeignKey(
                               'titles.id'), primary_key=True)
                           )
