"""
С помощью паттерна "Цепочка обязанностей" составьте список покупок для выпечки блинов.
Необходимо осмотреть холодильник и поочередно проверить, есть ли у нас необходимые ингридиенты:
    2 яйца
    300 грамм муки
    0.5 л молока
    100 грамм сахара
    10 мл подсолнечного масла
    120 грамм сливочного масла

В итоге мы должны получить список недостающих ингридиентов.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass


class Handler(ABC):
    """
    The Handler interface declares a method for building a handler chain.
    """

    @abstractmethod
    def set_next(self, handler):
        pass

    @abstractmethod
    def handle(self, request):
        pass


class AbstractHandler(Handler):
    """
    The behavior of the chain by default.
    """

    _next_handler: Handler = None

    def set_next(self, handler: Handler) -> Handler:
        self._next_handler = handler
        # Возврат обработчика отсюда позволит связать обработчики простым
        # способом, вот так:
        # handler1.set_next(handler2).set_next(handler3)
        return handler

    @abstractmethod
    def handle(self, request):
        if self._next_handler:
            return self._next_handler.handle(request)
        return None


INGREDIENTS = {'eggs': 2,
               'flour': 300,
               'milk': 0.5,
               'sugar': 100,
               'sunflower oil': 10,
               'butter': 120,
               }

shopping_list = []


@dataclass()
class Fridge:
    """Fridge contains products"""
    eggs: int = 0
    flour: int = 310
    milk: float = 0.3
    sugar: int = 120
    sunflower_oil: int = 30
    butter: int = 2


class EggsHandler(AbstractHandler):
    def handle(self, fridge: Fridge):
        if fridge.eggs < INGREDIENTS['eggs']:
            lack_of_eggs = INGREDIENTS['eggs'] - fridge.eggs
            shopping_list.append(f"eggs: {lack_of_eggs}")
            print(f"Необходимо купить яиц: {lack_of_eggs}")
        if self._next_handler:
            return self._next_handler.handle(fridge)


class FlourHandler(AbstractHandler):
    def handle(self, fridge: Fridge):
        if fridge.flour < INGREDIENTS['flour']:
            lack_of_flour = INGREDIENTS['flour'] - fridge.flour
            shopping_list.append(f"flour: {lack_of_flour}")
            print('ЧТО МУКА ДЕЛАЕТ В ХОЛОДИЛЬНИКЕ?!')
            print(f"Необходимо купить муки: {lack_of_flour}")
        if self._next_handler:
            return self._next_handler.handle(fridge)


class MilkHandler(AbstractHandler):
    def handle(self, fridge: Fridge):
        if fridge.milk < INGREDIENTS['milk']:
            lack_of_milk = INGREDIENTS['milk'] - fridge.milk
            shopping_list.append(f"milk: {lack_of_milk}")
            print(f"Необходимо купить молока: {lack_of_milk}")
        if self._next_handler:
            return self._next_handler.handle(fridge)


class SugarHandler(AbstractHandler):
    def handle(self, fridge: Fridge):
        if fridge.sugar < INGREDIENTS['sugar']:
            lack_of_sugar = INGREDIENTS['sugar'] - fridge.sugar
            shopping_list.append(f"sugar: {lack_of_sugar}")
            print(f"Необходимо купить сахара: {lack_of_sugar}")
        if self._next_handler:
            return self._next_handler.handle(fridge)


class SunflowerOilHandler(AbstractHandler):
    def handle(self, fridge: Fridge):
        if fridge.sunflower_oil < INGREDIENTS['sunflower oil']:
            lack_of_sunflower_oil = INGREDIENTS['sunflower oil'] - fridge.sunflower_oil
            shopping_list.append(f"sunflower oil: {lack_of_sunflower_oil}")
            print(f"Необходимо купить подсолнечного масла: {lack_of_sunflower_oil}")
        if self._next_handler:
            return self._next_handler.handle(fridge)


class ButterHandler(AbstractHandler):
    def handle(self, fridge: Fridge):
        if fridge.butter < INGREDIENTS['butter']:
            lack_of_butter = INGREDIENTS['butter'] - fridge.butter
            shopping_list.append(f"butter: {lack_of_butter}")
            print(f"Необходимо купить сливочного масла: {lack_of_butter}")
        if self._next_handler:
            return self._next_handler.handle(fridge)


def check_fridge(fridge):
    eggs_handler = EggsHandler()
    flour_handler = FlourHandler()
    milk_handler = MilkHandler()
    sugar_handler = SugarHandler()
    sunflower_oil_handler = SunflowerOilHandler()
    butter_handler = ButterHandler()

    eggs_handler.set_next(flour_handler).set_next(milk_handler) \
        .set_next(sugar_handler).set_next(sunflower_oil_handler).set_next(butter_handler)

    eggs_handler.handle(fridge)


if __name__ == '__main__':
    fridge_to_check = Fridge(sunflower_oil=2)
    check_fridge(fridge_to_check)
