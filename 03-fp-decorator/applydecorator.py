from functools import wraps


def applydecorator(decorator):
    def new_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return decorator(func, *args, **kwargs)

        return wrapper

    return new_decorator


@applydecorator
def saymyname(f, *args, **kwargs):
    print('Name is', f.__name__)
    return f(*args, **kwargs)


@saymyname
def foo(*whatever):
    return whatever


if __name__ == '__main__':
    print(*(foo(40, 2)))
