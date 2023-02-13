from flaskr import db
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey


class Title(db.Model):
    __tablename__ = 'titles'
    id = Column(Integer, primary_key=True)
    name = Column(String(250))
    composers = db.relationship(
        'Composer', secondary='composer_title', back_populates='titles')
    performers = db.relationship(
        'Performer', secondary='performer_title', back_populates='titles')
    def __repr__(self):
        return f'<Title {self.name}>'