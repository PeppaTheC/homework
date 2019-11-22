def square(func):
    print(1)
    return lambda x: func(x * x)


def addsome(func):
    print(2)
    return lambda x: func(x + 10)


@square
@addsome
def foo(x):
    return x


print(foo(2))
