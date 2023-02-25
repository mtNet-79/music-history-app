#flake8 : noqa
from . import db
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from .composer import Composer


class Composition(db.Model): # type: ignore
    __tablename__ = 'compositions'
    id = Column(Integer, primary_key=True)
    name = Column(String(300))
    year = Column(Integer)
    composer_id = Column(Integer, ForeignKey('composers.id'))
    
    
    def __init__(
        self,
        name: Column[str],
        year: Column[int],
        composer_id: Column[int]
    ) -> None:
        self.name = name
        self.year = year
        self.composer_id = composer_id

    def insert(self) -> None:
        db.session.add(self)
        db.session.commit()

    def update(self) -> None:
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    # period = Period.query.get(period_id)

    def format(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'year': self.year,
            'composer': Composer.query.get(self.composer_id).one_or_none().name
        }

    def __repr__(self) -> str:
        return f'<Composition {self.name}>'