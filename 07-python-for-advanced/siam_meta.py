import inspect
import weakref


class SiamMeta(type):
    _instances = {}
    pool = weakref.WeakSet()

    def __call__(cls, *args, **kwargs):
        params = inspect.signature(cls.__init__).bind_partial(cls, *args, **kwargs)
        params.apply_defaults()
        params = str(params)
        if params not in cls._instances:
            instance = super(SiamMeta, cls).__call__(*args, **kwargs)
            SiamMeta._instances[params] = weakref.ref(instance)
            SiamMeta.pool.add(instance)
            cls.pool = SiamMeta.pool
            cls.connect = cls.connect
            return instance
        instance = SiamMeta._instances[params]()
        return instance

    def connect(cls, *args, **kwargs):
        params = inspect.signature(cls.__init__).bind_partial(cls, *args, **kwargs)
        params.apply_defaults()
        params = str(params)
        return SiamMeta._instances[params]()


class SiamObj(metaclass=SiamMeta):
    def __init__(self, b: str, c: str, a: int):
        self.b = b
        self.c = c
        self.a = a


if __name__ == '__main__':
    unit1 = SiamObj('1', '2', a=1)
    unit2 = SiamObj('1', '2', a=1)
    assert unit1 is unit2
    unit3 = SiamObj('2', '2', a=1)
    unit3.connect('1', '2', 1).a = 2

    assert unit2.a == 2
    pool = unit3.pool
    assert len(pool) == 2
    del unit3
    assert len(pool) == 1
