"""Module provides realization of  a timer_property.

Timer_property copies behavior of a built-in property with following extensions:
* stores the result of the method for some time, which is transmitted
parameter to initialize the property
* recalculates value if timer expires

    Typical usage example:
    class Example:

        @timer_property(2)
        def msg(self):
        return self._msg

        @msg.setter
        def msg(self, param):
            self._msg = param
"""
import time
import uuid


def timer_property(timing: int = 0):
    """Extend original property.

    Args:
      timing: Time in seconds for updating cache.

    Returns:
      Class Property.
    """
    cache = {}
    start_time = {}

    class Property:
        """Property with timing cache

        Args:
            fget: function to be used for getting an attribute value
            fset: function to be used for setting an attribute value
            fdel: function to be used for del'ing an attribute
            doc: docstring
        """

        def __init__(self, fget=None, fset=None, fdel=None, doc=None):
            self.fget = fget
            self.fset = fset
            self.fdel = fdel
            if doc is None and fget is not None:
                doc = fget.__doc__
            self.__doc__ = doc

        def __set_name__(self, owner, name):
            """Set new class attribute read as getter"""
            owner.read = self.getter(self.fget)

        def __get__(self, obj, objtype=None):
            """Extension of original property get.

            Replaces usual returning  by returning cache value
            if timer didn't expire.

            Args:
                obj: Instance which tries to access to attribute .
                objtype: Class of instance

            Returns:
                Result of method if timer didn't expired,
                otherwise return cache

            Raises:
                AttributeError: An error occurred when function to be used
                for getting an attribute value wasn't defined.
            """
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
            """Extension of original property set.

            Set an attribute of instance to value and
            set new value into the cache and reset timer.
            """
            if self.fset is None:
                raise AttributeError("can't set attribute")
            nonlocal start_time, cache
            cache[obj] = value
            start_time[obj] = time.monotonic()
            return self.fset(obj, cache)

        def __delete__(self, obj):
            """ Delete an attribute of instance. """
            if self.fdel is None:
                raise AttributeError("can't delete attribute")
            self.fdel(obj)

        def getter(self, fget):
            """ Descriptor to change the getter on a property."""
            return type(self)(fget, self.fset, self.fdel, self.__doc__)

        def setter(self, fset):
            """ Descriptor to change the setter on a property."""
            return type(self)(self.fget, fset, self.fdel, self.__doc__)

    return Property


class Message:
    """Example class

    To use:
    >>> m = Message()
    >>> initial = m.read
    >>> initial is m.read
    True
    >>> time.sleep(2)
    >>> initial is not m.read
    False
    """

    @timer_property(2)
    def msg(self):
        self._msg = self.get_message()
        return self._msg

    @msg.setter  # reset timer also
    def msg(self, param):
        self._msg = param

    def get_message(self):
        """ Return random string. """
        return uuid.uuid4().hex


if __name__ == '__main__':
    m = Message()
    initial = m.read
    assert initial is m.read
    time.sleep(2)
    assert initial is not m.read
