from db import DB
from site_parser import parse_page
import time
shops_list = ["5ka", "magnit-univer", "amwine" , "dixy" , "verno" , "winelab" , "vkusvill_offline" , "7shagoff" , "perekrestok" , "tdreal.spb", "norman_1" , "velikolukskij-myasokombinat", "mini-lenta", "lenta-giper", "lenta-super", "okmarket-giper", "eurospar" , "auchan" , "esh-derevenskoe", "rosal24" , "glavpivo" ]

database = DB()
while True:
    result = {}
    for shop in shops_list:
        try:
            result[shop] = parse_page(shop=shop)['offer']    
        except:
            continue
    database.update_products(result)
    time.sleep(600)
