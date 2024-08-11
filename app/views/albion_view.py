import requests
from datetime import datetime, timezone
from flask import request
from flask_restful import Resource

from ..models.item import Item
from ..models.item_datos import ItemDatos
from ..models.city import City
from ..db import *

from ..schema.item_datos_schema import ItemDatosSchema

from ..common.generate_response import generate_response
from ..common.http_code import HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

class calcularGastos(Resource):
    def get(self):
        resp = []
        cuerpo = request.get_json()
        api_comercio_items = ""

        city = City.simple_filter(name_city=cuerpo["city"]).first()

        for item in cuerpo["items"]:
            item = Item.simple_filter(id_item=item["item_id"]).first()
            if item is None:
                item = Item(item["item_id"])
                item.save()
                api_comercio_items += item.id_item + ","
            else:
                item_data = ItemDatos.simple_filter(item_id=item.id).first()
                if item_data is not None:
                    result_item_data = ItemDatosSchema().dump(item_data, many=False)
                    fecha = datetime.strptime(result_item_data["fecha_creacion"], "%Y-%m-%dT%H:%M:%S")
                    print("Fecha",fecha)
                    now = datetime.now(timezone.utc).replace(tzinfo=None)
                    time_difference = now - fecha
                    horas = time_difference.total_seconds() / 3600
                    if(horas>1):
                        api_comercio_items += item.id_item + ","
                else:
                    api_comercio_items += item.id_item + ","

        if(api_comercio_items!=""):
            api_comercio_items = api_comercio_items[:-1]
            print("Items api",api_comercio_items)
            response = requests.get('https://west.albion-online-data.com/api/v2/stats/prices/'+api_comercio_items+'?locations='+city.name_city+'&qualities=1')
            if response.status_code == 200:
                data = response.json()
                for json_data in data:
                    item_comp = Item.simple_filter(id_item=json_data["item_id"]).first()

                    print("Item",item_comp.id)
                    print("Ciudad",city.id)

                    item_datos_comp = ItemDatos.simple_filter(item_id=item_comp.id,city_id=city.id).first()

                    if(item_datos_comp is None):
                        item_id_data = item_comp.id
                        city_id_data = city.id
                        quality_data = json_data["quality"]
                        sell_price_min_data = json_data["sell_price_min"]
                        sell_price_min_date_data = datetime.strptime(json_data["sell_price_min_date"], "%Y-%m-%dT%H:%M:%S")
                        sell_price_max_data = json_data["sell_price_max"]
                        sell_price_max_date_data = datetime.strptime(json_data["sell_price_max_date"], "%Y-%m-%dT%H:%M:%S")
                        buy_price_min_data = json_data["buy_price_min"]
                        buy_price_min_date_data = datetime.strptime(json_data["buy_price_min_date"], "%Y-%m-%dT%H:%M:%S")
                        buy_price_max_data = json_data["buy_price_max"]
                        buy_price_max_date_data = datetime.strptime(json_data["buy_price_max_date"], "%Y-%m-%dT%H:%M:%S")
                        item_data_save = ItemDatos(item_id_data, city_id_data, quality_data, sell_price_min_data, sell_price_min_date_data, sell_price_max_data, sell_price_max_date_data, buy_price_min_data, buy_price_min_date_data, buy_price_max_data, buy_price_max_date_data, datetime.now(timezone.utc))
                        item_data_save.save()
                    else:
                        item_datos_comp.quality_data = json_data["quality"]
                        item_datos_comp.sell_price_min_data = json_data["sell_price_min"]
                        item_datos_comp.sell_price_min_date_data = datetime.strptime(json_data["sell_price_min_date"], "%Y-%m-%dT%H:%M:%S")
                        item_datos_comp.sell_price_max_data = json_data["sell_price_max"]
                        item_datos_comp.sell_price_max_date_data = datetime.strptime(json_data["sell_price_max_date"], "%Y-%m-%dT%H:%M:%S")
                        item_datos_comp.buy_price_min_data = json_data["buy_price_min"]
                        item_datos_comp.buy_price_min_date_data = datetime.strptime(json_data["buy_price_min_date"], "%Y-%m-%dT%H:%M:%S")
                        item_datos_comp.buy_price_max_data = json_data["buy_price_max"]
                        item_datos_comp.buy_price_max_date_data = datetime.strptime(json_data["buy_price_max_date"], "%Y-%m-%dT%H:%M:%S")
                        item_datos_comp.fecha_creacion = datetime.now(timezone.utc)
                        item_datos_comp.update()

        for item in cuerpo["items"]:
            item = Item.simple_filter(id_item=item["item_id"]).first()
            item_datos = ItemDatos.simple_filter(item_id=item.id).first()
            json = {
                "ITEM":item.id_item,
                "PRECIO":item_datos.sell_price_min
            }
            resp.append(json)

        return generate_response(message="Costos", data=resp, status=HTTP_200_OK)
            
