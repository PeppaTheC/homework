def instances_counter(cls):
    class Wrapper(cls):
        counter = 0

        def __init__(self):
            super().__init__()
            self.__class__.counter += 1

        @classmethod
        def get_created_instances(cls):
            return cls.counter

        @classmethod
        def reset_instances_counter(cls):
            counter = cls.counter
            cls.counter = 0
            return counter

    Wrapper.__name__ = cls.__name__
    Wrapper.__doc__ = cls.__doc__
    return Wrapper


@instances_counter
class User:
    pass


if __name__ == '__main__':
    assert User.get_created_instances() == 0
    user, _, _ = User(), User(), User()
    assert user.get_created_instances() == 3
    assert user.reset_instances_counter() == 3
    assert user.get_created_instances() == 0
