# -*- coding: utf-8 -*-

import operator


class ProcInt(tuple):

    __slots__ = ()

    def __new__(cls, inf, sup):
        """Create new instance of ProcInt(inf, sup)."""
        if not isinstance(inf, int):
            raise TypeError('{}() argument inf must be int'.format(cls.__name__))
        if not isinstance(sup, int):
            raise TypeError('{}() argument sup must be int'.format(cls.__name__))
        if inf > sup:
            raise ValueError('Invalid interval bounds')
        if inf < 0:
            raise ValueError('Invalid negative bound(s)')
        return tuple.__new__(cls, (inf, sup))

    def __repr__(self):
        """Return a nicely formatted representation string."""
        return '{}(inf={!r}, sup={!r})'.format(self.__class__.__name__, *self)

    def __str__(self):
        return format(self)

    def __format__(self, format_spec):
        if self.inf == self.sup:
            return str(self.inf)
        else:
            if len(format_spec) > 1:
                raise ValueError('Invalid format specifier')
            insep = format_spec or '-'
            return insep.join(map(str, self))

    def __len__(self):
        return self.sup - self.inf + 1

    def __contains__(self, item):
        return self.inf <= item <= self.sup

    inf = property(operator.itemgetter(0), doc='Alias for field number 0')

    sup = property(operator.itemgetter(1), doc='Alias for field number 1')


class ProcSet:

    __slots__ = ()

    def __init__(self, it=None):
        raise NotImplementedError

    @classmethod
    def from_str(cls, string, insep="-", outsep=" "):
        raise NotImplementedError

    @classmethod
    def _from_iterable(cls, it):
        """
        Construct an instance of the class from any iterable input.
        """
        return cls(it)

    def __str__(self):
        """interval_set_to_string(intervals, separator=" ")"""
        return format(self)

    def __format__(self, format_spec):
        raise NotImplementedError

    def __repr__(self):
        raise NotImplementedError

    def __iter__(self):
        raise NotImplementedError

    def __reversed__(self):
        raise NotImplementedError

    def __contains__(self, item):
        raise NotImplementedError

    def __len__(self):
        """Return the number of processors."""
        raise NotImplementedError

    def count(self):
        """Return the number of disjoint processors' intervals."""
        raise NotImplementedError

    def iscontiguous(self):
        """Return True if the processors form a single contiguous set."""
        return self.count() == 1

    def isdisjoint(self, other):
        raise NotImplementedError

    def issubset(self, other):
        raise NotImplementedError

    def __le__(self, other):
        raise NotImplementedError

    def __lt__(self, other):
        raise NotImplementedError

    def issuperset(self, other):
        raise NotImplementedError

    def __ge__(self, other):
        raise NotImplementedError

    def __gt__(self, other):
        raise NotImplementedError

    def union(self, *others):
        raise NotImplementedError

    def __or__(self, other):
        raise NotImplementedError

    __ror__ = __or__

    def __eq__(self, other):
        raise NotImplementedError

    def intersection(self, *others):
        raise NotImplementedError

    def __and__(self, other):
        raise NotImplementedError

    __rand__ = __and__

    def difference(self, *others):
        raise NotImplementedError

    def __sub__(self, other):
        raise NotImplementedError

    __rsub__ = __sub__

    def symmetric_difference(self, other):
        raise NotImplementedError

    def __xor__(self, other):
        raise NotImplementedError

    __rxor__ = __xor__

    def copy(self):
        raise NotImplementedError

    def update(self, *others):
        raise NotImplementedError

    def __ior__(self, other):
        raise NotImplementedError

    def intersection_update(self, *others):
        raise NotImplementedError

    def __iand__(self, other):
        raise NotImplementedError

    def difference_update(self, *others):
        raise NotImplementedError

    def __isub__(self, other):
        raise NotImplementedError

    def symmetric_difference_update(self, other):
        raise NotImplementedError

    def __ixor__(self, other):
        raise NotImplementedError

    def add(self, elem):
        raise NotImplementedError

    def remove(self, elem):
        raise NotImplementedError

    def discard(self, elem):
        raise NotImplementedError

    def pop(self, elem):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def __getitem__(self, key):
        raise NotImplementedError

    # we do not define __setitem__ as it makes no sense to modify a processor

    def __delitem__(self, key):
        raise NotImplementedError

    def aggregate(self):
        raise NotImplementedError


# Deprecated functions that will be removed in the future major release.

import functools
import warnings


def deprecated(message=""):
    def decorated(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(
                message,
                DeprecationWarning,
                stacklevel=2
            )
            return func(*args, **kwargs)
        return wrapper
    return decorated


@deprecated("Deprecated function: use list(itvs) instead.")
def interval_set_to_id_list(itvs):
    return list(itvs)


@deprecated("Deprecated function: use set(itvs) instead.")
def interval_set_to_set(itvs):
    return set(itvs)


@deprecated("Deprecated function: use ProcSet(s) instead.")
def set_to_interval_set(s):
    return ProcSet(s)


@deprecated("Deprecated function: use ProcSet(ids) instead.")
def id_list_to_iterval_set(ids):
    return ProcSet(ids)


@deprecated("Deprecated function: use ProcSet.from_str(s) instead.")
def string_to_interval_set(s, separator=" "):
    return ProcSet.from_str(s, outsep=separator)


@deprecated("Deprecated function: use str(intervals) or format(intervals) instead.")
def interval_set_to_string(intervals, separator=" "):
    format_spec = '-' + separator[0]
    return format(intervals, format_spec)


@deprecated("Deprecated function: use len(itvs) instead.")
def total(itvs):
    return len(itvs)


@deprecated("Deprecated function: use == instead.")
def equals(itvs1, itvs2):
    return itvs1 == itvs2


@deprecated("Deprecated function: itvs_base - itvs2 instead.")
def difference(itvs_base, itvs2):
    return itvs_base - itvs2


@deprecated("Deprecated function: use itvs1 & itvs2 instead.")
def intersection(itvs1, itvs2):
    return itvs1 & itvs2


@deprecated("Deprecated function: use itvs1 | itvs2 instead.")
def union(itvs1, itvs2):
    return itvs1 | itvs2


@deprecated("Deprecated function: use aggregate method instead.")
def aggregate(itvs):
    return itvs.aggregate()
