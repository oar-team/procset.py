# -*- coding: utf-8 -*-

import pytest
from procset import ProcInt, ProcSet


# pylint: disable=no-self-use,too-many-public-methods
class TestNew:
    def test_empty(self):
        pset = ProcSet()
        assert list(pset) == []
        assert len(pset) == 0
        assert pset.count() == 0

    def test_empty_iter(self):
        pset = ProcSet(*[])
        assert list(pset) == []
        assert len(pset) == 0
        assert pset.count() == 0

    def test_single_procint(self):
        pset = ProcSet(ProcInt(0, 3))
        assert list(pset) == [0, 1, 2, 3]
        assert len(pset) == 4
        assert pset.count() == 1

    def test_single_tuple(self):
        pset = ProcSet((0, 3))
        assert list(pset) == [0, 1, 2, 3]
        assert len(pset) == 4
        assert pset.count() == 1

    def test_many_procint(self):
        pset = ProcSet(ProcInt(0, 3), ProcInt(2, 3))
        assert list(pset) == [0, 1, 2, 3]
        assert len(pset) == 4
        assert pset.count() == 1

    def test_disjoint_tuple_iter(self):
        itvs = [(0, 1), (4, 7)]
        pset = ProcSet(*itvs)
        assert list(pset) == [0, 1, 4, 5, 6, 7]
        assert len(pset) == 6
        assert pset.count() == 2

    def test_mixed_itvs(self):
        pset = ProcSet(ProcInt(0, 3), (2, 3), [4, 7])
        assert list(pset) == [0, 1, 2, 3, 4, 5, 6, 7]
        assert len(pset) == 8
        assert pset.count() == 1

    def test_bad_iter(self):
        with pytest.raises(ValueError):
            ProcSet([])

    def test_single_int(self):
        pset = ProcSet(0)
        assert list(pset) == [0]
        assert len(pset) == 1
        assert pset.count() == 1

    def test_many_ints(self):
        pset = ProcSet(0, 1, 2)
        assert list(pset) == [0, 1, 2]
        assert len(pset) == 3
        assert pset.count() == 1

    def test_mixed_procint_int(self):
        pset = ProcSet(0, (2, 3))
        assert list(pset) == [0, 2, 3]
        assert len(pset) == 3
        assert pset.count() == 2

    def test_incompatible_string(self):
        # string are iterable but incompatible
        with pytest.raises(ValueError):
            ProcSet('1')  # caught because length < 1
        with pytest.raises(TypeError):
            ProcSet('12')  # caught because not an int
        with pytest.raises(ValueError):
            ProcSet('1-2')  # caught because length is > 2

    def test_bad_noiter(self):
        with pytest.raises(TypeError):
            ProcSet(None)


# pylint: disable=no-self-use,too-many-public-methods
class TestMisc:
    def test_equal(self):
        pset1 = ProcSet(ProcInt(0, 0))
        pset2 = ProcSet(ProcInt(0, 0))
        assert id(pset1) != id(pset2)
        assert pset1 == pset2

    def test_noequal(self):
        pset1 = ProcSet(ProcInt(0, 0))
        pset2 = ProcSet(ProcInt(0, 1))
        assert id(pset1) != id(pset2)
        assert pset1 != pset2


# pylint: disable=no-self-use,too-many-public-methods
class TestStringParsing:
    def test_empty(self):
        pset = ProcSet.from_str('')
        assert pset == ProcSet()

    def test_single_point(self):
        pset = ProcSet.from_str('0')
        assert pset == ProcSet(0)

    def test_contiguous(self):
        pset = ProcSet.from_str('0-3')
        assert pset == ProcSet(ProcInt(0, 3))

    def test_disjoint_pp(self):
        pset = ProcSet.from_str('1 2')
        assert pset == ProcSet(1, 2)

    def test_disjoint_ip(self):
        pset = ProcSet.from_str('0-1 2')
        assert pset == ProcSet(ProcInt(0, 1), 2)

    def test_disjoint_ii(self):
        pset = ProcSet.from_str('0-1 2-3')
        assert pset == ProcSet(ProcInt(0, 3))

    def test_nostring(self):
        with pytest.raises(TypeError, message='from_str() argument 2 must be str, not int'):
            ProcSet.from_str(42)

    def test_missing_left(self):
        with pytest.raises(ValueError, message='Invalid interval format, parsed string is: -1'):
            ProcSet.from_str('-1')

    def test_missing_right(self):
        with pytest.raises(ValueError, message='Invalid interval format, parsed string is: 0-'):
            ProcSet.from_str('0-')

    def test_many_contig(self):
        with pytest.raises(ValueError, message='Invalid interval format, parsed string is: 1-2-3'):
            ProcSet.from_str('1-2-3')


# pylint: disable=no-self-use,too-many-public-methods
class TestDisplay:
    def test_empty(self):
        pset = ProcSet()
        assert str(pset) == ''
        assert format(pset, ':,') == ''
        assert format(pset) == str(pset)
        assert format(pset, '') == str(pset)

    def test_single_point(self):
        pset = ProcSet(ProcInt(0, 0))
        assert str(pset) == '0'
        assert format(pset, ':,') == '0'
        assert format(pset) == str(pset)
        assert format(pset, '') == str(pset)

    def test_contiguous(self):
        pset = ProcSet(ProcInt(0, 7))
        assert str(pset) == '0-7'
        assert format(pset, ':,') == '0:7'
        assert format(pset) == str(pset)
        assert format(pset, '') == str(pset)

    def test_disjoint(self):
        pset = ProcSet(ProcInt(0, 3), ProcInt(7, 15))
        assert str(pset) == '0-3 7-15'
        assert format(pset, ':,') == '0:3,7:15'
        assert format(pset) == str(pset)
        assert format(pset, '') == str(pset)

    def test_bad_format_spec_short(self):
        with pytest.raises(ValueError, message='Invalid format specifier'):
            format(ProcSet(), ';')

    def test_bad_format_spec_long(self):
        with pytest.raises(ValueError, message='Invalid format specifier'):
            format(ProcSet(), ':--')


# pylint: disable=no-self-use,too-many-public-methods
class TestAdd:
    def test_empty(self):
        """
        init:  -∞................+∞
        add:   -∞....[______]....+∞
        final: -∞....[______]....+∞
        """
        pset = ProcSet()
        pset.add(ProcInt(0, 7))
        assert len(pset) == 8
        assert pset.count() == 1
        assert list(pset) == [0, 1, 2, 3, 4, 5, 6, 7]

    def test_strict_subset(self):
        """
        init:  -∞....[______]....+∞
        add:   -∞......[]........+∞
        final: -∞....[______]....+∞
        """
        pset = ProcSet(ProcInt(0, 7))
        pset.add(ProcInt(2, 3))
        assert len(pset) == 8
        assert pset.count() == 1
        assert list(pset) == [0, 1, 2, 3, 4, 5, 6, 7]

    def test_strict_superset(self):
        """
        init:  -∞......[]........+∞
        add:   -∞....[______]....+∞
        final: -∞....[______]....+∞
        """
        pset = ProcSet(ProcInt(2, 3))
        pset.add(ProcInt(0, 7))
        assert len(pset) == 8
        assert pset.count() == 1
        assert list(pset) == [0, 1, 2, 3, 4, 5, 6, 7]


    def test_left_disjoint_notouch(self):
        """
        init:  -∞........[__]....+∞
        add:   -∞....[]..........+∞
        final: -∞....[]..[__]....+∞
        """
        pset = ProcSet(ProcInt(4, 7))
        pset.add(ProcInt(0, 1))
        assert len(pset) == 6
        assert pset.count() == 2
        assert list(pset) == [0, 1, 4, 5, 6, 7]

    def test_right_disjoint_notouch(self):
        """
        init:  -∞....[__]........+∞
        add:   -∞..........[]....+∞
        final: -∞....[__]..[]....+∞
        """
        pset = ProcSet(ProcInt(0, 3))
        pset.add(ProcInt(6, 7))
        assert len(pset) == 6
        assert pset.count() == 2
        assert list(pset) == [0, 1, 2, 3, 6, 7]

    def test_left_disjoint_touch(self):
        """
        init:  -∞........[__]....+∞
        add:   -∞......[]........+∞
        final: -∞......[____]....+∞
        """
        pset = ProcSet(ProcInt(4, 7))
        pset.add(ProcInt(2, 3))
        assert len(pset) == 6
        assert pset.count() == 1
        assert list(pset) == [2, 3, 4, 5, 6, 7]

    def test_right_disjoint_touch(self):
        """
        init:  -∞....[__]........+∞
        add:   -∞........[]......+∞
        final: -∞....[____]......+∞
        """
        pset = ProcSet(ProcInt(0, 3))
        pset.add(ProcInt(4, 5))
        assert len(pset) == 6
        assert pset.count() == 1
        assert list(pset) == [0, 1, 2, 3, 4, 5]

    def test_left_intersect(self):
        """
        init:  -∞......[____]....+∞
        add:   -∞....[____]......+∞
        final: -∞....[______]....+∞
        """
        pset = ProcSet(ProcInt(2, 7))
        pset.add(ProcInt(0, 5))
        assert len(pset) == 8
        assert pset.count() == 1
        assert list(pset) == [0, 1, 2, 3, 4, 5, 6, 7]

    def test_right_intersect(self):
        """
        init:  -∞....[____]......+∞
        add:   -∞......[____]....+∞
        final: -∞....[______]....+∞
        """
        pset = ProcSet(ProcInt(0, 5))
        pset.add(ProcInt(2, 7))
        assert len(pset) == 8
        assert pset.count() == 1
        assert list(pset) == [0, 1, 2, 3, 4, 5, 6, 7]

    def test_between_disjoint_notouch(self):
        """
        init:  -∞....[]....[]....+∞
        add:   -∞.......[].......+∞
        final: -∞....[].[].[]....+∞
        """
        pset = ProcSet(ProcInt(0, 1), ProcInt(6, 7))
        pset.add(ProcInt(3, 4))
        assert len(pset) == 6
        assert pset.count() == 3
        assert list(pset) == [0, 1, 3, 4, 6, 7]

    def test_between_disjoint_touch(self):
        """
        init:  -∞....[]....[]....+∞
        add:   -∞......[__]......+∞
        final: -∞....[______]....+∞
        """
        pset = ProcSet(ProcInt(0, 1), ProcInt(6, 7))
        pset.add(ProcInt(2, 5))
        assert len(pset) == 8
        assert pset.count() == 1
        assert list(pset) == [0, 1, 2, 3, 4, 5, 6, 7]

    def test_between_intersect(self):
        """
        init:  -∞....[_]..[_]....+∞
        add:   -∞.....[___]......+∞
        final: -∞....[______]....+∞
        """
        pset = ProcSet(ProcInt(0, 2), ProcInt(5, 7))
        pset.add(ProcInt(1, 5))
        assert len(pset) == 8
        assert pset.count() == 1
        assert list(pset) == [0, 1, 2, 3, 4, 5, 6, 7]

    def test_superset_left_notouch(self):
        """
        init:  -∞.....[]..[_]....+∞
        add:   -∞....[_____].....+∞
        final: -∞....[______]....+∞
        """
        pset = ProcSet(ProcInt(1, 2), ProcInt(5, 7))
        pset.add(ProcInt(0, 6))
        assert len(pset) == 8
        assert pset.count() == 1
        assert list(pset) == [0, 1, 2, 3, 4, 5, 6, 7]

    def test_superset_left_touch(self):
        """
        init:  -∞....[_]..[_]....+∞
        add:   -∞....[_____].....+∞
        final: -∞....[______]....+∞
        """
        pset = ProcSet(ProcInt(0, 2), ProcInt(5, 7))
        pset.add(ProcInt(0, 6))
        assert len(pset) == 8
        assert pset.count() == 1
        assert list(pset) == [0, 1, 2, 3, 4, 5, 6, 7]

    def test_superset_right_notouch(self):
        """
        init:  -∞....[_]..[].....+∞
        add:   -∞.....[_____]....+∞
        final: -∞....[______]....+∞
        """
        pset = ProcSet(ProcInt(0, 2), ProcInt(5, 6))
        pset.add(ProcInt(1, 7))
        assert len(pset) == 8
        assert pset.count() == 1
        assert list(pset) == [0, 1, 2, 3, 4, 5, 6, 7]

    def test_superset_right_touch(self):
        """
        init:  -∞....[_]..[_]....+∞
        add:   -∞.....[_____]....+∞
        final: -∞....[______]....+∞
        """
        pset = ProcSet(ProcInt(0, 2), ProcInt(5, 7))
        pset.add(ProcInt(1, 7))
        assert len(pset) == 8
        assert pset.count() == 1
        assert list(pset) == [0, 1, 2, 3, 4, 5, 6, 7]

    def test_englobing_superset(self):
        """
        init:  -∞.....[].[]......+∞
        add:   -∞....[_____].....+∞
        final: -∞....[_____].....+∞
        """
        pset = ProcSet(ProcInt(1, 2), ProcInt(4, 5))
        pset.add(ProcInt(0, 6))
        assert len(pset) == 7
        assert pset.count() == 1
        assert list(pset) == [0, 1, 2, 3, 4, 5, 6]

    def test_left_disjoint_point_notouch(self):
        """
        init:  -∞........[__]....+∞
        add:   -∞....X...........+∞
        final: -∞....X...[__]....+∞
        """
        pset = ProcSet(ProcInt(4, 7))
        pset.add(ProcInt(0, 0))
        assert len(pset) == 5
        assert pset.count() == 2
        assert list(pset) == [0, 4, 5, 6, 7]

    def test_right_disjoint_point_notouch(self):
        """
        init:  -∞....[__]........+∞
        add:   -∞...........X....+∞
        final: -∞....[__]...X....+∞
        """
        pset = ProcSet(ProcInt(0, 3))
        pset.add(ProcInt(7, 7))
        assert len(pset) == 5
        assert pset.count() == 2
        assert list(pset) == [0, 1, 2, 3, 7]

    def test_left_disjoint_point_touch(self):
        """
        init:  -∞........[__]....+∞
        add:   -∞.......X........+∞
        final: -∞.......[___]....+∞
        """
        pset = ProcSet(ProcInt(4, 7))
        pset.add(ProcInt(3, 3))
        assert len(pset) == 5
        assert pset.count() == 1
        assert list(pset) == [3, 4, 5, 6, 7]

    def test_right_disjoint_point_touch(self):
        """
        init:  -∞....[__]........+∞
        add:   -∞........X.......+∞
        final: -∞....[___].......+∞
        """
        pset = ProcSet(ProcInt(0, 3))
        pset.add(ProcInt(4, 4))
        assert len(pset) == 5
        assert pset.count() == 1
        assert list(pset) == [0, 1, 2, 3, 4]

    def test_single_point(self):
        pset = ProcSet()
        pset.add(0)
        assert len(pset) == 1
        assert pset.count() == 1
        assert list(pset) == [0]

    def test_incompatible_iter(self):
        with pytest.raises(ValueError):
            pset = ProcSet()
            pset.add((0, 1, 2))  # too many
        with pytest.raises(ValueError):
            pset = ProcSet()
            pset.add((0, ))  # too few
