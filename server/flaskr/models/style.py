from flaskr import db
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey

class Style(db.Model):
    __tablename__ = 'styles'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    composers = db.relationship(
        'Composer', secondary='composer_style', back_populates='styles')
    performers = db.relationship(
        'Performer', secondary='performer_style', back_populates='styles')