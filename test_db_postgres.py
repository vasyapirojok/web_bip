from ration import *


def filter_products(products, shop="5ka"):
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


with open('full_offer.json', 'rb') as fd:
    a = fd.read()
string = a.decode("utf-8")
aa = ast.literal_eval(string)
aa = filter_products(aa['offer'])
b, c, d = magic_ext(products=aa, full_price=10000, days_number=7)

with open('magic_ext_res.json', 'wb') as fd:
    fd.write(str(b).encode('utf-8'))


# def magic_ext(products, full_price, days_number):
    
#     # price_per_day = full_price // days_number
#     max_portions = days_number / 2
#     prices = {
#         "breakfast": int((full_price) * 0.26),
#         "lunch": int((full_price) * 0.37),
#         "dinner": int((full_price) * 0.37)
#     }
#     if sum(list(prices.values())) > full_price:
#         prices["dinner"] -= full_price - sum(list(prices.values()))
#     with open('oracle.json', 'rb') as fd:
#         oracle_str = fd.read().decode('utf-8')
#         oracle = ast.literal_eval(oracle_str)
#     def decider(product_name, keywords):
#         # keywords = [{"name": "яйца", "portion": 3}, {"name": "мюсли", "portion": 75}]
#         for i in range(len(keywords)):
#             elem = keywords[i]
#             if (' ' + elem['name'].lower() in product_name.lower()) or \
#             (elem['name'].lower() in product_name.lower() and product_name.lower().find(elem['name'].lower()) == 0):
#                 return elem['portion']
#         return None

#     menu = {
#         "breakfast":{
#             "main": [],
#             "drink": []
#         },
#         "dinch": {
#             "main": [],
#             "drink": [],
#             "meat": [],
#             "garnish": []
#         },
#         "fruits": [],
#         "vegetables": [],
#         "snacks": []
#     }
#     for elem in products['offer']:
#         decider_result = decider(elem['name'], oracle['breakfast']['main'])
#         if decider_result is not None:
#             elem['portion'] = decider_result
#             elem['portions_count'] = int(elem['amount']/decider_result) if elem['amount']/decider_result < max_portions else max_portions
#             try:
#                 elem['portion_price'] = elem['priceAfter'] / elem['portions_count']
#             except:
#                 pass
#             else:
#                 menu['breakfast']['main'].append(elem.copy())
#         decider_result = decider(elem['name'], oracle['breakfast']['drink'])
#         if decider_result is not None:
#             elem['portion'] = decider_result
#             elem['portions_count'] = int(elem['amount']/decider_result) if elem['amount']/decider_result < max_portions else max_portions
#             try:
#                 elem['portion_price'] = elem['priceAfter'] / elem['portions_count']
#             except:
#                 pass
#             else:
#                 menu['breakfast']['drink'].append(elem.copy())
#         decider_result = decider(elem['name'], oracle['dinch']['main'])
#         if decider_result is not None:
#             elem['portion'] = decider_result
#             elem['portions_count'] = int(elem['amount']/decider_result) if elem['amount']/decider_result < max_portions else max_portions
#             try:
#                 elem['portion_price'] = elem['priceAfter'] / elem['portions_count']
#             except:
#                 pass
#             else:
#                 menu['dinch']['main'].append(elem.copy())
#         decider_result = decider(elem['name'], oracle['dinch']['drink'])
#         if decider_result is not None:
#             elem['portion'] = decider_result
#             elem['portions_count'] = int(elem['amount']/decider_result) if elem['amount']/decider_result < max_portions else max_portions
#             try:
#                 elem['portion_price'] = elem['priceAfter'] / elem['portions_count']
#             except:
#                 pass
#             else:
#                 menu['dinch']['drink'].append(elem.copy())
#         decider_result = decider(elem['name'], oracle['dinch']['meat'])
#         if decider_result is not None:
#             elem['portion'] = decider_result
#             elem['portions_count'] = int(elem['amount']/decider_result) if elem['amount']/decider_result < max_portions else max_portions
#             try:
#                 elem['portion_price'] = elem['priceAfter'] / elem['portions_count']
#             except:
#                 pass
#             else:
#                 menu['dinch']['meat'].append(elem.copy())
#         decider_result = decider(elem['name'], oracle['dinch']['garnish'])
#         if decider_result is not None:
#             elem['portion'] = decider_result
#             elem['portions_count'] = int(elem['amount']/decider_result) if elem['amount']/decider_result < max_portions else max_portions
#             try:
#                 elem['portion_price'] = elem['priceAfter'] / elem['portions_count']
#             except:
#                 pass
#             else:
#                 menu['dinch']['garnish'].append(elem.copy())
#         decider_result = decider(elem['name'], oracle['fruits'])
#         if decider_result is not None:
#             elem['portion'] = decider_result
#             elem['portions_count'] = int(elem['amount']/decider_result) if elem['amount']/decider_result < max_portions else max_portions
#             try:
#                 elem['portion_price'] = elem['priceAfter'] / elem['portions_count']
#             except:
#                 pass
#             else:
#                 menu['fruits'].append(elem.copy())
#         decider_result = decider(elem['name'], oracle['vegetables'])
#         if decider_result is not None:
#             elem['portion'] = decider_result
#             elem['portions_count'] = int(elem['amount']/decider_result) if elem['amount']/decider_result < max_portions else max_portions
#             try:
#                 elem['portion_price'] = elem['priceAfter'] / elem['portions_count']
#             except:
#                 pass
#             else:
#                 menu['vegetables'].append(elem.copy())
#         decider_result = decider(elem['name'], oracle['snacks'])
#         if decider_result is not None:
#             elem['portion'] = decider_result
#             elem['portions_count'] = int(elem['amount']/decider_result) if elem['amount']/decider_result < max_portions else max_portions
#             try:
#                 elem['portion_price'] = elem['priceAfter'] / elem['portions_count']
#             except:
#                 pass
#             else:
#                 menu['snacks'].append(elem.copy())
    
#     return generate(prices, days_number, menu)



# def generate(prices: dict, days: int, menu: dict):
#     products_to_buy = []
#     generated = {
#         "breakfast":{
#             "main": [],
#             "drink": []
#         },
#         "lunch": {
#             "main": [],
#             "drink": [],
#             "meat": [],
#             "garnish": []
#         },
#         "dinner": {
#             "main": [],
#             "drink": [],
#             "meat": [],
#             "garnish": []
#         },
#         "fruits": [],
#         "vegetables": [],
#         "snacks": []
#     }
#     total_money_leftover = 0

    
#     breakfast_names, breakfast_to_buy, money_leftover = generate_meals(prices['breakfast'], menu['breakfast']['main'], days)
#     if len(breakfast_names) < days:
#         return None, None, None
#     products_to_buy += breakfast_to_buy
#     generated['breakfast']['main'] = breakfast_names
#     total_money_leftover += money_leftover

#     lunch_meat_names, lunch_meat_to_buy, money_leftover = generate_meals(prices['lunch'] * 0.7, menu['dinch']['meat'], days)
#     generated['lunch']['meat'] = lunch_meat_names
#     products_to_buy += lunch_meat_to_buy
#     total_money_leftover += money_leftover
    
#     lunch_garnish_names, lunch_garnish_to_buy, money_leftover = generate_meals(prices['lunch'] * 0.3, menu['dinch']['garnish'], len(lunch_meat_names))
#     generated['lunch']['garnish'] = lunch_garnish_names
#     products_to_buy += lunch_garnish_to_buy
#     total_money_leftover = money_leftover

#     if len(lunch_meat_names) < days: 
#         lunch_main_names, lunch_main_to_buy, money_leftover = generate_backup(total_money_leftover , menu['dinch']['main'], days - len(lunch_meat_names))

#         if lunch_main_names == None:
#             return None, None, None
#         generated['lunch']['main'] = lunch_main_names
#         products_to_buy += lunch_main_to_buy
#         total_money_leftover += money_leftover
    
#     dinner_meat_names, dinner_meat_to_buy, money_leftover = generate_meals(prices['dinner'] * 0.7, menu['dinch']['meat'], days)
#     generated['dinner']['meat'] = dinner_meat_names
#     products_to_buy += dinner_meat_to_buy
#     total_money_leftover += money_leftover
    
#     dinner_garnish_names, dinner_garnish_to_buy, money_leftover = generate_meals(prices['dinner'] * 0.3, menu['dinch']['garnish'], len(dinner_meat_names))
#     generated['dinner']['garnish'] = dinner_garnish_names
#     products_to_buy += dinner_garnish_to_buy
#     total_money_leftover += money_leftover

#     if len(dinner_meat_names) < days: 
#         dinner_main_names, dinner_main_to_buy, money_leftover = generate_backup(total_money_leftover , menu['dinch']['main'], days - len(dinner_meat_names))
#         if dinner_main_names == None:
#             return None, None, None
#         generated['dinner']['main'] = dinner_main_names
#         products_to_buy += dinner_main_to_buy
#         total_money_leftover = money_leftover

#     vegetables_names, vegetables_to_buy, money_leftover = generate_addition(total_money_leftover, menu['vegetables'], days)
#     generated['vegetables'] = vegetables_names
#     products_to_buy += vegetables_to_buy
#     total_money_leftover = money_leftover

#     fruits_names, fruits_to_buy, money_leftover = generate_addition(total_money_leftover, menu['fruits'], days)
#     generated['fruits'] = fruits_names
#     products_to_buy += fruits_to_buy
#     total_money_leftover = money_leftover

#     snacks_names, snacks_to_buy, money_leftover = generate_addition(total_money_leftover, menu['snacks'], days)
#     generated['snacks'] = snacks_names
#     products_to_buy += snacks_to_buy
#     total_money_leftover = money_leftover


#     return generated, products_to_buy, money_leftover
    
    
# def generate_backup(money: int, menu_item: list, days_count: int):
#     good_choices = []
#     for _ in range(days_count):
#         good_choice = min(menu_item, key=lambda x:x['priceAfter'])
#         good_choices.append(good_choice)
#         menu_item.remove(good_choice)
#     if good_choices[0]['priceAfter'] * days_count > money:
#         return None, None, None
#     while True:
#         if sum([x['priceAfter'] for x in good_choices]) > money:
#             most_expensive = max(good_choices, key=lambda x:x['priceAfter'])
#             for _ in range(good_choices.count(most_expensive)):
#                 good_choices.remove(most_expensive)
#             most_expensive = max(good_choices, key=lambda x:x['priceAfter'])
#             for _ in range(days_count - len(good_choices)):
#                 good_choices.append(most_expensive)
#         else:
#             money_leftover = money - sum([x['priceAfter'] for x in good_choices])
#             return [x["name"] for x in good_choices], good_choices, money_leftover
    

# def generate_meals(money: int, menu_item: list, days_count: int):
#     if len(menu_item) / 3 < 100:
#         sample_size = int(len(menu_item)/3)
#     else:
#         sample_size = 100
#     result_names = []
#     result_to_buy = []
#     days_done = 0
#     money_leftover = money
#     avg_money = money/days_count
#     while days_done < days_count:
#         chosen_products = random.sample(menu_item, sample_size)
#         closest_elem = min(chosen_products, key=lambda x:abs(x['portion_price']-avg_money))
#         attempts = 0

#         while closest_elem['priceAfter'] > money_leftover and attempts < 20:
#             chosen_products = random.sample(menu_item, sample_size)
#             closest_elem = min(chosen_products, key=lambda x:abs(x['portion_price']-avg_money))
#             attempts += 1
        
#         if attempts == 20:
#             return result_names, result_to_buy, money_leftover
#         result_to_buy.append(closest_elem)
#         result_names += [closest_elem['name'] for _ in range(int(closest_elem['portions_count']) if int(closest_elem['portions_count']) <= days_count - days_done else days_count - days_done)]
#         days_done += int(closest_elem['portions_count'])
#         money_leftover -= closest_elem['priceAfter']
#         avg_money = money_leftover/days_count - days_done
#     return result_names, result_to_buy, money_leftover


# def generate_addition(money: int, menu_item: list, max_days_count: int):
#     result_names = []
#     result_to_buy = []
#     days_done = 0
#     money_leftover = money
#     attempts = 0
#     while days_done <= max_days_count and attempts < 200:
#         chosen_product = random.choice(menu_item)
#         if chosen_product['priceAfter'] > money:
#             attempts += 1
#             continue

#         result_to_buy.append(chosen_product)
#         result_names += [chosen_product['name'] for _ in range(int(chosen_product['portions_count']))]
#         days_done += chosen_product['portions_count']
#         money_leftover -= chosen_product['priceAfter']

#     return result_names, result_to_buy, money_leftover
