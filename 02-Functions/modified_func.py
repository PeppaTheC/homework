import inspect


def modified_func(func, *fixated_args, **fixated_kwargs):
    def wrapper(*args, **kwargs):
        wrapper.__name__ = func.__name__
        try:
            code = inspect.getsource(func)
        except TypeError:
            code = "it is builtin_function"
        wrapper.__doc__ = f"""A func implementation of {wrapper.__name__}
            with pre-applied arguments being:
            {fixated_args} и {fixated_kwargs}
            source_code: {code}"""
        if not args and not kwargs:
            return func(*fixated_args, **fixated_kwargs)
        else:
            new_args = fixated_args[:]
            new_kwargs = fixated_kwargs.copy()
            if args:
                new_args = args + fixated_args
            if kwargs:
                new_kwargs.update(kwargs)
            return func(*new_args, **new_kwargs)

    return wrapper


def test():
    from make_it_count import make_it_count
    count = 0
    new_modified_func = make_it_count(modified_func, 'count')

    from letters_range import letters_range
    transliterations = {'l': 7, 'o': 0}
    letters_range_with_transliteration = new_modified_func(letters_range, **transliterations)
    letters_range_to_h = new_modified_func(letters_range, 'h')
    assert letters_range_with_transliteration('g', 'p') == ['g', 'h', 'i', 'j', 'k', '7', 'm', 'n', '0']
    assert letters_range_to_h() == ['a', 'b', 'c', 'd', 'e', 'f', 'g']

    from atom import atom
    get_x, set_x, process_x, delete_x = atom('Hello python')
    set_of_functions = [lambda x: x + 10 for _ in range(0, 4)]
    long_process_x = new_modified_func(process_x, *set_of_functions)
    set_x(10)
    assert long_process_x(lambda x: x // 2) == 45
    delete_x()

    # assert count == 0  # не разобрался, как менять пееременую в другом модуле с помощью декоратора

    min_less_100 = new_modified_func(min, 100)
    assert min_less_100(1010, 21321, 233) == 100
    assert min_less_100(31, 432, 100) == 31
    max_more_1000 = new_modified_func(max, 1000)
    assert max_more_1000(1010, 1021) == 1021
    assert max_more_1000(1, 2, 3, 4, 5) == 1000
    print(inspect.signature(any))  # in python 3.7 (iterable, /)

    print(f"name: {letters_range_with_transliteration.__name__}\ndoc: {letters_range_with_transliteration.__doc__}",
          f"name: {letters_range_to_h.__name__}\ndoc: {letters_range_to_h.__doc__}",
          f"name: {long_process_x.__name__}\ndoc: {long_process_x.__doc__}",
          f"name: {min_less_100.__name__}\ndoc: {min_less_100.__doc__}",
          f"name: {max_more_1000.__name__}\ndoc: {max_more_1000.__doc__}",
          sep='\n')


if __name__ == '__main__':
    test()
