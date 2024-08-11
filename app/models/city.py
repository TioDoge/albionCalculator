from ..db import db, BaseModelMixin
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class City(db.Model, BaseModelMixin):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name_city: Mapped[str] = mapped_column(String(50), unique=True)

    def __init__(self, nombre):
        self.nombre = nombre

    def __repr__(self):
        return '<City {}>'.format(self.id)
    
    def __str__(self):
        return 'City {}'.format(self.id)