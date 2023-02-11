from flaskr import db
from sqlalchemy import Table, Column, String, Integer, UniqueConstraint, ForeignKey
print("WAIT")
contemporaries = db.Table('contemporaries',
                          Column('composer_id', Integer, ForeignKey(
                              'composers.id'), primary_key=True, index=True),
                          Column('contemporary_id', Integer, ForeignKey(
                              'composers.id'), primary_key=True, index=True),
                          UniqueConstraint('composer_id', 'contemporary_id',
                                           name='unique_contemporaries')

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
