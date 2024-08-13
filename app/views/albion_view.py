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

class obtenerValoresCraft(Resource):
    def get(self):
        resp = []
        cuerpo = request.get_json()
        api_comercio_items = ""

        city = City.simple_filter(name_city=cuerpo["city"]).first()

        for item_json in cuerpo["items"]:
            item = Item.simple_filter(id_item=item_json["item_id"]).first()
            if item is None:
                item = Item(item_json["item_id"])
                item.save()
                api_comercio_items += item_json["item_id"]+","
            else:
                item_data = ItemDatos.simple_filter(item_id=item.id,city_id=city.id).first()
                if item_data is not None:
                    result_item_data = ItemDatosSchema().dump(item_data, many=False)
                    fecha = datetime.strptime(result_item_data["fecha_registro"], "%Y-%m-%dT%H:%M:%S")
                    now = datetime.now(timezone.utc).replace(tzinfo=None)
                    time_difference = now - fecha
                    horas = time_difference.total_seconds() / 3600
                    if(horas>1):
                        api_comercio_items += item.id_item+","
                else:
                    api_comercio_items += item.id_item+","
        
        if(api_comercio_items!=""):
            api_comercio_items = api_comercio_items[:-1]
            response = requests.get('https://west.albion-online-data.com/api/v2/stats/prices/'+api_comercio_items+'?locations=Bridgewatch,Caerleon,Fort Sterling,Lymhurst,Martlock,Thetford&qualities=1')
            if response.status_code == 200:
                data = response.json()
                for json_data in data:
                    item_da = Item.simple_filter(id_item=json_data["item_id"]).first()
                    item_id_data = item_da.id
                    city_da = City.simple_filter(name_city=json_data["city"]).first()
                    city_id_data = city_da.id
                    quality_data = json_data["quality"]
                    sell_price_min_data = json_data["sell_price_min"]
                    sell_price_min_date_data = datetime.strptime(json_data["sell_price_min_date"], "%Y-%m-%dT%H:%M:%S")
                    sell_price_max_data = json_data["sell_price_max"]
                    sell_price_max_date_data = datetime.strptime(json_data["sell_price_max_date"], "%Y-%m-%dT%H:%M:%S")
                    buy_price_min_data = json_data["buy_price_min"]
                    buy_price_min_date_data = datetime.strptime(json_data["buy_price_min_date"], "%Y-%m-%dT%H:%M:%S")
                    buy_price_max_data = json_data["buy_price_max"]
                    buy_price_max_date_data = datetime.strptime(json_data["buy_price_max_date"], "%Y-%m-%dT%H:%M:%S")
                    
                    item_datos = ItemDatos.simple_filter(item_id=item_da.id,city_id=city_da.id).first()
                    if item_datos is None:
                        item_data_save = ItemDatos(item_id_data, city_id_data, quality_data, sell_price_min_data, sell_price_min_date_data, sell_price_max_data, sell_price_max_date_data, buy_price_min_data, buy_price_min_date_data, buy_price_max_data, buy_price_max_date_data, datetime.now(timezone.utc))
                        item_data_save.save()
                    else:
                        if(item_datos.sell_price_min == 0):
                            item_datos.sell_price_min = sell_price_min_data
                            item_datos.sell_price_min_date = sell_price_min_date_data
                            
                        if(item_datos.sell_price_max==0):
                            item_datos.sell_price_max = sell_price_max_data
                            item_datos.sell_price_max_date = sell_price_max_date_data

                        if(item_datos.buy_price_min==0):
                            item_datos.buy_price_min = buy_price_min_data
                            item_datos.buy_price_min_date = buy_price_min_date_data
                        
                        if(item_datos.buy_price_max==0):
                            item_datos.buy_price_max = buy_price_max_data
                            item_datos.buy_price_max_date = buy_price_max_date_data

                        item_datos.fecha_registro = datetime.now(timezone.utc)
                        item_datos.update()
        else:
            print("Sin consulta")

        for item in cuerpo["items"]:
            item = Item.simple_filter(id_item=item["item_id"]).first()
            item_data = ItemDatos.simple_filter(item_id=item.id,city_id=city.id).first()
            result_item_data = ItemDatosSchema().dump(item_data, many=False)

            resp_data = {
                "item": item.id_item,
                "precio": item_data.sell_price_min,
                "utc": datetime.strptime(result_item_data["sell_price_min_date"], "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
            }

            resp.append(resp_data)

        return generate_response(message="precios", data=resp, status=HTTP_200_OK)

