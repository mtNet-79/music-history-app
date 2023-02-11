from flaskr import db
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
# from .composer import Composer


class Composition(db.Model):
    __tablename__ = 'compositions'
    id = Column(Integer, primary_key=True)
    name = Column(String(300))
    year = Column(Integer)
    composer_id = Column(Integer, ForeignKey('composers.id'))

    def __repr__(self):
        return f'<Composition {self.name}>'