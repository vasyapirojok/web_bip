import random
import ast


def offer_to_menu(products, days_number):
    max_portions = days_number / 2
    menu = {
        "breakfast":{
            "main": [],
            "drink": []
        },
        "dinch": {
            "main": [],
            "drink": [],
            "meat": [],
            "garnish": []
        },
        "fruits": [],
        "vegetables": [],
        "snacks": []
    }
    with open('oracle.json', 'rb') as fd:
        oracle_str = fd.read().decode('utf-8')
        oracle = ast.literal_eval(oracle_str)
    def decider(product_name, keywords):
        # keywords = [{"name": "яйца", "portion": 3}, {"name": "мюсли", "portion": 75}]
        for i in range(len(keywords)):
            elem = keywords[i]
            if (' ' + elem['name'].lower() in product_name.lower()) or \
            (elem['name'].lower() in product_name.lower() and product_name.lower().find(elem['name'].lower()) == 0):
                if "fake" in list(elem.keys()):
                    for fake_keyword in elem["fake"]:
                        if fake_keyword.lower() not in elem["name"].lower():
                            return elem['portion']
                else:
                    return elem['portion']
        return None
    
    def generate_menu_elem(elem, decider_result, max_portions):
        elem['portion'] = decider_result
        elem['portions_count'] = int(elem['amount']/decider_result) if elem['amount']/decider_result < max_portions else max_portions
        try:
            elem['portion_price'] = elem['priceAfter'] / elem['portions_count']
        except:
            return None
        else:
           return elem
    
    types_of_meals = [('breakfast', 'main'), ('breakfast', 'drink'),
                     ('dinch', 'main'), ('dinch', 'drink'), ('dinch', 'meat'),
                     ('dinch', 'garnish'), ('fruits'), ('vegetables'), ('snacks')]
    for elem in products:
        for type_of_meal in types_of_meals:
            if len(type_of_meal) == 2:
                decider_result = decider(elem['name'], oracle[type_of_meal[0]][type_of_meal[1]])
                if decider_result is not None:
                    menu_item = generate_menu_elem(elem, decider_result, max_portions)
                    if menu_item is not None:
                        menu[type_of_meal[0]][type_of_meal[1]].append(menu_item.copy())
            else:
                # try:
                decider_result = decider(elem['name'], oracle[type_of_meal])
                # except:
                #     a = type_of_meal[0]
                #     print(a)
                if decider_result is not None:
                    menu_item = generate_menu_elem(elem, decider_result, max_portions)
                    if menu_item is not None:
                        menu[type_of_meal].append(menu_item.copy())
    return menu


def magic_ext(products, full_price, days_number):
    
    # price_per_day = full_price // days_number
    prices = {
        "breakfast": int((full_price) * 0.26),
        "lunch": int((full_price) * 0.37),
        "dinner": int((full_price) * 0.37)
    }
    
    if sum(list(prices.values())) > full_price:
        prices["dinner"] -= full_price - sum(list(prices.values()))
    
    menu = offer_to_menu(products, days_number)

    generated, products_to_buy, money_leftover = generate(prices, days_number, menu)

    if generated is None or products_to_buy is None or money_leftover is None:
        return None, None, None
    ration = {'breakfast': [], 'lunch': [], 'dinner': []}
    
    random.shuffle(generated['breakfast']['main'])
    ration['breakfast'] = [[elem] for elem in generated['breakfast']['main']]
    
    indexes = random.sample(range(days_number), len(generated['fruits']))
    for i in range(len(indexes)):
        ration['breakfast'][indexes[i]].append(generated['fruits'][i])

    random.shuffle(generated['lunch']['meat'])
    random.shuffle(generated['lunch']['garnish'])

    try:
        for i in range(len(generated['lunch']['meat'])):
            ration['lunch'].append([generated['lunch']['meat'][i], generated['lunch']['garnish'][i]])
    except:
        print('a')
    random.shuffle(generated['lunch']['main'])
    for elem in generated['lunch']['main']:
        ration['lunch'].append([elem])

    random.shuffle(ration['lunch'])

    
    random.shuffle(generated['dinner']['meat'])
    random.shuffle(generated['dinner']['garnish'])

    for i in range(len(generated['dinner']['meat'])):
        ration['dinner'].append([generated['dinner']['meat'][i], generated['dinner']['garnish'][i]])
    
    random.shuffle(generated['dinner']['main'])
    for elem in generated['dinner']['main']:
        ration['dinner'].append([elem])

    random.shuffle(ration['dinner'])

    
    indexes = random.sample(range(days_number), len(generated['vegetables']))
    for i in range(len(indexes)):
        ch = random.randint(0, 1)
        if ch == 0:
            ration['lunch'][indexes[i]].append(generated['vegetables'][i])
        else:
            ration['dinner'][indexes[i]].append(generated['vegetables'][i])
    
    indexes = random.sample(range(days_number), len(generated['snacks']))
    for i in range(len(indexes)):
        ch = random.randint(0, 1)
        if ch == 0:
            ration['lunch'][indexes[i]].append(generated['snacks'][i])
        else:
            ration['dinner'][indexes[i]].append(generated['snacks'][i])
            
    
    
    return ration, products_to_buy, money_leftover



def generate(prices: dict, days: int, menu: dict):
    products_to_buy = []
    generated = {
        "breakfast":{
            "main": [],
            "drink": []
        },
        "lunch": {
            "main": [],
            "drink": [],
            "meat": [],
            "garnish": []
        },
        "dinner": {
            "main": [],
            "drink": [],
            "meat": [],
            "garnish": []
        },
        "fruits": [],
        "vegetables": [],
        "snacks": []
    }
    total_money_leftover = 0

    
    breakfast_names, breakfast_to_buy, money_leftover = generate_meals(prices['breakfast'], menu['breakfast']['main'], days)
    if len(breakfast_names) < days:
        return None, None, None
    products_to_buy += breakfast_to_buy
    generated['breakfast']['main'] = breakfast_names
    total_money_leftover += money_leftover

    lunch_meat_names, lunch_meat_to_buy, money_leftover = generate_meals(prices['lunch'] * 0.7, menu['dinch']['meat'], days)

    total_money_leftover += money_leftover
    
    lunch_garnish_names, lunch_garnish_to_buy, money_leftover = generate_meals(prices['lunch'] * 0.3, menu['dinch']['garnish'], len(lunch_meat_names))
    generated['lunch']['garnish'] = lunch_garnish_names
    products_to_buy += lunch_garnish_to_buy
    total_money_leftover = money_leftover
    
    if len(lunch_garnish_names) < len(lunch_meat_names):
        lunch_meat_names = lunch_meat_names[:len(lunch_garnish_names)]
        new_lunch_meat_to_buy = []
        for elem in lunch_meat_to_buy:
            if elem['name'] not in lunch_garnish_names:
                total_money_leftover += elem['priceAfter']
            else:
                new_lunch_meat_to_buy.append(elem.copy())
        lunch_meat_to_buy = new_lunch_meat_to_buy

    generated['lunch']['meat'] = lunch_meat_names
    products_to_buy += lunch_meat_to_buy

    if len(lunch_meat_names) < days: 
        lunch_main_names, lunch_main_to_buy, money_leftover = generate_backup(total_money_leftover , menu['dinch']['main'], days - len(lunch_meat_names))
        if lunch_main_names == None:
            return None, None, None
        generated['lunch']['main'] = lunch_main_names
        products_to_buy += lunch_main_to_buy
        total_money_leftover += money_leftover
    
    dinner_meat_names, dinner_meat_to_buy, money_leftover = generate_meals(prices['dinner'] * 0.7, menu['dinch']['meat'], days)
    total_money_leftover += money_leftover
    
    dinner_garnish_names, dinner_garnish_to_buy, money_leftover = generate_meals(prices['dinner'] * 0.3, menu['dinch']['garnish'], len(dinner_meat_names))
    generated['dinner']['garnish'] = dinner_garnish_names
    products_to_buy += dinner_garnish_to_buy
    total_money_leftover += money_leftover

    if len(dinner_garnish_names) < len(dinner_meat_names):
        dinner_meat_names = dinner_meat_names[:len(dinner_garnish_names)]
        new_dinner_meat_to_buy = []
        for elem in dinner_meat_to_buy:
            if elem['name'] not in dinner_garnish_names:
                total_money_leftover += elem['priceAfter']
            else:
                new_dinner_meat_to_buy.append(elem.copy())
        dinner_meat_to_buy = new_dinner_meat_to_buy

    generated['dinner']['meat'] = dinner_meat_names
    products_to_buy += dinner_meat_to_buy

    if len(dinner_meat_names) < days: 
        dinner_main_names, dinner_main_to_buy, money_leftover = generate_backup(total_money_leftover , menu['dinch']['main'], days - len(dinner_meat_names))
        if dinner_main_names == None:
            return None, None, None
        generated['dinner']['main'] = dinner_main_names
        products_to_buy += dinner_main_to_buy
        total_money_leftover = money_leftover

    vegetables_names, vegetables_to_buy, money_leftover = generate_addition(total_money_leftover, menu['vegetables'], days)
    generated['vegetables'] = vegetables_names
    products_to_buy += vegetables_to_buy
    total_money_leftover = money_leftover

    fruits_names, fruits_to_buy, money_leftover = generate_addition(total_money_leftover, menu['fruits'], days)
    generated['fruits'] = fruits_names
    products_to_buy += fruits_to_buy
    total_money_leftover = money_leftover

    snacks_names, snacks_to_buy, money_leftover = generate_addition(total_money_leftover, menu['snacks'], days)
    generated['snacks'] = snacks_names
    products_to_buy += snacks_to_buy
    total_money_leftover = money_leftover


    return generated, products_to_buy, money_leftover
    
    
def generate_backup(money: int, menu_item: list, days_count: int):
    good_choices = []
    for _ in range(days_count):
        good_choice = min(menu_item, key=lambda x:x['priceAfter'])
        good_choices.append(good_choice)
        menu_item.remove(good_choice)
    if good_choices[0]['priceAfter'] * days_count > money:
        return None, None, None
    while True:
        if sum([x['priceAfter'] for x in good_choices]) > money:
            most_expensive = max(good_choices, key=lambda x:x['priceAfter'])
            for _ in range(good_choices.count(most_expensive)):
                good_choices.remove(most_expensive)
            most_expensive = max(good_choices, key=lambda x:x['priceAfter'])
            for _ in range(days_count - len(good_choices)):
                good_choices.append(most_expensive)
        else:
            money_leftover = money - sum([x['priceAfter'] for x in good_choices])
            return [x["name"] for x in good_choices], good_choices, money_leftover
    

def generate_meals(money: int, menu_item: list, days_count: int):
    if len(menu_item) / 3 < 100:
        sample_size = int(len(menu_item)/3)
    else:
        sample_size = 100
    result_names = []
    result_to_buy = []
    days_done = 0
    money_leftover = money
    avg_money = money/days_count
    while days_done < days_count:
        chosen_products = random.sample(menu_item, sample_size)
        closest_elem = min(chosen_products, key=lambda x:abs(x['portion_price']-avg_money))
        attempts = 0

        while closest_elem['priceAfter'] > money_leftover and attempts < 20:
            chosen_products = random.sample(menu_item, sample_size)
            closest_elem = min(chosen_products, key=lambda x:abs(x['portion_price']-avg_money))
            attempts += 1
        
        if attempts == 20:
            return result_names, result_to_buy, money_leftover
        result_to_buy.append(closest_elem)
        result_names += [closest_elem['name'] for _ in range(int(closest_elem['portions_count']) if int(closest_elem['portions_count']) <= days_count - days_done else days_count - days_done)]
        days_done += int(closest_elem['portions_count'])
        money_leftover -= closest_elem['priceAfter']
        avg_money = money_leftover/days_count - days_done
    return result_names, result_to_buy, money_leftover


def generate_addition(money: int, menu_item: list, max_days_count: int):
    result_names = []
    result_to_buy = []
    days_done = 0
    money_leftover = money
    attempts = 0
    while days_done < max_days_count and attempts < 200:
        chosen_product = random.choice(menu_item)
        if chosen_product['priceAfter'] > money_leftover:
            attempts += 1
            continue

        result_to_buy.append(chosen_product)
        result_names += [chosen_product['name'] for _ in range(int(chosen_product['portions_count']) if int(chosen_product['portions_count']) <= max_days_count - days_done else max_days_count - days_done)]
        days_done += int(chosen_product['portions_count'])
        money_leftover -= chosen_product['priceAfter']

    return result_names, result_to_buy, money_leftover
