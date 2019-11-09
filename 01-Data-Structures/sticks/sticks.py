from collections import Counter


def object_to_json_string(data) -> str:
    """Функция конвертирует данные в json строку"""
    if data is None:
        return 'null'
    elif data is True:
        return 'true'
    elif data is False:
        return 'false'
    elif isinstance(data, int) or isinstance(data, float):
        return f'{data}'
    elif isinstance(data, str):
        return f'"{data}"'
    elif isinstance(data, list):
        string = ''
        for obj in data:
            string += f'{object_to_json_string(obj)}, '
        string = string[:-2]
        return f'[{string}]'
    elif isinstance(data, dict):
        string = ''
        for key, value in data.items():
            string += f'{object_to_json_string(key)}: {object_to_json_string(value)}, '
        string = string[:-2]
        return "{%s}" % string


def json_dump(data, file):
    """Функция записывает данные в файл в
        формате json строки"""
    string = object_to_json_string(data)
    file.write(string)


def parse_array(string: str, index: int) -> (list, int):
    """Функция преобразует массив cтроки json в
        в python список"""
    global parse_object
    array = []
    while string[index] != ']':
        if string[index] == '[':
            value, index = parse_array(string, index + 1)
            array.append(value)
        elif string[index] == '{':
            value, index = parse_object(string, index + 1)
            array.append(value)
        elif string[index] == '"':
            read_word(string, index + 1)
        else:
            index += 1
    return array, index + 1


def parse_object(string: str, index: int) -> (dict, int):
    """Функция преобразует словарь cтроки json в
        в python словарь"""
    global parse_array
    json_object = {}
    while string[index] != '}':
        index = pass_spacing(string, index)
        name, index = read_word(string, index + 1)
        index += 1
        if string[index] == ':':
            index = pass_spacing(string, index + 1)
            if string[index] == '{':
                value, index = parse_object(string, index + 1)
            elif string[index] == '[':
                value, index = parse_array(string, index + 1)
            else:
                value, index = parse_data(string, index)
                index += 1
            json_object.update({name: value})
        if string[index] == ',':
            index += 1
    return json_object, index + 1


def parse_data(string: str, index: int):
    """Функция конвертируте данные json в
    струкруры данные в python"""
    nextchar = string[index]
    if nextchar == '"':
        return read_word(string, index + 1)
    elif nextchar == 'n' and string[index:index + 4] == 'null':
        return None, index + 4
    elif nextchar == 't' and string[index:index + 4] == 'true':
        return True, index + 4
    elif nextchar == 'f' and string[index:index + 5] == 'false':
        return False, index + 5
    else:
        return parse_number(string, index)


def parse_number(string: str, index: int):
    """Функция конвертирует числа json
    в числа python"""
    word = ''
    symbols_of_float = '.,Ee'
    while string[index] != ',' and string[index] != '}':
        word += string[index]
        index += 1
    if set(word) & set(symbols_of_float):
        return float(word), index
    else:
        return int(word), index


def read_word(string: str, index: int):
    """Функция читает слово json"""
    word = ''
    while string[index] != '"':
        word += string[index]
        index += 1
    if word.isdigit():
        word = int(word)
    return word, index


def pass_spacing(string: str, index: int) -> int:
    """Функция перемещает указатель с отступов"""
    while string[index] == ' ' or string[index] == '\n':
        index += 1
    return index


def json_loads(file):
    """Функция за счтитывает json данные из файла,
     затем с помощью указателя переводит в струкруты
     данных python (время работы O(n))
     """
    string = file.read()
    index = 0
    next_char = string[index]
    if next_char == '[':
        json_item, _ = parse_array(string, index + 1)
    elif next_char == '{':
        json_item, _ = parse_object(string, index + 1)
    else:
        json_item = None
    return json_item


def merge_two_lists(list1: list, list2: list) -> list:
    """Функция сливает два списка без повторений"""
    sum = list1 + list2
    set_of_values = set()
    merged_list = []
    for item in sum:
        value = tuple(item.values())
        if value not in set_of_values:
            merged_list.append(item)
            set_of_values.add(value)
    return sum


def find_max(array: Counter, max: bool = True):
    """Функция возвращает максимальные занчения в массиве
    или последовательность с максимальными занчения"""
    if max:
        max = array.most_common(1)[0][1]
        max_items = [item for item in array if array[item] == max]
        return max_items if len(max_items) > 1 else max_items[0]
    else:
        min = array.most_common()[-1][1]
        min_items = [item for item in array if array[item] == min]
        return min_items if len(min_items) > 1 else min_items[0]


with open('winedata_1.json', 'r') as json_file:
    wine_data_1 = json_loads(json_file)

print("done_1")

with open('winedata_2.json', 'r') as json_file:
    wine_data_2 = json_loads(json_file)

print("done_2")
wine_data_full = merge_two_lists(wine_data_1, wine_data_2)
wine_data_full.sort(key=lambda obj: (-obj['price'] if obj['price'] else 0, obj['variety'] if obj['variety'] else ''))

with open('winedata_full.json', 'w') as json_file:
    json_dump(wine_data_full, json_file)

print("done_3")
varieties_list = [r"Gew\u00fcrztraminer", "Riesling", "Merlot", "Madera", "Tempranillo", "Red Blend"]

statistics = {variety: {"average_price": [], "min_price": float('inf'), "max_price": -1,
                        "most_common_region": Counter(), "most_common_country": Counter(),
                        "average_score": []} for variety in varieties_list}

score_counter = Counter()
price_counter = Counter()
country_price = {}
country_score = {}
comments_counter = Counter()

for item in wine_data_full:
    current_price = item.get('price')
    title = item.get('title')
    current_score = item.get('points')
    country = item.get('country')
    taster_name = item.get('taster_name')
    variety = item.get('variety')

    if current_price:
        price_counter[title] = current_price

    if current_score:
        score_counter[title] = current_score

    if taster_name:
        comments_counter.setdefault(taster_name, 1)
        comments_counter[taster_name] += 1

    if country:
        if current_score:
            country_score.setdefault(country, [])
            country_score[country].append(current_score)

        if current_price:
            country_price.setdefault(country, [])
            country_price[country].append(current_price)

    if variety in varieties_list:
        points = item.get("points")
        region_1 = item.get("region_1")
        region_2 = item.get("region_2")

        if current_price:
            statistics[variety]['average_price'].append(current_price)
            statistics[variety]['min_price'] = min(statistics[variety]['min_price'], current_price)
            statistics[variety]['max_price'] = max(statistics[variety]['max_price'], current_price)

        if current_score:
            statistics[variety]['average_score'].append(current_score)

        if country:
            statistics[variety]['most_common_country'].setdefault(country, 1)
            statistics[variety]['most_common_country'][country] += 1

        if region_1:
            statistics[variety]['most_common_region'].setdefault(region_1, 1)
            statistics[variety]['most_common_region'][region_1] += 1

        if region_2:
            statistics[variety]['most_common_region'].setdefault(region_2, 1)
            statistics[variety]['most_common_region'][region_2] += 1

print("done_4")
for variety in varieties_list:
    if statistics[variety]['average_price']:
        statistics[variety]['average_price'] = round(sum(statistics[variety]['average_price'])
                                                     / len(statistics[variety]['average_price']), 2)
    if statistics[variety]['average_score']:
        statistics[variety]['average_score'] = round(sum(statistics[variety]['average_score'])
                                                     / len(statistics[variety]['average_score']), 2)
    if statistics[variety]['most_common_country']:
        statistics[variety]['most_common_country'] = statistics[variety]['most_common_country'].most_common(1)[0][0]
    if statistics[variety]['most_common_region']:
        statistics[variety]['most_common_region'] = statistics[variety]['most_common_region'].most_common(1)[0][0]

print("done_5")
country_price_counter = Counter({key: round(sum(value) / max(len(value), 2)) for key, value in country_price.items()})
country_score_counter = Counter({key: round(sum(value) / max(len(value), 2)) for key, value in country_score.items()})

common_statistics = {'most_expensive_wine': find_max(price_counter),
                     'cheapest_wine': find_max(price_counter, False),
                     'highest_score': find_max(score_counter),
                     'lowest_score': find_max(score_counter, False),
                     'most_expensive_country': find_max(country_price_counter),
                     'cheapest_country': find_max(country_price_counter, False),
                     'most_rated_country': find_max(country_score_counter),
                     'underrated_country': find_max(country_score_counter, False),
                     'most_active_commentator': find_max(comments_counter)}

statistics.update(common_statistics)
stats = {'statistics': statistics}

with open('stats.json', 'w') as json_file:
    json_dump(stats, json_file)
