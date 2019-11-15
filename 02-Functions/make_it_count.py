def make_it_count(func, counter_name: str):
    def wrapper(*args, **kwargs):
        if wrapper.__module__ == '__main__':
            wrapper.__globals__[counter_name] += 1
        return func(*args, **kwargs)

    return wrapper


def test():
    new_pow = make_it_count(pow, 'count')
    for i in range(100):
        assert i == count
        assert new_pow(i, 2) == pow(i, 2)


if __name__ == '__main__':
    count = 0
    test()
