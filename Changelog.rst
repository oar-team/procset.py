=========
Changelog
=========

All notable changes to this project will be documented in this file.

The format follows the recommendations of
`Keep a Changelog <https://keepachangelog.com/en/1.0.0/>`_, and adapts the
markup language to use reStructuredText.

This projects adheres to `Semantic Versioning <https://semver.org/spec/v2.0.0.html>`_.


Unreleased_
===========


1.0_ -- 2019-02-20
==================

Added
-----

- ``ProcSet.iter_slice``, a constant memory iterator with slice semantic


1.0rc1_ -- 2019-02-14
=====================

Added
-----

- Changelog
- support of slices for ``ProcSet.__getitem__``


Changed
-------

- documentation is managed with sphinx, and published on Read the Docs



1.0rc0_ -- 2019-02-07
=====================

Added
-----

- [issue #3, MR !2] full support of set operations for ``ProcSet``:
    - *operand methods* (``|``, ``&``, ``-``, ``^``, ``|=``, ``&=``, ``-=``,
      ``^=``) support set operation (immutable and in-place) with ``ProcSet``
      objects only
    - *plain-text methods* (``.union(…)``, ``.intersection(…)``,
      ``.difference(…)``, ``.symmetric_difference(…)``, ``.update(…)``,
      ``.intersection_update(…)``, ``.difference_update(…)``,
      ``.symmetric_difference_update(…)``) support set operations (both
      immutable and in-place) with any list of arguments that is a valid list
      of arguments for ``ProcSet`` initialization.
      ``.symmetric_difference(…)`` and ``.symmetric_difference_update(…)``
      support a single argument only.

- full support of set comparison methods for ``ProcSet``:
    - *operand methods* (``<=``, ``<``, ``>=``, ``>``) support comparisons with
      ``ProcSet`` objects only
    - *plain-text methods* (``.isdisjoint(…)``, ``.issubset(…)``,
      ``.issuperset(…)``) support comparison with any list of arguments that is
      a valid list of arguments for ``ProcSet`` initialization

- support of index-based access with integers for ``ProcSet`` (e.g., ``self[a]``),
  slice objects (e.g., ``self[a:b:c]``) are not supported yet

- in-place emptying of a ``ProcSet`` (``.clear()``)

- ``.discard(…)`` as an alias for ``.difference_update(…)``


Changed
-------

- cleaned public imports of modules ``procset`` and ``intsetwrap``
- ``ProcInt`` supports construction without specifying ``sup``:
  ``ProcInt(0)`` is the same as ``ProcInt(inf=0, sup=0)``
- ``ProcSet`` supports ``ProcSet`` objects for its initialization
- ``ProcSet.isdisjoint(…)`` is more permissive with the ``other`` argument,
  see the description of added features
- ``ProcSet.insert(…)`` is now an alias for ``.update(…)``: it is more
  permissive with its arguments, see the description of added features


0.4_ -- 2018-02-15
==================

Added
-----

- implement ``.isdisjoint(…)`` for ``ProcSet``


0.3_ -- 2018-02-05
==================

Changed
-------

- ``ProcSet``:
    - [issue #7] rename ``.add(…)`` into ``.insert(…)``
    - optimize performances of ``.__deepcopy__(…)``


0.2_ -- 2018-01-31
==================

Added
-----

- [issue #2] support shallow and deep copy for both ``ProcInt`` and ``ProcSet``
  (see ``copy.copy`` and ``copy.deepcopy``)
- [issue #6] support ``repr`` for ``ProcSet``


0.1.dev5_ -- 2017-09-13
=======================

Fixed
-----

- fix license metadata of package
- [issue #5] packaging of ``intsetwrap`` module


0.1.dev4_ -- 2017-09-11
=======================

Convenience release, nothing to report.


0.1.dev3_ -- 2017-09-11
=======================

Changed
-------

- the project is now licensed under LGPLv3


0.1.dev2_ -- 2017-09-06
=======================

Added
-----

- [issue #4] basic support of in-place set-like operations for ``ProcSet``:
  ``|=``, ``&=``, ``-=``, ``^=``


Fixed
-----

- ``.iscontiguous()`` now returns ``True`` for an empty ``ProcSet``


0.1.dev1_ -- 2017-03-28
=======================

Added
-----

- ``ProcSet``:
    - membership testing (a.k.a., ``in``)
    - iteration over the processors, in decreasing order (a.k.a. ``reversed(…)``)
    - ``.min``, ``.max``, attributes for fast access to the extremal
      processors
    - ``.intervals()``, a method to iterate over the contiguous ranges of a
      ``ProcSet``


0.1.dev0 -- 2017-03-22
======================

Added
-----

- ``ProcInt``, a compact representation of a contiguous processor interval

- ``ProcSet``, a compact representation of processor intervals:
    - parsing from (``.from_str(…)``) / dumping to (``str(…)``) a string
      representation (e.g., ``'0-3 8-15'``)
    - equality testing (``==``)
    - contiguity testing (``.iscontiguous()``)
    - number of processors (``len(…)``)
    - number of contiguous ranges (``.count()``)
    - iteration over the processors in increasing order (a.k.a. ``iter(…)``)
    - convex hull (``.aggregate()``)
    - in-place insertion of processors (``.add(…)``)
    - basic support of immutable set-like operations (returning the resulting
      ``ProcSet`` as a new object): ``|``, ``&``, ``-``, ``^``


Deprecated
----------

- ``intsetwrap`` provides a drop-in replacement module for
  ``interval_set``: it is guaranteed to stay until the first minor release of
  the stable API (i.e., for ``procset<=1.0``)


.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..

.. links to git diffs: https://{gitlab-project-url}/compare/{previous-tag}...{current-tag}

.. _Unreleased: https://gitlab.inria.fr/bleuse/procset.py/compare/v1.0...master
.. _1.0: https://gitlab.inria.fr/bleuse/procset.py/compare/v1.0rc1...v1.0
.. _1.0rc1: https://gitlab.inria.fr/bleuse/procset.py/compare/v1.0rc0...v1.0rc1
.. _1.0rc0: https://gitlab.inria.fr/bleuse/procset.py/compare/v0.4...v1.0rc0
.. _0.4: https://gitlab.inria.fr/bleuse/procset.py/compare/v0.3...v0.4
.. _0.3: https://gitlab.inria.fr/bleuse/procset.py/compare/v0.2...v0.3
.. _0.2: https://gitlab.inria.fr/bleuse/procset.py/compare/v0.1.dev5...v0.2
.. _0.1.dev5: https://gitlab.inria.fr/bleuse/procset.py/compare/v0.1.dev4...v0.1.dev5
.. _0.1.dev4: https://gitlab.inria.fr/bleuse/procset.py/compare/v0.1.dev3...v0.1.dev4
.. _0.1.dev3: https://gitlab.inria.fr/bleuse/procset.py/compare/v0.1.dev2...v0.1.dev3
.. _0.1.dev2: https://gitlab.inria.fr/bleuse/procset.py/compare/v0.1.dev1...v0.1.dev2
.. _0.1.dev1: https://gitlab.inria.fr/bleuse/procset.py/compare/v0.1.dev0...v0.1.dev1
