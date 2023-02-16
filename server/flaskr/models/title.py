from . import db
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from typing import Optional


class Title(db.Model):
    __tablename__ = 'titles'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    composers = db.relationship(
        'Composer', secondary='composer_title', back_populates='titles')
    performers = db.relationship(
        'Performer', secondary='performer_title', back_populates='titles')
    
    def __init__(
        self, 
        name: str, 
        composers: Optional[list[int]] = [], 
        performers: Optional[list[int]] = []
    ):
        self.name = name,
        self.composers = composers,
        self.performers = performers
        
        
    def __repr__(self):
        return f'<Title {self.name}>'