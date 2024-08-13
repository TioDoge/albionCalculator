import datetime
from ..db import db, BaseModelMixin
from sqlalchemy import Integer, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..models.city import City
from ..models.item import Item

class ItemDatos(db.Model, BaseModelMixin):
    __tablename__ = "item_datos"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    item_id: Mapped[int] = mapped_column(ForeignKey('item.id'))
    city_id: Mapped[int] = mapped_column(ForeignKey('city.id'))
    quality: Mapped[int] = mapped_column(Integer)
    sell_price_min: Mapped[int] = mapped_column(Integer)
    sell_price_min_date: Mapped[DateTime] = mapped_column(DateTime, default=datetime.datetime.now)
    sell_price_max: Mapped[int] = mapped_column(Integer)
    sell_price_max_date: Mapped[DateTime] = mapped_column(DateTime, default=datetime.datetime.now)
    buy_price_min: Mapped[int] = mapped_column(Integer)
    buy_price_min_date: Mapped[DateTime] = mapped_column(DateTime, default=datetime.datetime.now)
    buy_price_max: Mapped[int] = mapped_column(Integer)
    buy_price_max_date: Mapped[DateTime] = mapped_column(DateTime, default=datetime.datetime.now)
    fecha_registro: Mapped[DateTime] = mapped_column(DateTime, default=datetime.datetime.now)

    item = relationship(Item)
    city = relationship(City)

    def __init__(self, item_id, city_id, quality, sell_price_min, sell_price_min_date, sell_price_max, sell_price_max_date, buy_price_min, buy_price_min_date, buy_price_max, buy_price_max_date, fecha_registro):
        self.item_id = item_id
        self.city_id = city_id
        self.quality = quality
        self.sell_price_min = sell_price_min
        self.sell_price_min_date = sell_price_min_date
        self.sell_price_max = sell_price_max
        self.sell_price_max_date = sell_price_max_date
        self.buy_price_min = buy_price_min
        self.buy_price_min_date = buy_price_min_date
        self.buy_price_max = buy_price_max
        self.buy_price_max_date = buy_price_max_date
        self.fecha_registro = fecha_registro
        
    def __repr__(self):
        return '<ItemData {}>'.format(self.id)
    
    def __str__(self):
        return 'ItemData {}'.format(self.id)
    