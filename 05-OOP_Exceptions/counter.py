def instances_counter(cls):
    cls.counter = 0
    true_new = cls.__new__

    def __new__(cls, *args, **kwargs):
        cls.counter += 1
        return true_new(cls, *args, **kwargs)

    def get_created_instances(self: cls = None) -> int:
        return cls.counter

    def reset_instances_counter(self: cls = None) -> int:
        counter = cls.counter
        cls.counter = 0
        return counter

    cls.get_created_instances = get_created_instances
    cls.reset_instances_counter = reset_instances_counter
    cls.__new__ = __new__
    return cls


@instances_counter
class User:
    pass


if __name__ == '__main__':
    assert User.get_created_instances() == 0
    user = User()
    assert user.get_created_instances() == 1
    assert user.reset_instances_counter() == 1
    assert user.get_created_instances() == 0
