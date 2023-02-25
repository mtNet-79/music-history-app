from . import db
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
# from .performer import Performer


class Recording(db.Model): # type: ignore
    __tablename__ = 'recordings'
    id = Column(Integer, primary_key=True)
    name = Column(String(300))
    year = Column(Integer)
    performer_id = Column(Integer, ForeignKey('performers.id'))
    composer_id = Column(Integer, ForeignKey('composers.id'))
    
    def __init__(
        self, 
        name: Column[str], 
        years: Column[int], 
        performer_id: Column[int],
        composer_id: Column[int]
    ):
        self.name = name
        self.years = years
        self.performer_id = performer_id
        self.composer_id = composer_id
        
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def __repr__(self):
        return f'<Recording {self.name}>'