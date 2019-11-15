def atom(x=None) -> tuple:
    """Function encapsulates the variable x and returns
        an interface to interact with it"""

    def get_value():
        """Return value x"""
        return x

    def set_value(new_value):
        """Set new value for x"""
        nonlocal x
        x = new_value
        return x

    def process_value(*functions):
        """Applies a sequence of functions to x"""
        nonlocal x
        for fun in functions:
            x = fun(x)
        return x

    def delete_value():
        """Delete x"""
        nonlocal x
        # del x
        x = None

    return get_value, set_value, process_value, delete_value


def test():
    get_x, set_x, process_x, delete_x = atom('Hello python')
    assert get_x() == 'Hello python'
    assert process_x() == 'Hello python'
    assert process_x(lambda x: x[::-1], ) == 'nohtyp olleH'
    assert set_x(10) == 10
    delete_x()
    assert not get_x()


if __name__ == '__main__':
    test()
