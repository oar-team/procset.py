==========
procset.py
==========

Toolkit to manage sets of closed intervals.

`procset` is a pure python module to manage sets of closed intervals. It can be
used as a small python library to manage sets of resources, and is especially
useful when writing schedulers.


Features
--------

- Free Software: licensed under LGPLv3 (see `<LICENSE.rst>`_).
- Pure Python module :)
- Thoroughly tested!
- Drop-in replacement for `interval_set` (see `intsetwrap.py
  <src/intsetwrap.py>`_).


Limitations
-----------

- The provided implementation target only Python 3 (I do not want to maintain
  old stuff :P).
- The intervals bounds have to be non-negative integers.


Requirements
------------

- `setuptools>=34.4.0`


Example use
-----------

What does it look like to use ``procset``?  Here is a simple example program:

.. code:: python

   from procset import ProcSet


   free_cores = ProcSet((0, 7))  # I have 8 cores to work with

   job_cores = ProcSet((2, 5))  # let's use some cores for a job
   free_cores -= job_cores

   print('remaining cores:', str(free_cores))


And it looks like this when run:

.. code:: bash

   $ python example.py
   remaining cores: 0-1 6-7
