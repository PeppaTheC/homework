import functools


def wraps(func):
    def save_origin(wrapper):
        wrapper.__doc__ = func.__doc__
        wrapper.__name__ = func.__name__
        wrapper.__original_func = func
        return wrapper

    return save_origin


def print_result(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        """Function-wrapper which print result of an original function"""
        result = func(*args, **kwargs)
        print(result)
        return result

    return wrapper


@print_result
def custom_sum(*args):
    """This function can sum any objects which have __add___"""
    return functools.reduce(lambda x, y: x + y, args)


if __name__ == '__main__':
    custom_sum([1, 2, 3], [4, 5])
    custom_sum(1, 2, 3, 4)

    print(custom_sum.__doc__)
    print(custom_sum.__name__)
    print(custom_sum.__original_func)
    without_print = custom_sum.__original_func

    # the result returns without printing
    without_print(1, 2, 3, 4)
