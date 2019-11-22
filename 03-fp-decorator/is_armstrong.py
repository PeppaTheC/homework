from functools import reduce


def is_armstrong(number):
    return reduce(lambda a, b: a + b, [pow(i, len(str(number))) for i in list(map(int, str(number)))]) == number


def test():
    assert is_armstrong(153) is True, 'Число Армстронга'
    assert is_armstrong(10) is False, 'Не число Армстронга'


if __name__ == '__main__':
    test()
