"""
Представьте, что вы пишите программу по формированию и выдачи комплексных обедов для сети столовых, которая стала
расширяться и теперь предлагает комплексные обеды для вегетарианцев, детей и любителей китайской кухни.

С помощью паттерна "Абстрактная фабрика" вам необходимо реализовать выдачу комплексного обеда, состоящего из трёх
позиций (первое, второе и напиток).
В файле menu.yml находится меню на каждый день, в котором указаны позиции и их принадлежность к
определенному типу блюд.

"""
from abc import ABC, abstractmethod
import yaml

with open('menu.yml', encoding='utf-8') as f:
    menu = yaml.load(f, Loader=yaml.FullLoader)


class AbstractFood(ABC):
    """Abstract product class"""
    def __init__(self, name):
        self._name = name

    def __str__(self):
        return self._name


class FirstCourse(AbstractFood):
    """Lunch first course meal"""
    pass


class SecondCourse(AbstractFood):
    """Lunch second course meal"""
    pass


class Drink(AbstractFood):
    """Lunch drink"""
    pass


class AbstractLunch(ABC):

    @abstractmethod
    def create_lunch(self, day: str) -> dict:
        pass


class VeganLunch(AbstractLunch):
    """Vegan lunch factory by day"""
    def create_lunch(self, day) -> dict:
        first_course = FirstCourse(menu[day]['first_courses']['vegan'])
        second_course = SecondCourse(menu[day]['second_courses']['vegan'])
        drink = Drink(menu[day]['drinks']['vegan'])
        print(f"Vegan {day.lower()}  lunch is: "
              f"first course is {first_course}, "
              f"second course is {second_course} and "
              f"drink is  {drink}")
        return {'first_course': first_course, 'second_course': second_course, 'drink': drink}


class ChildLunch(AbstractLunch):
    """Child lunch factory by day"""
    def create_lunch(self, day) -> dict:
        first_course = FirstCourse(menu[day]['first_courses']['child'])
        print(first_course)
        second_course = SecondCourse(menu[day]['second_courses']['child'])
        drink = Drink(menu[day]['drinks']['child'])
        print(f"Child {day.lower()} lunch is: "
              f"first course is {first_course}, "
              f"second course is {second_course} and "
              f"drink is  {drink}")
        return {'first_course': first_course, 'second_course': second_course, 'drink': drink}


class ChinaLunch(AbstractLunch):
    """Chinese lunch factory by day"""
    def create_lunch(self, day) -> dict:
        first_course = FirstCourse(menu[day]['first_courses']['china'])
        second_course = SecondCourse(menu[day]['second_courses']['china'])
        drink = Drink(menu[day]['drinks']['china'])
        print(f"China {day.lower()}  lunch is: "
              f"first course is {first_course}, "
              f"second course is {second_course} and "
              f"drink is  {drink}")
        return {'first_course': first_course, 'second_course': second_course, 'drink': drink}


def client_code(lunch_factory: AbstractLunch, day: str) -> None:
    product_a = lunch_factory.create_lunch(day)


if __name__ == '__main__':
    client_code(ChildLunch(), 'Saturday')
