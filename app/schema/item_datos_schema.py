from marshmallow import fields
from ..ext import marshmallow
from ..models.item_datos import ItemDatos

class ItemDatosSchema(marshmallow.SQLAlchemySchema):
    class Meta:
        model = ItemDatos

    id = marshmallow.auto_field()
    item_id = marshmallow.auto_field()
    city_id = marshmallow.auto_field()
    quality = marshmallow.auto_field()
    sell_price_min = marshmallow.auto_field()
    sell_price_min_date = marshmallow.auto_field()
    sell_price_max = marshmallow.auto_field()
    sell_price_max_date = marshmallow.auto_field()
    buy_price_min = marshmallow.auto_field()
    buy_price_min_date = marshmallow.auto_field()
    buy_price_max = marshmallow.auto_field()
    buy_price_max_date = marshmallow.auto_field()
    fecha_creacion = marshmallow.auto_field()