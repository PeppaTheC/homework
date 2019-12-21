"""
Используя паттерн "Декоратор" реализуйте возможность дополнительно добавлять к кофе
    маршмеллоу, взбитые сливки и сироп, а затем вычислить итоговую стоимость напитка.
"""


class Component:
    def get_cost(self):
        raise NotImplementedError("Override get_cost method")


class BaseCoffee(Component):
    def get_cost(self):
        return 90


class AbstractCoffeeDecorator(BaseCoffee):
    def __init__(self, decorated_coffee):
        self.decorated_coffee = decorated_coffee

    def get_cost(self):
        return self.decorated_coffee.get_cost()


class Whip(AbstractCoffeeDecorator):
    def __init__(self, decorated_coffee):
        super(Whip, self).__init__(decorated_coffee)

    def get_cost(self):
        return self.decorated_coffee.get_cost() + 5


class Marshmallow(AbstractCoffeeDecorator):
    def __init__(self, decorated_coffee):
        super(Marshmallow, self).__init__(decorated_coffee)

    def get_cost(self):
        return self.decorated_coffee.get_cost() + 10


class Syrup(AbstractCoffeeDecorator):
    def __init__(self, decorated_coffee):
        super(Syrup, self).__init__(decorated_coffee)

    def get_cost(self):
        return self.decorated_coffee.get_cost() + 15


if __name__ == "__main__":
    coffee = BaseCoffee()
    coffee = Whip(coffee)
    coffee = Marshmallow(coffee)
    coffee = Syrup(coffee)
    print("Итоговая стоимость за кофе: {}".format(str(coffee.get_cost())))
