# -*- coding: utf-8 -*-

# Copyright © 2017
# Contributed by Raphaël Bleuse <raphael.bleuse@imag.fr>
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import collections
import operator
import pytest
from procset import ProcSet


# The naming convention of the tests follows the one in the position paper by
# the IEEE Interval Standard Working Group - P1788.
# See docs/NehmeierM2010Interval.pdf for further informations.


# helper functions/classes

_TestCase = collections.namedtuple(
    '_TestCase',
    ['doc', 'leftop', 'rightop', 'expect_len', 'expect_count', 'expect_list']
)


def build_test_class(name, operator, testcases, wrapper):
    tests = {
        'test_' + name: wrapper(testcase)
        for name, testcase in testcases.items()
    }
    return type(name, (), dict(operator=operator, **tests))


def build_merge_test(testcase):
    def merge_test(self):
        pleft = testcase.leftop
        pright = testcase.rightop
        pres = self.operator(pleft, pright)
        assert len(pres) == testcase.expect_len
        assert pres.count() == testcase.expect_count
        assert list(pres) == testcase.expect_list

    merge_test.__doc__ = testcase.doc

    return merge_test


# testcases

difference_testcases = {
    'before_ii_notouch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[__]........+∞
        right: -∞.........[_]....+∞
        final: -∞....[__]........+∞
        """,
        ProcSet((0, 3)),
        ProcSet((5, 7)),
        4,
        1,
        [0, 1, 2, 3]
    ),
    'before_ip_notouch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[__]........+∞
        right: -∞...........X....+∞
        final: -∞....[__]........+∞
        """,
        ProcSet((0, 3)),
        ProcSet(7),
        4,
        1,
        [0, 1, 2, 3]
    ),
    'before_pi_notouch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....X...........+∞
        right: -∞........[__]....+∞
        final: -∞....X...........+∞
        """,
        ProcSet(0),
        ProcSet((4, 7)),
        1,
        1,
        [0]
    ),
    'before_pp_notouch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....X...........+∞
        right: -∞........X.......+∞
        final: -∞....X...........+∞
        """,
        ProcSet(0),
        ProcSet(4),
        1,
        1,
        [0]
    ),
    'before_ii_touch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[__]........+∞
        right: -∞........[__]....+∞
        final: -∞....[__]........+∞
        """,
        ProcSet((0, 3)),
        ProcSet((4, 7)),
        4,
        1,
        [0, 1, 2, 3]
    ),
    'before_ip_touch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[__]........+∞
        right: -∞........X.......+∞
        final: -∞....[__]........+∞
        """,
        ProcSet((0, 3)),
        ProcSet(4),
        4,
        1,
        [0, 1, 2, 3]
    ),
    'before_pi_touch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....X...........+∞
        right: -∞.....[_]........+∞
        final: -∞....X...........+∞
        """,
        ProcSet(0),
        ProcSet((1, 3)),
        1,
        1,
        [0]
    ),
    'before_pp_touch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....X...........+∞
        right: -∞.....X..........+∞
        final: -∞....X...........+∞
        """,
        ProcSet(0),
        ProcSet(1),
        1,
        1,
        [0]
    ),
    'meets_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[__]........+∞
        right: -∞.......[___]....+∞
        final: -∞....[_].........+∞
        """,
        ProcSet((0, 3)),
        ProcSet((3, 7)),
        3,
        1,
        [0, 1, 2]
    ),
    'overlaps_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[____]......+∞
        right: -∞......[____]....+∞
        final: -∞....[]..........+∞
        """,
        ProcSet((0, 5)),
        ProcSet((2, 7)),
        2,
        1,
        [0, 1]
    ),
    'starts_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[__]........+∞
        right: -∞....[______]....+∞
        final: -∞................+∞
        """,
        ProcSet((0, 3)),
        ProcSet((0, 7)),
        0,
        0,
        []
    ),
    'starts_pi': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....X...........+∞
        right: -∞....[__]........+∞
        final: -∞................+∞
        """,
        ProcSet(0),
        ProcSet((0, 3)),
        0,
        0,
        []
    ),
    'containedby_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞......[__]......+∞
        right: -∞....[______]....+∞
        final: -∞................+∞
        """,
        ProcSet((2, 5)),
        ProcSet((0, 7)),
        0,
        0,
        []
    ),
    'containedby_pi': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞.......X........+∞
        right: -∞....[______]....+∞
        final: -∞................+∞
        """,
        ProcSet(3),
        ProcSet((0, 7)),
        0,
        0,
        []
    ),
    'finishes_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞........[__]....+∞
        right: -∞....[______]....+∞
        final: -∞................+∞
        """,
        ProcSet((4, 7)),
        ProcSet((0, 7)),
        0,
        0,
        []
    ),
    'finishes_pi': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞.......X........+∞
        right: -∞....[__]........+∞
        final: -∞................+∞
        """,
        ProcSet(3),
        ProcSet((0, 3)),
        0,
        0,
        []
    ),
    'equal_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[__]........+∞
        right: -∞....[__]........+∞
        final: -∞................+∞
        """,
        ProcSet((0, 3)),
        ProcSet((0, 3)),
        0,
        0,
        []
    ),
    'equal_pp': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....X...........+∞
        right: -∞....X...........+∞
        final: -∞................+∞
        """,
        ProcSet(0),
        ProcSet(0),
        0,
        0,
        []
    ),
    'finishedby_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[______]....+∞
        right: -∞........[__]....+∞
        final: -∞....[__]........+∞
        """,
        ProcSet((0, 7)),
        ProcSet((4, 7)),
        4,
        1,
        [0, 1, 2, 3]
    ),
    'finishedby_ip': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[______]....+∞
        right: -∞...........X....+∞
        final: -∞....[_____].....+∞
        """,
        ProcSet((0, 7)),
        ProcSet(7),
        7,
        1,
        [0, 1, 2, 3, 4, 5, 6]
    ),
    'contains_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[______]....+∞
        right: -∞......[__]......+∞
        final: -∞....[]....[]....+∞
        """,
        ProcSet((0, 7)),
        ProcSet((2, 5)),
        4,
        2,
        [0, 1, 6, 7]
    ),
    'contains_ip': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[______]....+∞
        right: -∞........X.......+∞
        final: -∞....[__].[_]....+∞
        """,
        ProcSet((0, 7)),
        ProcSet(4),
        7,
        2,
        [0, 1, 2, 3, 5, 6, 7]
    ),
    'startedby_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[______]....+∞
        right: -∞....[__]........+∞
        final: -∞........[__]....+∞
        """,
        ProcSet((0, 7)),
        ProcSet((0, 3)),
        4,
        1,
        [4, 5, 6, 7]
    ),
    'startedby_ip': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[______]....+∞
        right: -∞....X...........+∞
        final: -∞.....[_____]....+∞
        """,
        ProcSet((0, 7)),
        ProcSet(0),
        7,
        1,
        [1, 2, 3, 4, 5, 6, 7]
    ),
    'overlappedby_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞.......[___]....+∞
        right: -∞....[____]......+∞
        final: -∞..........[]....+∞
        """,
        ProcSet((3, 7)),
        ProcSet((0, 5)),
        2,
        1,
        [6, 7]
    ),
    'metby_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[___].......+∞
        right: -∞........[__]....+∞
        final: -∞....[__]........+∞
        """,
        ProcSet((0, 4)),
        ProcSet((4, 7)),
        4,
        1,
        [0, 1, 2, 3]
    ),
    'after_ii_notouch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞..........[]....+∞
        right: -∞......[]........+∞
        final: -∞..........[]....+∞
        """,
        ProcSet((6, 7)),
        ProcSet((2, 3)),
        2,
        1,
        [6, 7]
    ),
    'after_pi_notouch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞.........X......+∞
        right: -∞....[__]........+∞
        final: -∞.........X......+∞
        """,
        ProcSet(5),
        ProcSet((0, 3)),
        1,
        1,
        [5]
    ),
    'after_ip_notouch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞........[__]....+∞
        right: -∞....X...........+∞
        final: -∞........[__]....+∞
        """,
        ProcSet((4, 7)),
        ProcSet(0),
        4,
        1,
        [4, 5, 6, 7]
    ),
    'after_pp_notouch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞.......X........+∞
        right: -∞....X...........+∞
        final: -∞.......X........+∞
        """,
        ProcSet(3),
        ProcSet(0),
        1,
        1,
        [3]
    ),
    'after_ii_touch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞..........[]....+∞
        right: -∞......[__]......+∞
        final: -∞..........[]....+∞
        """,
        ProcSet((6, 7)),
        ProcSet((2, 5)),
        2,
        1,
        [6, 7]
    ),
    'after_pi_touch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞.........X......+∞
        right: -∞....[___].......+∞
        final: -∞.........X......+∞
        """,
        ProcSet(5),
        ProcSet((0, 4)),
        1,
        1,
        [5]
    ),
    'after_ip_touch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞........[__]....+∞
        right: -∞.......X........+∞
        final: -∞........[__]....+∞
        """,
        ProcSet((4, 7)),
        ProcSet(3),
        4,
        1,
        [4, 5, 6, 7]
    ),
    'after_pp_touch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞.......X........+∞
        right: -∞......X.........+∞
        final: -∞.......X........+∞
        """,
        ProcSet(3),
        ProcSet(2),
        1,
        1,
        [3]
    ),
    'firstempty_i': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞................+∞
        right: -∞......[__]......+∞
        final: -∞................+∞
        """,
        ProcSet(),
        ProcSet((2, 5)),
        0,
        0,
        []
    ),
    'firstempy_p': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞................+∞
        right: -∞.......X........+∞
        final: -∞................+∞
        """,
        ProcSet(),
        ProcSet(3),
        0,
        0,
        []
    ),
    'secondempty_i': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞......[__]......+∞
        right: -∞................+∞
        final: -∞......[__]......+∞
        """,
        ProcSet((2, 5)),
        ProcSet(),
        4,
        1,
        [2, 3, 4, 5]
    ),
    'secondempty_p': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞.......X........+∞
        right: -∞................+∞
        final: -∞.......X........+∞
        """,
        ProcSet(3),
        ProcSet(),
        1,
        1,
        [3]
    ),
    'bothempty': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞................+∞
        right: -∞................+∞
        final: -∞................+∞
        """,
        ProcSet(),
        ProcSet(),
        0,
        0,
        []
    ),
}
intersection_testcases = {
    'before_ii_notouch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[__]........+∞
        right: -∞.........[_]....+∞
        final: -∞................+∞
        """,
        ProcSet((0, 3)),
        ProcSet((5, 7)),
        0,
        0,
        []
    ),
    'before_ip_notouch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[__]........+∞
        right: -∞...........X....+∞
        final: -∞................+∞
        """,
        ProcSet((0, 3)),
        ProcSet(7),
        0,
        0,
        []
    ),
    'before_pi_notouch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....X...........+∞
        right: -∞........[__]....+∞
        final: -∞................+∞
        """,
        ProcSet(0),
        ProcSet((4, 7)),
        0,
        0,
        []
    ),
    'before_pp_notouch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....X...........+∞
        right: -∞........X.......+∞
        final: -∞................+∞
        """,
        ProcSet(0),
        ProcSet(4),
        0,
        0,
        []
    ),
    'before_ii_touch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[__]........+∞
        right: -∞........[__]....+∞
        final: -∞................+∞
        """,
        ProcSet((0, 3)),
        ProcSet((4, 7)),
        0,
        0,
        []
    ),
    'before_ip_touch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[__]........+∞
        right: -∞........X.......+∞
        final: -∞................+∞
        """,
        ProcSet((0, 3)),
        ProcSet(4),
        0,
        0,
        []
    ),
    'before_pi_touch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....X...........+∞
        right: -∞.....[_]........+∞
        final: -∞................+∞
        """,
        ProcSet(0),
        ProcSet((1, 3)),
        0,
        0,
        []
    ),
    'before_pp_touch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....X...........+∞
        right: -∞.....X..........+∞
        final: -∞................+∞
        """,
        ProcSet(0),
        ProcSet(1),
        0,
        0,
        []
    ),
    'meets_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[__]........+∞
        right: -∞.......[___]....+∞
        final: -∞.......X........+∞
        """,
        ProcSet((0, 3)),
        ProcSet((3, 7)),
        1,
        1,
        [3]
    ),
    'overlaps_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[____]......+∞
        right: -∞......[____]....+∞
        final: -∞......[__]......+∞
        """,
        ProcSet((0, 5)),
        ProcSet((2, 7)),
        4,
        1,
        [2, 3, 4, 5]
    ),
    'starts_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[__]........+∞
        right: -∞....[______]....+∞
        final: -∞....[__]........+∞
        """,
        ProcSet((0, 3)),
        ProcSet((0, 7)),
        4,
        1,
        [0, 1, 2, 3]
    ),
    'starts_pi': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....X...........+∞
        right: -∞....[__]........+∞
        final: -∞....X...........+∞
        """,
        ProcSet(0),
        ProcSet((0, 3)),
        1,
        1,
        [0]
    ),
    'containedby_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞......[__]......+∞
        right: -∞....[______]....+∞
        final: -∞......[__]......+∞
        """,
        ProcSet((2, 5)),
        ProcSet((0, 7)),
        4,
        1,
        [2, 3, 4, 5]
    ),
    'containedby_pi': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞.......X........+∞
        right: -∞....[______]....+∞
        final: -∞.......X........+∞
        """,
        ProcSet(3),
        ProcSet((0, 7)),
        1,
        1,
        [3]
    ),
    'finishes_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞........[__]....+∞
        right: -∞....[______]....+∞
        final: -∞........[__]....+∞
        """,
        ProcSet((4, 7)),
        ProcSet((0, 7)),
        4,
        1,
        [4, 5, 6, 7]
    ),
    'finishes_pi': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞.......X........+∞
        right: -∞....[__]........+∞
        final: -∞.......X........+∞
        """,
        ProcSet(3),
        ProcSet((0, 3)),
        1,
        1,
        [3]
    ),
    'equal_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[__]........+∞
        right: -∞....[__]........+∞
        final: -∞....[__]........+∞
        """,
        ProcSet((0, 3)),
        ProcSet((0, 3)),
        4,
        1,
        [0, 1, 2, 3]
    ),
    'equal_pp': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....X...........+∞
        right: -∞....X...........+∞
        final: -∞....X...........+∞
        """,
        ProcSet(0),
        ProcSet(0),
        1,
        1,
        [0]
    ),
    'finishedby_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[______]....+∞
        right: -∞........[__]....+∞
        final: -∞........[__]....+∞
        """,
        ProcSet((0, 7)),
        ProcSet((4, 7)),
        4,
        1,
        [4, 5, 6, 7]
    ),
    'finishedby_ip': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[______]....+∞
        right: -∞...........X....+∞
        final: -∞...........X....+∞
        """,
        ProcSet((0, 7)),
        ProcSet(7),
        1,
        1,
        [7]
    ),
    'contains_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[______]....+∞
        right: -∞......[__]......+∞
        final: -∞......[__]......+∞
        """,
        ProcSet((0, 7)),
        ProcSet((2, 5)),
        4,
        1,
        [2, 3, 4, 5]
    ),
    'contains_ip': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[______]....+∞
        right: -∞........X.......+∞
        final: -∞........X.......+∞
        """,
        ProcSet((0, 7)),
        ProcSet(4),
        1,
        1,
        [4]
    ),
    'startedby_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[______]....+∞
        right: -∞....[__]........+∞
        final: -∞....[__]........+∞
        """,
        ProcSet((0, 7)),
        ProcSet((0, 3)),
        4,
        1,
        [0, 1, 2, 3]
    ),
    'startedby_ip': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[______]....+∞
        right: -∞....X...........+∞
        final: -∞....X...........+∞
        """,
        ProcSet((0, 7)),
        ProcSet(0),
        1,
        1,
        [0]
    ),
    'overlappedby_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞.......[___]....+∞
        right: -∞....[____]......+∞
        final: -∞.......[_]......+∞
        """,
        ProcSet((3, 7)),
        ProcSet((0, 5)),
        3,
        1,
        [3, 4, 5]
    ),
    'metby_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[___].......+∞
        right: -∞........[__]....+∞
        final: -∞........X.......+∞
        """,
        ProcSet((0, 4)),
        ProcSet((4, 7)),
        1,
        1,
        [4]
    ),
    'after_ii_notouch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞..........[]....+∞
        right: -∞......[]........+∞
        final: -∞................+∞
        """,
        ProcSet((6, 7)),
        ProcSet((2, 3)),
        0,
        0,
        []
    ),
    'after_pi_notouch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞.........X......+∞
        right: -∞....[__]........+∞
        final: -∞................+∞
        """,
        ProcSet(5),
        ProcSet((0, 3)),
        0,
        0,
        []
    ),
    'after_ip_notouch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞........[__]....+∞
        right: -∞....X...........+∞
        final: -∞................+∞
        """,
        ProcSet((4, 7)),
        ProcSet(0),
        0,
        0,
        []
    ),
    'after_pp_notouch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞.......X........+∞
        right: -∞....X...........+∞
        final: -∞................+∞
        """,
        ProcSet(3),
        ProcSet(0),
        0,
        0,
        []
    ),
    'after_ii_touch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞..........[]....+∞
        right: -∞......[__]......+∞
        final: -∞................+∞
        """,
        ProcSet((6, 7)),
        ProcSet((2, 5)),
        0,
        0,
        []
    ),
    'after_pi_touch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞.........X......+∞
        right: -∞....[___].......+∞
        final: -∞................+∞
        """,
        ProcSet(5),
        ProcSet((0, 4)),
        0,
        0,
        []
    ),
    'after_ip_touch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞........[__]....+∞
        right: -∞.......X........+∞
        final: -∞................+∞
        """,
        ProcSet((4, 7)),
        ProcSet(3),
        0,
        0,
        []
    ),
    'after_pp_touch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞.......X........+∞
        right: -∞......X.........+∞
        final: -∞................+∞
        """,
        ProcSet(3),
        ProcSet(2),
        0,
        0,
        []
    ),
    'firstempty_i': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞................+∞
        right: -∞......[__]......+∞
        final: -∞................+∞
        """,
        ProcSet(),
        ProcSet((2, 5)),
        0,
        0,
        []
    ),
    'firstempy_p': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞................+∞
        right: -∞.......X........+∞
        final: -∞................+∞
        """,
        ProcSet(),
        ProcSet(3),
        0,
        0,
        []
    ),
    'secondempty_i': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞......[__]......+∞
        right: -∞................+∞
        final: -∞................+∞
        """,
        ProcSet((2, 5)),
        ProcSet(),
        0,
        0,
        []
    ),
    'secondempty_p': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞.......X........+∞
        right: -∞................+∞
        final: -∞................+∞
        """,
        ProcSet(3),
        ProcSet(),
        0,
        0,
        []
    ),
    'bothempty': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞................+∞
        right: -∞................+∞
        final: -∞................+∞
        """,
        ProcSet(),
        ProcSet(),
        0,
        0,
        []
    ),
}
symmetric_difference_testcases = {
    'before_ii_notouch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[__]........+∞
        right: -∞.........[_]....+∞
        final: -∞....[__] [_]....+∞
        """,
        ProcSet((0, 3)),
        ProcSet((5, 7)),
        7,
        2,
        [0, 1, 2, 3, 5, 6, 7]
    ),
    'before_ip_notouch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[__]........+∞
        right: -∞...........X....+∞
        final: -∞....[__]...X....+∞
        """,
        ProcSet((0, 3)),
        ProcSet(7),
        5,
        2,
        [0, 1, 2, 3, 7]
    ),
    'before_pi_notouch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....X...........+∞
        right: -∞........[__]....+∞
        final: -∞....X...[__]....+∞
        """,
        ProcSet(0),
        ProcSet((4, 7)),
        5,
        2,
        [0, 4, 5, 6, 7]
    ),
    'before_pp_notouch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....X...........+∞
        right: -∞........X.......+∞
        final: -∞....X...X.......+∞
        """,
        ProcSet(0),
        ProcSet(4),
        2,
        2,
        [0, 4]
    ),
    'before_ii_touch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[__]........+∞
        right: -∞........[__]....+∞
        final: -∞....[______]....+∞
        """,
        ProcSet((0, 3)),
        ProcSet((4, 7)),
        8,
        1,
        [0, 1, 2, 3, 4, 5, 6, 7]
    ),
    'before_ip_touch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[__]........+∞
        right: -∞........X.......+∞
        final: -∞....[___].......+∞
        """,
        ProcSet((0, 3)),
        ProcSet(4),
        5,
        1,
        [0, 1, 2, 3, 4]
    ),
    'before_pi_touch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....X...........+∞
        right: -∞.....[_]........+∞
        final: -∞....[__]........+∞
        """,
        ProcSet(0),
        ProcSet((1, 3)),
        4,
        1,
        [0, 1, 2, 3]
    ),
    'before_pp_touch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....X...........+∞
        right: -∞.....X..........+∞
        final: -∞....[]..........+∞
        """,
        ProcSet(0),
        ProcSet(1),
        2,
        1,
        [0, 1]
    ),
    'meets_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[__]........+∞
        right: -∞.......[___]....+∞
        final: -∞....[_].[__]....+∞
        """,
        ProcSet((0, 3)),
        ProcSet((3, 7)),
        7,
        2,
        [0, 1, 2, 4, 5, 6, 7]
    ),
    'overlaps_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[____]......+∞
        right: -∞......[____]....+∞
        final: -∞....[]....[]....+∞
        """,
        ProcSet((0, 5)),
        ProcSet((2, 7)),
        4,
        2,
        [0, 1, 6, 7]
    ),
    'starts_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[__]........+∞
        right: -∞....[______]....+∞
        final: -∞........[__]....+∞
        """,
        ProcSet((0, 3)),
        ProcSet((0, 7)),
        4,
        1,
        [4, 5, 6, 7]
    ),
    'starts_pi': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....X...........+∞
        right: -∞....[__]........+∞
        final: -∞.....[_]........+∞
        """,
        ProcSet(0),
        ProcSet((0, 3)),
        3,
        1,
        [1, 2, 3]
    ),
    'containedby_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞......[__]......+∞
        right: -∞....[______]....+∞
        final: -∞....[]....[]....+∞
        """,
        ProcSet((2, 5)),
        ProcSet((0, 7)),
        4,
        2,
        [0, 1, 6, 7]
    ),
    'containedby_pi': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞.......X........+∞
        right: -∞....[______]....+∞
        final: -∞....[_].[__]....+∞
        """,
        ProcSet(3),
        ProcSet((0, 7)),
        7,
        2,
        [0, 1, 2, 4, 5, 6, 7]
    ),
    'finishes_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞........[__]....+∞
        right: -∞....[______]....+∞
        final: -∞....[__]........+∞
        """,
        ProcSet((4, 7)),
        ProcSet((0, 7)),
        4,
        1,
        [0, 1, 2, 3]
    ),
    'finishes_pi': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞.......X........+∞
        right: -∞....[__]........+∞
        final: -∞....[_].........+∞
        """,
        ProcSet(3),
        ProcSet((0, 3)),
        3,
        1,
        [0, 1, 2]
    ),
    'equal_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[__]........+∞
        right: -∞....[__]........+∞
        final: -∞................+∞
        """,
        ProcSet((0, 3)),
        ProcSet((0, 3)),
        0,
        0,
        []
    ),
    'equal_pp': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....X...........+∞
        right: -∞....X...........+∞
        final: -∞................+∞
        """,
        ProcSet(0),
        ProcSet(0),
        0,
        0,
        []
    ),
    'finishedby_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[______]....+∞
        right: -∞........[__]....+∞
        final: -∞....[__]........+∞
        """,
        ProcSet((0, 7)),
        ProcSet((4, 7)),
        4,
        1,
        [0, 1, 2, 3]
    ),
    'finishedby_ip': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[______]....+∞
        right: -∞...........X....+∞
        final: -∞....[_____].....+∞
        """,
        ProcSet((0, 7)),
        ProcSet(7),
        7,
        1,
        [0, 1, 2, 3, 4, 5, 6]
    ),
    'contains_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[______]....+∞
        right: -∞......[__]......+∞
        final: -∞....[]....[]....+∞
        """,
        ProcSet((0, 7)),
        ProcSet((2, 5)),
        4,
        2,
        [0, 1, 6, 7]
    ),
    'contains_ip': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[______]....+∞
        right: -∞........X.......+∞
        final: -∞....[__].[_]....+∞
        """,
        ProcSet((0, 7)),
        ProcSet(4),
        7,
        2,
        [0, 1, 2, 3, 5, 6, 7]
    ),
    'startedby_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[______]....+∞
        right: -∞....[__]........+∞
        final: -∞........[__]....+∞
        """,
        ProcSet((0, 7)),
        ProcSet((0, 3)),
        4,
        1,
        [4, 5, 6, 7]
    ),
    'startedby_ip': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[______]....+∞
        right: -∞....X...........+∞
        final: -∞.....[_____]....+∞
        """,
        ProcSet((0, 7)),
        ProcSet(0),
        7,
        1,
        [1, 2, 3, 4, 5, 6, 7]
    ),
    'overlappedby_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞.......[___]....+∞
        right: -∞....[____]......+∞
        final: -∞....[_]...[]....+∞
        """,
        ProcSet((3, 7)),
        ProcSet((0, 5)),
        5,
        2,
        [0, 1, 2, 6, 7]
    ),
    'metby_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[___].......+∞
        right: -∞........[__]....+∞
        final: -∞....[__].[_]....+∞
        """,
        ProcSet((0, 4)),
        ProcSet((4, 7)),
        7,
        2,
        [0, 1, 2, 3, 5, 6, 7]
    ),
    'after_ii_notouch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞..........[]....+∞
        right: -∞......[]........+∞
        final: -∞......[]..[]....+∞
        """,
        ProcSet((6, 7)),
        ProcSet((2, 3)),
        4,
        2,
        [2, 3, 6, 7]
    ),
    'after_pi_notouch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞.........X......+∞
        right: -∞....[__]........+∞
        final: -∞....[__].X......+∞
        """,
        ProcSet(5),
        ProcSet((0, 3)),
        5,
        2,
        [0, 1, 2, 3, 5]
    ),
    'after_ip_notouch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞........[__]....+∞
        right: -∞....X...........+∞
        final: -∞....X...[__]....+∞
        """,
        ProcSet((4, 7)),
        ProcSet(0),
        5,
        2,
        [0, 4, 5, 6, 7]
    ),
    'after_pp_notouch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞.......X........+∞
        right: -∞....X...........+∞
        final: -∞....X..X........+∞
        """,
        ProcSet(3),
        ProcSet(0),
        2,
        2,
        [0, 3]
    ),
    'after_ii_touch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞..........[]....+∞
        right: -∞......[__]......+∞
        final: -∞......[____]....+∞
        """,
        ProcSet((6, 7)),
        ProcSet((2, 5)),
        6,
        1,
        [2, 3, 4, 5, 6, 7]
    ),
    'after_pi_touch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞.........X......+∞
        right: -∞....[___].......+∞
        final: -∞....[____]......+∞
        """,
        ProcSet(5),
        ProcSet((0, 4)),
        6,
        1,
        [0, 1, 2, 3, 4, 5]
    ),
    'after_ip_touch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞........[__]....+∞
        right: -∞.......X........+∞
        final: -∞.......[___]....+∞
        """,
        ProcSet((4, 7)),
        ProcSet(3),
        5,
        1,
        [3, 4, 5, 6, 7]
    ),
    'after_pp_touch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞.......X........+∞
        right: -∞......X.........+∞
        final: -∞......[]........+∞
        """,
        ProcSet(3),
        ProcSet(2),
        2,
        1,
        [2, 3]
    ),
    'firstempty_i': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞................+∞
        right: -∞......[__]......+∞
        final: -∞......[__]......+∞
        """,
        ProcSet(),
        ProcSet((2, 5)),
        4,
        1,
        [2, 3, 4, 5]
    ),
    'firstempy_p': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞................+∞
        right: -∞.......X........+∞
        final: -∞.......X........+∞
        """,
        ProcSet(),
        ProcSet(3),
        1,
        1,
        [3]
    ),
    'secondempty_i': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞......[__]......+∞
        right: -∞................+∞
        final: -∞......[__]......+∞
        """,
        ProcSet((2, 5)),
        ProcSet(),
        4,
        1,
        [2, 3, 4, 5]
    ),
    'secondempty_p': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞.......X........+∞
        right: -∞................+∞
        final: -∞.......X........+∞
        """,
        ProcSet(3),
        ProcSet(),
        1,
        1,
        [3]
    ),
    'bothempty': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞................+∞
        right: -∞................+∞
        final: -∞................+∞
        """,
        ProcSet(),
        ProcSet(),
        0,
        0,
        []
    ),
}
union_testcases = {
    'before_ii_notouch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[__]........+∞
        right: -∞.........[_]....+∞
        final: -∞....[__].[_]....+∞
        """,
        ProcSet((0, 3)),
        ProcSet((5, 7)),
        7,
        2,
        [0, 1, 2, 3, 5, 6, 7]
    ),
    'before_ip_notouch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[__]........+∞
        right: -∞...........X....+∞
        final: -∞....[__]...X....+∞
        """,
        ProcSet((0, 3)),
        ProcSet(7),
        5,
        2,
        [0, 1, 2, 3, 7]
    ),
    'before_pi_notouch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....X...........+∞
        right: -∞........[__]....+∞
        final: -∞....X...[__]....+∞
        """,
        ProcSet(0),
        ProcSet((4, 7)),
        5,
        2,
        [0, 4, 5, 6, 7]
    ),
    'before_pp_notouch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....X...........+∞
        right: -∞........X.......+∞
        final: -∞....X...X.......+∞
        """,
        ProcSet(0),
        ProcSet(4),
        2,
        2,
        [0, 4]
    ),
    'before_ii_touch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[__]........+∞
        right: -∞........[__]....+∞
        final: -∞....[______]....+∞
        """,
        ProcSet((0, 3)),
        ProcSet((4, 7)),
        8,
        1,
        [0, 1, 2, 3, 4, 5, 6, 7]
    ),
    'before_ip_touch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[__]........+∞
        right: -∞........X.......+∞
        final: -∞....[___].......+∞
        """,
        ProcSet((0, 3)),
        ProcSet(4),
        5,
        1,
        [0, 1, 2, 3, 4]
    ),
    'before_pi_touch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....X...........+∞
        right: -∞.....[_]........+∞
        final: -∞....[__]........+∞
        """,
        ProcSet(0),
        ProcSet((1, 3)),
        4,
        1,
        [0, 1, 2, 3]
    ),
    'before_pp_touch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....X...........+∞
        right: -∞.....X..........+∞
        final: -∞....[]..........+∞
        """,
        ProcSet(0),
        ProcSet(1),
        2,
        1,
        [0, 1]
    ),
    'meets_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[__]........+∞
        right: -∞.......[___]....+∞
        final: -∞....[______]....+∞
        """,
        ProcSet((0, 3)),
        ProcSet((3, 7)),
        8,
        1,
        [0, 1, 2, 3, 4, 5, 6, 7]
    ),
    'overlaps_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[____]......+∞
        right: -∞......[____]....+∞
        final: -∞....[______]....+∞
        """,
        ProcSet((0, 5)),
        ProcSet((2, 7)),
        8,
        1,
        [0, 1, 2, 3, 4, 5, 6, 7]
    ),
    'starts_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[__]........+∞
        right: -∞....[______]....+∞
        final: -∞....[______]....+∞
        """,
        ProcSet((0, 3)),
        ProcSet((0, 7)),
        8,
        1,
        [0, 1, 2, 3, 4, 5, 6, 7]
    ),
    'starts_pi': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....X...........+∞
        right: -∞....[__]........+∞
        final: -∞....[__]........+∞
        """,
        ProcSet(0),
        ProcSet((0, 3)),
        4,
        1,
        [0, 1, 2, 3]
    ),
    'containedby_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞......[__]......+∞
        right: -∞....[______]....+∞
        final: -∞....[______]....+∞
        """,
        ProcSet((2, 5)),
        ProcSet((0, 7)),
        8,
        1,
        [0, 1, 2, 3, 4, 5, 6, 7]
    ),
    'containedby_pi': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞.......X........+∞
        right: -∞....[______]....+∞
        final: -∞....[______]....+∞
        """,
        ProcSet(3),
        ProcSet((0, 7)),
        8,
        1,
        [0, 1, 2, 3, 4, 5, 6, 7]
    ),
    'finishes_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞........[__]....+∞
        right: -∞....[______]....+∞
        final: -∞....[______]....+∞
        """,
        ProcSet((4, 7)),
        ProcSet((0, 7)),
        8,
        1,
        [0, 1, 2, 3, 4, 5, 6, 7]
    ),
    'finishes_pi': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞.......X........+∞
        right: -∞....[__]........+∞
        final: -∞....[__]........+∞
        """,
        ProcSet(3),
        ProcSet((0, 3)),
        4,
        1,
        [0, 1, 2, 3]
    ),
    'equal_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[__]........+∞
        right: -∞....[__]........+∞
        final: -∞....[__]........+∞
        """,
        ProcSet((0, 3)),
        ProcSet((0, 3)),
        4,
        1,
        [0, 1, 2, 3]
    ),
    'equal_pp': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....X...........+∞
        right: -∞....X...........+∞
        final: -∞....X...........+∞
        """,
        ProcSet(0),
        ProcSet(0),
        1,
        1,
        [0]
    ),
    'finishedby_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[______]....+∞
        right: -∞........[__]....+∞
        final: -∞....[______]....+∞
        """,
        ProcSet((0, 7)),
        ProcSet((4, 7)),
        8,
        1,
        [0, 1, 2, 3, 4, 5, 6, 7]
    ),
    'finishedby_ip': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[______]....+∞
        right: -∞...........X....+∞
        final: -∞....[______]....+∞
        """,
        ProcSet((0, 7)),
        ProcSet(7),
        8,
        1,
        [0, 1, 2, 3, 4, 5, 6, 7]
    ),
    'contains_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[______]....+∞
        right: -∞......[__]......+∞
        final: -∞....[______]....+∞
        """,
        ProcSet((0, 7)),
        ProcSet((2, 5)),
        8,
        1,
        [0, 1, 2, 3, 4, 5, 6, 7]
    ),
    'contains_ip': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[______]....+∞
        right: -∞........X.......+∞
        final: -∞....[______]....+∞
        """,
        ProcSet((0, 7)),
        ProcSet(4),
        8,
        1,
        [0, 1, 2, 3, 4, 5, 6, 7]
    ),
    'startedby_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[______]....+∞
        right: -∞....[__]........+∞
        final: -∞....[______]....+∞
        """,
        ProcSet((0, 7)),
        ProcSet((0, 3)),
        8,
        1,
        [0, 1, 2, 3, 4, 5, 6, 7]
    ),
    'startedby_ip': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[______]....+∞
        right: -∞....X...........+∞
        final: -∞....[______]....+∞
        """,
        ProcSet((0, 7)),
        ProcSet(0),
        8,
        1,
        [0, 1, 2, 3, 4, 5, 6, 7]
    ),
    'overlappedby_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞.......[___]....+∞
        right: -∞....[____]......+∞
        final: -∞....[______]....+∞
        """,
        ProcSet((3, 7)),
        ProcSet((0, 5)),
        8,
        1,
        [0, 1, 2, 3, 4, 5, 6, 7]
    ),
    'metby_ii': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞....[___].......+∞
        right: -∞........[__]....+∞
        final: -∞....[______]....+∞
        """,
        ProcSet((0, 4)),
        ProcSet((4, 7)),
        8,
        1,
        [0, 1, 2, 3, 4, 5, 6, 7]
    ),
    'after_ii_notouch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞..........[]....+∞
        right: -∞......[]........+∞
        final: -∞......[]..[]....+∞
        """,
        ProcSet((6, 7)),
        ProcSet((2, 3)),
        4,
        2,
        [2, 3, 6, 7]
    ),
    'after_pi_notouch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞.........X......+∞
        right: -∞....[__]........+∞
        final: -∞....[__].X......+∞
        """,
        ProcSet(5),
        ProcSet((0, 3)),
        5,
        2,
        [0, 1, 2, 3, 5]
    ),
    'after_ip_notouch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞........[__]....+∞
        right: -∞....X...........+∞
        final: -∞....X...[__]....+∞
        """,
        ProcSet((4, 7)),
        ProcSet(0),
        5,
        2,
        [0, 4, 5, 6, 7]
    ),
    'after_pp_notouch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞.......X........+∞
        right: -∞....X...........+∞
        final: -∞....X..X........+∞
        """,
        ProcSet(3),
        ProcSet(0),
        2,
        2,
        [0, 3]
    ),
    'after_ii_touch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞..........[]....+∞
        right: -∞......[__]......+∞
        final: -∞......[____]....+∞
        """,
        ProcSet((6, 7)),
        ProcSet((2, 5)),
        6,
        1,
        [2, 3, 4, 5, 6, 7]
    ),
    'after_pi_touch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞.........X......+∞
        right: -∞....[___].......+∞
        final: -∞....[____]......+∞
        """,
        ProcSet(5),
        ProcSet((0, 4)),
        6,
        1,
        [0, 1, 2, 3, 4, 5]
    ),
    'after_ip_touch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞........[__]....+∞
        right: -∞.......X........+∞
        final: -∞.......[___]....+∞
        """,
        ProcSet((4, 7)),
        ProcSet(3),
        5,
        1,
        [3, 4, 5, 6, 7]
    ),
    'after_pp_touch': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞.......X........+∞
        right: -∞......X.........+∞
        final: -∞......[]........+∞
        """,
        ProcSet(3),
        ProcSet(2),
        2,
        1,
        [2, 3]
    ),
    'firstempty_i': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞................+∞
        right: -∞......[__]......+∞
        final: -∞......[__]......+∞
        """,
        ProcSet(),
        ProcSet((2, 5)),
        4,
        1,
        [2, 3, 4, 5]
    ),
    'firstempy_p': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞................+∞
        right: -∞.......X........+∞
        final: -∞.......X........+∞
        """,
        ProcSet(),
        ProcSet(3),
        1,
        1,
        [3]
    ),
    'secondempty_i': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞......[__]......+∞
        right: -∞................+∞
        final: -∞......[__]......+∞
        """,
        ProcSet((2, 5)),
        ProcSet(),
        4,
        1,
        [2, 3, 4, 5]
    ),
    'secondempty_p': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞.......X........+∞
        right: -∞................+∞
        final: -∞.......X........+∞
        """,
        ProcSet(3),
        ProcSet(),
        1,
        1,
        [3]
    ),
    'bothempty': _TestCase(
        """
               -∞....01234567....+∞
        left:  -∞................+∞
        right: -∞................+∞
        final: -∞................+∞
        """,
        ProcSet(),
        ProcSet(),
        0,
        0,
        []
    ),
}


# actual test classes

TestMergeDifference = build_test_class(
    'TestMergeDifference',
    operator.__sub__,
    difference_testcases,
    build_merge_test
)

TestMergeIntersection = build_test_class(
    'TestMergeIntersection',
    operator.__and__,
    intersection_testcases,
    build_merge_test
)

TestMergeSymmetricDifference = build_test_class(
    'TestMergeSymmetricDifference',
    operator.__xor__,
    symmetric_difference_testcases,
    build_merge_test
)

TestMergeUnion = build_test_class(
    'TestMergeUnion',
    operator.__or__,
    union_testcases,
    build_merge_test
)
