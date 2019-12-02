import time
import uuid


def timer_property(timing: int = 0):
    cache = {}
    start_time = {}

    class Property(object):

        def __init__(self, fget=None, fset=None, fdel=None, doc=None):
            self.fget = fget
            self.fset = fset
            self.fdel = fdel
            if doc is None and fget is not None:
                doc = fget.__doc__
            self.__doc__ = doc

        def __set_name__(self, owner, name):
            owner.read = self.getter(self.fget)

        def __get__(self, obj, objtype=None):

            if obj is None:
                return self
            if self.fget is None:
                raise AttributeError("unreadable attribute")
            nonlocal start_time, cache
            start_time.setdefault(obj, float('-inf'))
            if start_time[obj] + timing <= time.monotonic():
                start_time[obj] = time.monotonic()
                cache[obj] = self.fget(obj)
            return cache[obj]

        def __set__(self, obj, value):
            if self.fset is None:
                raise AttributeError("can't set attribute")
            nonlocal start_time, cache
            cache[obj] = value
            start_time[obj] = time.monotonic()
            return self.fset(obj, cache)

        def __delete__(self, obj):
            if self.fdel is None:
                raise AttributeError("can't delete attribute")
            self.fdel(obj)

        def getter(self, fget):
            return type(self)(fget, self.fset, self.fdel, self.__doc__)

        def setter(self, fset):
            return type(self)(self.fget, fset, self.fdel, self.__doc__)

    return Property


class Message:

    @timer_property(2)
    def msg(self):
        self._msg = self.get_message()
        return self._msg

    @msg.setter  # reset timer also
    def msg(self, param):
        self._msg = param

    def get_message(self):
        """
        Return random string
        """
        return uuid.uuid4().hex


if __name__ == '__main__':
    m = Message()
    a = Message()
    initial = m.read
    assert initial is m.read
    time.sleep(2)
    assert initial is not m.read
