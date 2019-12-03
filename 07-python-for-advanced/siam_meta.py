"""This module contains realization of  a metaclass SiamMeta.

SiamMeta a special metaclass. Class instances created using SiamMeta
class have the following properties:
* objects created with the same attributes will be the same object
* objects created with different attributes will be different objects
* any object has the ability to access other objects same class
through class attribute connect.

    Typical usage example:

    SiamObj(metaclass=SiamMeta):
        pass
"""

import inspect
import weakref


class SiamMeta(type):
    """ Metaclass SiamMeta.

    SiamMeta gives the classes created on its basis the following properties:
    * objects created with the same attributes will be the same object
    * objects created with different attributes will be different objects
    * any object has the ability to access other objects same class
    through class attribute connect.

    Attributes:
        pool: A set of references on  unique classes instances.
        connect: Method provides instances access other objects same class.
    """
    _instances = {}
    pool = weakref.WeakSet()

    def __call__(cls, *args, **kwargs):
        """Decorates class method __call__

        Adds to class instances attributes pool and
        method connect.

        Returns:
             New class instance if class attributes unique
             otherwise return existed class instances with called attributes.
        """
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
        """Provides instances access to other objects with same class.

            Method provides  one class instances access to  another
            instances of this class. Throw calling it created with attributes.

            Returns:
                Class instances with created attributes args and kwargs.
        """
        params = inspect.signature(cls.__init__).bind_partial(cls, *args, **kwargs)
        params.apply_defaults()
        params = str(params)
        return SiamMeta._instances[params]()


class SiamObj(metaclass=SiamMeta):
    """Example class

    To use:
    >>> unit1 = SiamObj('1', '2', a=1)
    >>> unit2 = SiamObj('1', '2', a=1)
    >>> unit1 is unit2
    True
    >>> unit3 = SiamObj('2', '2', a=1)
    >>> unit3.connect('1', '2', 1).a = 2
    >>> unit2.a == 2
    True
    >>> pool = unit3.pool
    >>> print(len(pool))
    2
    >>> del unit3
    >>> print(len(pool))
    1
    """
    def __init__(self, b: str, c: str, a: int):
        self.b = b
        self.c = c
        self.a = a


if __name__ == '__main__':
    print(help(__name__))
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
