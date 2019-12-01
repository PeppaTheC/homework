class Suppressor:
    __slots__ = {'exception'}

    def __init__(self, *exception):
        self.exception = exception

    def __enter__(self):
        pass

    def __exit__(self, exp_type, exp_value, traceback):
        return exp_type in self.exception or issubclass(exp_type, self.exception)


with Suppressor(ZeroDivisionError):
    1 / 0
print("It's fine")
