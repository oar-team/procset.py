# -*- coding: utf-8 -*-

# Copyright © 2018
# Contributed by Raphaël Bleuse <raphael.bleuse@uni.lu>
#
# This file is part of procset.py, a pure python module to manage sets of
# closed intervals.
#
#   procset.py is free software: you can redistribute it and/or modify it
#   under the terms of the GNU Lesser General Public License version 3 only
#   as published by the Free Software Foundation.
#
#   procset.py is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License version 3 for more details.
#
#   You should have received a copy of the GNU Lesser General Public
#   License version 3 along with this program.  If not, see
#   <https://www.gnu.org/licenses/>.


def build_test_class(name, method, testcases, wrapper):
    """
    Build a pytest test class for a given method and a set of testcases.

    Build a pytest class with a test method for each testcase.  Given a dict of
    testcases (each key identifies a testcase), this function create a method
    out of testcase using wrapper.

    See test_procset_comparisons.py for an example.
    """
    tests = {
        'test_' + name: wrapper(testcase)
        for name, testcase in testcases.items()
    }
    return type(name, (), dict(method=method, **tests))
