"""
Define en passant helper objects.
"""

import sys
_PY2 = sys.version_info[0] == 2

try:
    from collections import OrderedDict
except ImportError:
    # Python 2.6
    from .ordereddict import OrderedDict

__all__ = 'Passer Grabber'.split()


class _NeverSeen(object):
    pass


class Passer(object):

    """
    Objects that help proxy values for en passant operations.
    """

    def __init__(self):
        """
        Make one!
        """
        self.value = _NeverSeen

    def _grab(self, other):
        """
        Get the value of the second operand, and return it as well.
        """
        self.value = other
        return other

    def _bool(self):
        """
        Return the boolean value of our value.
        """
        return bool(self.value)

    if _PY2:
        __div__ = _grab
        __nonzero__ = _bool
    else: # PY3 and ff
        __truediv__ = _grab
        __bool__ = _bool

    # define alterate operators (< and <=)
    __lt__ = _grab
    __le__ = _grab

    def __getattr__(self, name):
        """
        Forward attribute access to the contained value.
        """
        try:
            return object.__getattr__(self, name)
        except AttributeError:
            return getattr(self.value, name)

    def __setattr__(self, name, value):
        """
        Forward attribute setting to the contained value.
        """
        if name == 'value':
            object.__setattr__(self, name, value)
        else:
            setattr(self.value, name, value)

    def __getitem__(self, n):
        """
        Forward item access (indexing) to the contained value.
        """
        return self.value.__getitem__(n)

    def __setitem__(self, n, value):
        """
        Forward item setting (via index) to the contained value.
        """
        return self.value.__setitem__(n, value)

    def __call__(self, arg=_NeverSeen):
        """
        Use call to either caputre a result value or render the
        contained value. The first time called, captures. On
        subsequent calls, renders.
        """
        if arg is not _NeverSeen:
            self.value = arg
        return self.value

    def __pos__(self):
        """
        Implements positive unary operation, +x, to render value.
        """
        return self.value

    def __repr__(self):
        """
        Return string representation, showing current value.
        """
        return "{0}({1!r})".format(self.__class__.__name__, self.value)


class Grabber(object):

    """
    Objects that grab the value of initial attribute calls.
    """

    def __init__(self):
        """
        Make one!"
        """
        self._data = OrderedDict()

    def __getattr__(self, name):
        """
        The attribute call. If no such attribute already exists, return a
        setter function that will do the inital setting.
        """
        if name in self._data:
            return self._data[name]
        else:
            def setter(value):
                self._data[name] = value
                return value
            return setter

    def __repr__(self):
        """
        Return the string representation.
        """
        guts = ', '.join("{0}={1!r}".format(k, v)
                         for k, v in self._data.items())
        return "{0}({1})".format(self.__class__.__name__, guts)
