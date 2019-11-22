def instances_counter(cls):

    class Wrapper(cls):
        counter = 0

        def __new__(cls, *args, **kwargs):
            cls.counter += 1
            instance = super().__new__(cls)
            return instance

        @classmethod
        def get_created_instances(cls):
            return cls.counter

        @classmethod
        def reset_instances_counter(cls):
            counter = cls.counter
            cls.counter = 0
            return counter

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
