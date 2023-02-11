from flaskr import db
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
# from .performer import Performer


class Recording(db.Model):
    __tablename__ = 'recordings'
    id = Column(Integer, primary_key=True)
    name = Column(String(300))
    year = Column(Integer)
    performer_id = Column(Integer, ForeignKey('performers.id'))

    def __repr__(self):
        return f'<Recording {self.name}>'