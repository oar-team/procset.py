.. role:: py(code)
   :language: python


API description
===============

This document describes the API for the ProcSet.

The implementation status is indicated by the bullet:
✗ means the method is not yet implemented,
✓ means the method is implemented,
✓✓ means the method is implemented and optimized.

basic methods
-------------

✗ :py:`str(s)`:, :py:`format(s, format_spec)`:
    - implemented by :py:`__str__` and :py:`__format__`
    - the default inner and outer separators respectively are :py:`-` and
      :py:` `
    - the format spec is a string of length 2, where the inner (resp. outer)
      separator is the first (resp. second) item
    - :py:`format(s, '')` matches the behavior of :py:`str` as recommended in
      the documentation


container-like methods
----------------------

✗ :py:`len(s)`:
    implemented by :py:`__len__`

✗ :py:`x in s`, :py:`x not in s`:
    implemented by :py:`__contains__`

✗ iterator operations:
    implemented by :py:`__iter__`, :py:`__reversed__`

https://docs.python.org/3/reference/datamodel.html#emulating-container-types


sequence-like methods
---------------------

✗ :py:`[i]`:
    implemented with :py:`__getitem__` called with an :py:`int`

✗ :py:`[i:j]`, :py:`[i:j:k]`:
    implemented with :py:`__getitem__` called with an :py:`slice`

✗ :py:`del s[i]`:
    implemented with :py:`__delitem__`

✗ :py:`min`, :py:`max`:
    provide fast method

https://docs.python.org/3/library/stdtypes.html#sequence-types-list-tuple-range


set-like methods
----------------

- immutable operations:
    ✗ :py:`isdisjoint(other)`

    ✗ :py:`issubset(other)`, :py:`<= other`:
        implemented by :py:`__le__`

    ✗ :py:`< other`:
        implemented by :py:`__lt__`

    ✗ :py:`issuperset(other)`, :py:`>= other`:
        implemented by :py:`__ge__`

    ✗ :py:`> other`:
        implemented by :py:`__gt__`

    ✗ :py:`== other`:
        implemented by :py:`__eq__`

    ✗ :py:`union(*others)`, :py:`| other | …`:
        implemented by :py:`__or__`, check :py:`__ror__`

    ✗ :py:`intersection(*others)`, :py:`& other & …`:
        implemented by :py:`__and__`, check :py:`__rand__`

    ✗ :py:`difference(*others)`, :py:`- other - …`:
        implemented by :py:`__sub__`, check :py:`__rsub__`

    ✗ `symmetric_difference(other)`, :py:`^ other`:
        implemented by :py:`__xor__`

    ✗ :py:`copy()`

- mutable operations:
    ✗ :py:`update(*others)`, :py:`|= other | …`:
        implemented by :py:`__ior__`

    ✗ :py:`intersection_update(*others)`, :py:`&= other & …`:
        implemented by :py:`__iand__`

    ✗ :py:`difference_update(*others)`, :py:`-= other | …`:
        implemented by :py:`__isub__`

    ✗ `symmetric_difference_update(other)`, :py:`^= other`:
        implemented by :py:`__ixor__`

    ✗ :py:`add(elem)`

    ✗ :py:`remove(elem)`

    ✗ :py:`discard(elem)`

    ✗ :py:`pop()`

    ✗ :py:`clear()`

https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset


custom methods
--------------

- new functions:
    ✗ :py:`iscontiguous()`:
        return :py:`True` if the processors form a single contiguous set

    ✗ :py:`count()`:
        could add a parameter :py:`minspan=1` to set the min width to count
        interval

- adapted functions:
    ✗ :py:`aggregate()`:
        return the smallest interval containing :py:`itvs`, could use
        :py:`span` attribute with a property


Deprecated functions
====================

✓ :py:`equals(itvs1, itvs2)`:
    use :py:`==` instead

✓ :py:`total(itvs)`:
    use :py:`len` instead

✓ :py:`interval_set_to_id_list(itvs)`:
    use :py:`list(itvs)` instead (possible through :py:`__iter__`)

✓ :py:`interval_set_to_set(intervals)`:
    use :py:`set(itvs)` instead (possible through :py:`__iter__`)

✓ :py:`set_to_interval_set(s)`:
    use constructor instead

✓ :py:`id_list_to_iterval_set(ids)`:
    use constructor instead

✓ :py:`string_to_interval_set(s, separator=" ")`:
    use :py:`from_str` instead

✗ :py:`interval_set_to_string(intervals, separator=" ")`:
    use :py:`__str__` or :py:`__format__` instead

✓ :py:`difference(itvs_base, itvs2)`:
    use :py:`-` instead

✓ :py:`intersection(itvs1, itvs2)`:
    use :py:`&` instead

✓ :py:`union(itvs1, itvs2)`:
    use :py:`|` instead

✓ :py:`aggregate(itvs)`:
    use :py:`aggregate` method instead

Old API usage in evalys
=======================

The comparison is made against commit d6d7234e51727adc0922b1df8826e5c6bd4b10ac.

+========================+===========+=============+
| function               | frequency | implemented |
+========================+===========+=============+
| difference             |         4 |             |
+------------------------+-----------+-------------+
| interval_set_to_set    |         3 |             |
+------------------------+-----------+-------------+
| string_to_interval_set |         3 |             |
+------------------------+-----------+-------------+
| intersection           |         2 |             |
+------------------------+-----------+-------------+
| total                  |         2 |             |
+------------------------+-----------+-------------+
| equals                 |         1 |             |
+------------------------+-----------+-------------+
| interval_set_to_string |         1 |             |
+------------------------+-----------+-------------+
| set_to_interval_set    |         1 |             |
+------------------------+-----------+-------------+
| union                  |         1 |             |
+------------------------+-----------+-------------+
