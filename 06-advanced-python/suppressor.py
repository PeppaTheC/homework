class Suppressor:
    __slots__ = {'exception'}

    def __init__(self, *exception):
        self.exception = exception

    def __enter__(self):
        pass

    def __exit__(self, exp_type, exp_value, traceback):
        return issubclass(exp_type, self.exception)


with Suppressor(ArithmeticError):
    1 / 0
print("It's fine")
