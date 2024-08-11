from marshmallow import fields
from ..ext import marshmallow
from ..models.item import Item

class ItemSchema(marshmallow.SQLAlchemySchema):
    class Meta:
        model = Item

    id = marshmallow.auto_field()
    id_item = marshmallow.auto_field()