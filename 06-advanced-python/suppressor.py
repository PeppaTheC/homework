class Suppressor:
    __slots__ = {'exception'}

    def __init__(self, exception: type):
        self.exception = exception

    def __enter__(self):
        pass

    def __exit__(self, exp_type, exp_value, traceback):
        if exp_type == self.exception:
            return True
        return False

    pass


with Suppressor(ZeroDivisionError):
    1 / 0
print("It's fine")
