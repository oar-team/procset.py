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
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Wrapper functions around procset to provide the API of interval_set.

This module aims at easing the transition from interval_set to procset, and
should not be used in any new project. The code is not optimized at all, as it
converts the structures to ProcSet back and forth.

The module is planned for removal in the next major release.
"""

import functools
import warnings

from procset import ProcSet


# helper decorator factory

def _deprecated(message=""):
    def _decorated(func):
        @functools.wraps(func)
        def _wrapper(*args, **kwargs):
            warnings.warn(
                message,
                DeprecationWarning,
                stacklevel=2
            )
            return func(*args, **kwargs)
        return _wrapper
    return _decorated


# old API implementation: string conversions

@_deprecated("Deprecated function: use str(intervals) or format(intervals) instead.")
def interval_set_to_string(itvs, separator=" "):
    """[deprecated] Convert an intervals' set into a string."""
    format_spec = '-' + separator[0]
    return format(ProcSet(*itvs), format_spec)


@_deprecated("Deprecated function: use ProcSet.from_str(s) instead.")
def string_to_interval_set(string, separator=" "):
    """[deprecated] Transform a string to an intervals' set."""
    # pylint: disable=protected-access
    return ProcSet.from_str(string, outsep=separator)._itvs


# old API implementation: ID list conversions

@_deprecated("Deprecated function: use ProcSet(*ids) instead.")
def id_list_to_iterval_set(idlist):
    """[deprecated] Convert a list of ID (int) into an intervals' set."""
    # pylint: disable=protected-access
    return ProcSet(*idlist)._itvs


@_deprecated("Deprecated function: use list(itvs) instead.")
def interval_set_to_id_list(itvs):
    """[deprecated] Convert an intervals' set into a list of ID (int)."""
    return list(ProcSet(*itvs))


# old API implementation: ID set conversions

@_deprecated("Deprecated function: use set(itvs) instead.")
def interval_set_to_set(itvs):
    """[deprecated] Convert an intervals' set into a set of ID (int)."""
    return set(ProcSet(*itvs))


@_deprecated("Deprecated function: use ProcSet(*s) instead.")
def set_to_interval_set(idset):
    """[deprecated] Convert a set of ID (int) into an intervals' set."""
    # pylint: disable=protected-access
    return ProcSet(*idset)._itvs


# old API implementation: statistics

@_deprecated("Deprecated function: use len(itvs) instead.")
def total(itvs):
    """[deprecated] Compute the number of elements in the whole set."""
    return len(ProcSet(*itvs))


# old API implementation: set theory operations

@_deprecated("Deprecated function: use == instead.")
def equals(itvs1, itvs2):
    """[deprecated] Check for equality between two intervals' sets."""
    return ProcSet(*itvs1) == ProcSet(*itvs2)


@_deprecated("Deprecated function: itvs_base - itvs2 instead.")
def difference(itvs1, itvs2):
    """
    [deprecated] Return the intervals' set containing elements in the first set
    but not in the second.
    """
    # pylint: disable=protected-access
    return (ProcSet(*itvs1) - ProcSet(*itvs2))._itvs


@_deprecated("Deprecated function: use itvs1 & itvs2 instead.")
def intersection(itvs1, itvs2):
    """
    [deprecated] Return the intervals' set containing elements common to the
    first and second sets.
    """
    # pylint: disable=protected-access
    return (ProcSet(*itvs1) & ProcSet(*itvs2))._itvs


@_deprecated("Deprecated function: use itvs1 | itvs2 instead.")
def union(itvs1, itvs2):
    """
    [deprecated] Return the intervals' set with the elements from the first set
    and the second set.
    """
    # pylint: disable=protected-access
    return (ProcSet(*itvs1) | ProcSet(*itvs2))._itvs


@_deprecated("Deprecated function: use aggregate method instead.")
def aggregate(itvs):
    """
    [deprecated] Return the smallest interval containing all intervals from the
    given intervals' set.
    """
    # pylint: disable=protected-access
    return ProcSet(*itvs).aggregate()._itvs
