from collections import OrderedDict
from inspect import signature
from functools import wraps
import requests
from time import monotonic


def make_cache(timing):
    def my_decorator(func):
        cache = OrderedDict()

        @wraps(func)
        def wrapper(*args, **kwargs):
            a = signature(func).bind(*args, **kwargs)
            a.apply_defaults()
            a = str(a)
            elapsed = monotonic() - timing
            for key in list(cache.keys()):
                if cache[key][1] < elapsed:
                    cache.popitem(False)
                else:
                    break
            if a not in cache:
                result = func(*args, **kwargs)
                cache[a] = (result, monotonic())
            else:
                result = cache[a][0]
            return result

        return wrapper

    return my_decorator


def city_temperature(city: str = 'Saint Petersburg'):
    api_url = "http://api.openweathermap.org/data/2.5/weather"
    parameters = {'q': city,
                  'appid': '11c0d3dc6093f7442898ee49d2430d20',
                  'units': 'metric'}
    res = requests.get(api_url, params=parameters)
    data = res.json()
    return f"Current temperature in {city} is {data['main']['temp']}°С"


slow_function = make_cache(3600)(city_temperature)  # updates temperature  only once in hour
print(city_temperature(), slow_function(), sep='\n')
