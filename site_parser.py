import json
import requests

from google.protobuf.json_format import MessageToJson
from proto_structs import offers_pb2

cities = [
    'moskva',
    'sankt-peterburg'
]

shops = [
    'dixy',
    '5ka',
    'vkusvill_offline',
    'magnit-univer',
    'perekrestok',
    'amwine'
]

def parse_page(city = 'sankt-peterburg', shop = 'amwine', page_num = 1):
    """
    :param city: location of the shop
    :param shop: shop name
    :param page_num: parsed page number
    :return: {'offer': [{продукт1}, {продукт2}, ..., {продуктn}]}
    """
    
    url = f"https://squark.edadeal.ru/web/search/offers?count=10000&locality={city}&page={page_num}&retailer={shop}&segment=food"
    data = requests.get(url, allow_redirects=True)
    offers = offers_pb2.Offers()
    offers.ParseFromString(data.content)
    products: str = MessageToJson(offers)
    products = json.loads(products)
    if not products:
        return {'offer': []}
    page_num += 1
    while True:
        url = f"https://squark.edadeal.ru/web/search/offers?count=10000&locality={city}&page={page_num}&retailer={shop}&segment=food"
        data = requests.get(url, allow_redirects=True)
        if data.status_code != 200:
            break
        
        offers = offers_pb2.Offers()
        offers.ParseFromString(data.content)
        upd_products: str = MessageToJson(offers)
        upd_products = json.loads(upd_products)
        products['offer'] += upd_products['offer']
        page_num += 1
    print(products.keys())

    #print(products.get('offer'))
    #json.dumps(products, indent=4, ensure_ascii=False)
    products_copy = []
    for elem in products['offer']:
        if 'amount' in list(elem.keys()):
            products_copy.append(elem)
    products['offer'] = products_copy
    products = filter_products(products=products['offer'], shop=shop)
    # with open('a.json', 'wb') as fd:
    #     fd.write(str(products).encode())
    return products

def filter_products(products, shop):
    new_offer = []
    for product in products:
        if "amount" not in list(product.keys()):
            continue
        if "пакетик" in product['name']:
            continue
        if 'кг' in product['name']:
            product['amount'] = product['amount'] / 1000
        if 'мл' in product['name']:
            product['amount'] = product['amount'] / 1000
        product["shop"] = shop
        new_offer.append(product)
    return {"offer": new_offer}

def get_several_pages(city = 'sankt-peterburg', shop = 'amwine', page_amount = 2):
    result = list()
    for page in range(1, page_amount + 1):
        result.extend(parse_page(city, shop, page).get('offer'))
    return {'offer': result}