from . import db
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from typing import Optional

class Style(db.Model):
    __tablename__ = 'styles'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    composers = db.relationship(
        'Composer', secondary='composer_style', back_populates='styles')
    performers = db.relationship(
        'Performer', secondary='performer_style', back_populates='styles')
    
    def __init__(
        self, 
        name: str, 
        composers: Optional[list[int]] = [], 
        performers: Optional[list[int]] = []
    ):
        self.name = name,
        self.composers = composers,
        self.performers = performers
        
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def __repr__(self):
        return f'<Style {self.name}>'