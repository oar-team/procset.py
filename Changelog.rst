.. custom role for python code

.. role:: py(code)
   :language: python

.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..

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

Added
-----

- :py:`ProcSet.iter_slice`, a constant memory iterator with slice semantic


1.0rc1_ -- 2019-02-14
=====================

Added
-----

- Changelog
- support of slices for :py:`ProcSet.__getitem__`


Changed
-------

- documentation is managed with sphinx, and published on Read the Docs



1.0rc0_ -- 2019-02-07
=====================

Added
-----

- [issue #3, MR !2] full support of set operations for :py:`ProcSet`:
    - *operand methods* (:py:`|`, :py:`&`, :py:`-`, :py:`^`, :py:`|=`,
      :py:`&=`, :py:`-=`, :py:`^=`) support set operation (immutable and
      in-place) with :py:`ProcSet` objects only
    - *plain-text methods* (:py:`.union(…)`, :py:`.intersection(…)`,
      :py:`.difference(…)`, :py:`.symmetric_difference(…)`, :py:`.update(…)`,
      :py:`.intersection_update(…)`, :py:`.difference_update(…)`,
      :py:`.symmetric_difference_update(…)`) support set operations (both
      immutable and in-place) with any list of arguments that is a valid list
      of arguments for :py:`ProcSet` initialization.
      :py:`.symmetric_difference(…)` and :py:`.symmetric_difference_update(…)`
      support a single argument only.

- full support of set comparison methods for :py:`ProcSet`:
    - *operand methods* (:py:`<=`, :py:`<`, :py:`>=`, :py:`>`) support
      comparisons with :py:`ProcSet` objects only
    - *plain-text methods* (:py:`.isdisjoint(…)`, :py:`.issubset(…)`,
      :py:`.issuperset(…)`) support comparison with any list of arguments that
      is a valid list of arguments for :py:`ProcSet` initialization

- support of index-based access with integers for :py:`ProcSet` (e.g., :py:`self[a]`),
  slice objects (e.g., :py:`self[a:b:c]`) are not supported yet

- in-place emptying of a :py:`ProcSet` (:py:`.clear()`)

- :py:`.discard(…)` as an alias for :py:`.difference_update(…)`


Changed
-------

- cleaned public imports of modules :py:`procset` and :py:`intsetwrap`
- :py:`ProcInt` supports construction without specifying :py:`sup`:
  :py:`ProcInt(0)` is the same as :py:`ProcInt(inf=0, sup=0)`
- :py:`ProcSet` supports :py:`ProcSet` objects for its initialization
- :py:`ProcSet.isdisjoint(…)` is more permissive with the :py:`other` argument,
  see the description of added features
- :py:`ProcSet.insert(…)` is now an alias for :py:`.update(…)`: it is more
  permissive with its arguments, see the description of added features


0.4_ -- 2018-02-15
==================

Added
-----

- implement :py:`.isdisjoint(…)` for :py:`ProcSet`


0.3_ -- 2018-02-05
==================

Changed
-------

- :py:`ProcSet`:
    - [issue #7] rename :py:`.add(…)` into :py:`.insert(…)`
    - optimize performances of :py:`.__deepcopy__(…)`


0.2_ -- 2018-01-31
==================

Added
-----

- [issue #2] support shallow and deep copy for both :py:`ProcInt` and :py:`ProcSet`
  (see :py:`copy.copy` and :py:`copy.deepcopy`)
- [issue #6] support :py:`repr` for :py:`ProcSet`


0.1.dev5_ -- 2017-09-13
=======================

Fixed
-----

- fix license metadata of package
- [issue #5] packaging of :py:`intsetwrap` module


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

- [issue #4] basic support of in-place set-like operations for :py:`ProcSet`:
  :py:`|=`, :py:`&=`, :py:`-=`, :py:`^=`


Fixed
-----

- :py:`.iscontiguous()` now returns :py:`True` for an empty :py:`ProcSet`


0.1.dev1_ -- 2017-03-28
=======================

Added
-----

- :py:`ProcSet`:
    - membership testing (a.k.a., :py:`in`)
    - iteration over the processors, in decreasing order (a.k.a. :py:`reversed(…)`)
    - :py:`.min`, :py:`.max`, attributes for fast access to the extremal
      processors
    - :py:`.intervals()`, a method to iterate over the contiguous ranges of a
      :py:`ProcSet`


0.1.dev0 -- 2017-03-22
======================

Added
-----

- :py:`ProcInt`, a compact representation of a contiguous processor interval

- :py:`ProcSet`, a compact representation of processor intervals:
    - parsing from (:py:`.from_str(…)`) / dumping to (:py:`str(…)`) a string
      representation (e.g., :py:`'0-3 8-15'`)
    - equality testing (:py:`==`)
    - contiguity testing (:py:`.iscontiguous()`)
    - number of processors (:py:`len(…)`)
    - number of contiguous ranges (:py:`.count()`)
    - iteration over the processors in increasing order (a.k.a. :py:`iter(…)`)
    - convex hull (:py:`.aggregate()`)
    - in-place insertion of processors (:py:`.add(…)`)
    - basic support of immutable set-like operations (returning the resulting
      :py:`ProcSet` as a new object): :py:`|`, :py:`&`, :py:`-`, :py:`^`


Deprecated
----------

- :py:`intsetwrap` provides a drop-in replacement module for
  :py:`interval_set`: it is guaranteed to stay until the first minor release of
  the stable API (i.e., for ``procset<=1.0``)


.. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. ..

.. links to git diffs: https://{gitlab-project-url}/compare/{previous-tag}...{current-tag}

.. _Unreleased: https://gitlab.inria.fr/bleuse/procset.py/compare/v1.0rc1...master
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
