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


class _Sentinel:
    """Helper class whose instances are greater than any object."""

    __slots__ = ()

    def __eq__(self, other):
        return self is other

    def __lt__(self, other):
        return False

    __le__ = __eq__

    def __gt__(self, other):
        return True

    def __ge__(self, other):
        return True


class ProcSet:

    __slots__ = '_itvs'

    def __init__(self, *intervals):
        """
        Initialize a ProcSet.

        A ProcSet can be intialized with either nothing (empty set), any number
        of non-negative int, any number of ProcInt compatible objects (iterable
        of 2 ints), or any combination of both.

        There are no restrictions on the domains of the intervals in the
        constructor: they may overlap.

        Examples:
            ProcSet()  # empty set
            ProcSet(1)
            ProcSet(ProcInt(0, 1))
            ProcSet(ProcInt(0, 1), ProcInt(2, 3))
            ProcSet((0, 1), [2, 3])  # identical to previous call
            ProcSet(ProcInt(0, 1), *[0, 3])  # mixing ProcInt and lists
        """
        self._itvs = []  # list of disjoint intervals
        for itv in intervals:
            self.add(itv)

    @classmethod
    def from_str(cls, string, insep="-", outsep=" "):
        """Parse a string interval set representation into a ProcSet."""
        if not isinstance(string, str):
            raise TypeError(
                'from_str() argument 2 must be str, not {}'.format(string.__class__.__name__)
            )

        new_pset = cls()

        # empty string is parsed as empty ProcSet
        if string == '':
            return new_pset

        try:
            for itv in string.split(sep=outsep):
                bounds = itv.split(sep=insep, maxsplit=1)
                if len(bounds) == 1:
                    new_pset.add(int(itv))
                else:
                    inf, sup = bounds
                    new_pset.add(ProcInt(int(inf), int(sup)))
        except ValueError:
            raise ValueError(
                'Invalid interval format, parsed string is: {}'.format(string)
            ) from None

        return new_pset

    @classmethod
    def _from_iterable(cls, it):
        """Construct an instance of the class from any iterable input."""
        return cls(*it)

    def __str__(self):
        return format(self)

    def __format__(self, format_spec):
        if format_spec:
            try:
                insep, outsep = format_spec
            except ValueError:
                raise ValueError('Invalid format specifier') from None
        else:
            insep, outsep = '- '

        return outsep.join(format(itv, insep) for itv in self._itvs)

    # def __repr__(self):
    #     pass

    def __iter__(self):
        for itv in self._itvs:
            yield from range(itv.inf, itv.sup + 1)

    def __reversed__(self):
        raise NotImplementedError

    def __contains__(self, item):
        raise NotImplementedError

    def __len__(self):
        """Return the number of processors."""
        return sum(len(itv) for itv in self._itvs)

    def count(self):
        """Return the number of disjoint processors' intervals."""
        return len(self._itvs)

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

    def _flatten(self):
        """Generate the (flat) list of interval bounds contained by self."""
        for itv in self._itvs:
            # use inf as is
            yield False, itv.inf
            # convert sup, as merging operations are made with half-open
            # intervals
            yield True, itv.sup + 1

    @classmethod
    def _merge_core(cls, leftset, rightset, keeppredicate):
        """
        Generate the (flat) list of interval bounds of the requested merge.
        """
        endbound = False
        sentinel = _Sentinel()

        # pylint: disable=protected-access
        lflat = leftset._flatten()
        rflat = rightset._flatten()
        lend, lhead = next(lflat, (False, sentinel))
        rend, rhead = next(rflat, (False, sentinel))

        head = min(lhead, rhead)
        while head < sentinel:
            inleft = (head < lhead) == lend
            inright = (head < rhead) == rend
            keep = keeppredicate(inleft, inright)

            if keep ^ endbound:
                endbound = not endbound
                yield head
            if head == lhead:
                lend, lhead = next(lflat, (False, sentinel))
            if head == rhead:
                rend, rhead = next(rflat, (False, sentinel))

            head = min(lhead, rhead)

    @classmethod
    def _merge(cls, leftset, rightset, keeppredicate):
        """
        Generate the ProcInt list of the requested merge.

        The returned iterator is supposed to be assigned to the _itvs attribute
        of the result ProcSet.
        See the difference(), intersection(), symmetric_difference(), and
        union() methods for an usage example.
        """
        flat_merge = cls._merge_core(leftset, rightset, keeppredicate)

        # Note that we are feeding the same iterable twice to zip.
        # The iterated bounds are hence grouped by pairs (lower and upper
        # bounds of the intervals).
        # As zip() stops on the shortest iterable, it won't consider the
        # optional terminating sentinel (the sentinel would be the last
        # element, and would have an odd index).
        for inf, sup in zip(flat_merge, flat_merge):
            yield ProcInt(inf, sup - 1)  # convert back to closed intervals

    def union(self, *others):
        raise NotImplementedError

    def __or__(self, other):
        """Return a new ProcSet with the intervals from self and other."""
        if not isinstance(other, self.__class__):
            return NotImplemented

        # pylint: disable=protected-access
        # we do not use self._from_iterable as we know the result already is a
        # valid _itvs list
        result = ProcSet()
        result._itvs = list(self._merge(self, other, operator.or_))
        return result

    __ror__ = __or__

    def __eq__(self, other):
        # pylint: disable=protected-access
        return self._itvs == other._itvs

    def intersection(self, *others):
        raise NotImplementedError

    def __and__(self, other):
        """Return a new ProcSet with the intervals common to self and other."""
        if not isinstance(other, self.__class__):
            return NotImplemented

        # pylint: disable=protected-access
        # we do not use self._from_iterable as we know the result already is a
        # valid _itvs list
        result = ProcSet()
        result._itvs = list(self._merge(self, other, operator.and_))
        return result

    __rand__ = __and__

    def difference(self, *others):
        raise NotImplementedError

    def __sub__(self, other):
        """
        Return a new ProcSet with the intervals in self that are not in other.
        """
        if not isinstance(other, self.__class__):
            return NotImplemented

        # pylint: disable=protected-access
        # we do not use self._from_iterable as we know the result already is a
        # valid _itvs list
        result = ProcSet()
        result._itvs = list(
            self._merge(
                self, other,
                lambda inleft, inright: inleft and not inright
            )
        )
        return result

    __rsub__ = __sub__

    def symmetric_difference(self, other):
        raise NotImplementedError

    def __xor__(self, other):
        """
        Return a new ProcSet with the intervals in either self or other but not
        both.
        """
        if not isinstance(other, self.__class__):
            return NotImplemented

        # pylint: disable=protected-access
        # we do not use self._from_iterable as we know the result already is a
        # valid _itvs list
        result = ProcSet()
        result._itvs = list(self._merge(self, other, operator.xor))
        return result

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
        """
        Insert elem into self.

        It is assumed elem is ProcInt compatible (iterable of 2 ints), or a
        single int.
        In the first case, ProcInt(*elem) is added into self, in the latter
        ProcInt(elem, elem) is added.

        If some processors already exist in self, they will not be added twice
        (hey this is a set!).
        """
        try:
            newinf, newsup = elem  # assume it is ProcInt compatible
        except TypeError:
            newinf, newsup = elem, elem  # if not assume it is a single point

        for itv in list(self._itvs):
            if newinf > itv.sup + 1:
                continue
            if newsup + 1 < itv.inf:
                break
            self._itvs.remove(itv)
            newinf = min(newinf, itv.inf)
            newsup = max(newsup, itv.sup)

        self._itvs.append(ProcInt(newinf, newsup))
        self._itvs.sort()

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
