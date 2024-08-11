from ..ext import marshmallow
from ..models.city import City

class CitySchema(marshmallow.SQLAlchemySchema):
    class Meta:
        model = City

    id = marshmallow.auto_field()
    name_city = marshmallow.auto_field()