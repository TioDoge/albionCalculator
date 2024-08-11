from ..db import db, BaseModelMixin
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class Item(db.Model, BaseModelMixin):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    id_item: Mapped[str] = mapped_column(String(50), unique=True)

    def __init__(self, id_item):
        self.id_item = id_item

    def __repr__(self):
        return '<Item {}>'.format(self.id)
    
    def __str__(self):
        return 'Item {}'.format(self.id)