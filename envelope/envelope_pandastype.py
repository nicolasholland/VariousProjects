#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 21:42:15 2018

@author: dutchman

My envelope pandas extension.
"""
import unittest
import numpy as np
import pandas as pd
from pandas.api.extensions import ExtensionDtype
from pandas.core.arrays import ExtensionArray
import abc

class BaseType(abc.ABCMeta):
    """ Type metaclass """
    pass

class EnvelopeType(ExtensionDtype):
    name = 'envelope'
    type = BaseType
    kind = 'O'

    @classmethod
    def construct_from_string(cls, string):
        if string == cls.name:
            return cls()
        else:
            raise TypeError("Cannot construct a '{}' from "
                            "'{}'".format(cls, string))


class EnvelopeArray(ExtensionArray):
    """
    Envelope Extension Array
    """
    _can_hold_na = True

    def __init__(self, array, upper=None, dtype=None, copy=None):
        self.lower = array

        if upper is None:
            upper = array * np.nan
        else:
            if not (array < upper).all():
                raise ValueError("Upper array must be greater than lower.")

        self.upper = upper


    @classmethod
    def _from_factorized(cls, values, original):
        return cls(values)

    def __str__(self):
        return  ''.join(['l', str(self.lower), ' u', str(self.upper)])

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, item):
        retval = type(self)(self.lower[item], upper=self.upper[item])
        return retval

    def __len__(self):
        """
        Length of this array
        Returns
        -------
        length : int
        """
        return len(self.lower)

    @property
    def dtype(self):
        return EnvelopeType()

    @classmethod
    def _concat_same_type(cls, to_concat):
        """
        Concatenate multiple array
        Parameters
        ----------
        to_concat : sequence of this type
        Returns
        -------
        ExtensionArray
        """
        data = np.concatenate(ea.data for ea in to_concat)
        upper = np.concatenate(ea.upper for ea in to_concat)
        return cls(data, upper=upper)

    def isna(self):
        """
        Boolean NumPy array indicating if each value is missing.
        """
        return np.isnan(self.lower) & np.isnan(self.upper)

    def copy(self, deep=False):
        """
        Return a copy of the array.
        Parameters
        ----------
        deep : bool, default False
            Also copy the underlying data backing this array.
        Returns
        -------
        ExtensionArray
        """
        if deep:
            return type(self)(self.lower.copy(deep=True))
        return type(self)(self.lower)

    @property
    def T(self):
        return self


    @property
    def nbytes(self):
        """
        The number of bytes needed to store this object in memory.
        """
        return self.lower.nbytes + self.upper.nbytes


    @classmethod
    def _from_sequence(cls, scalars, dtype=None):
        """
        Construct a new ExtensionArray from a sequence of scalars.
        Parameters
        ----------
        scalars : Sequence
            Each element will be an instance of the scalar type for this
            array, ``cls.dtype.type``.
        Returns
        -------
        ExtensionArray
        """
        return cls(np.array(scalars))

    def take(self, indices, allow_fill=False, fill_value=None):
        """
        Take elements from an array.

        Parameters
        ----------
        indices : sequence of integers
            Indices to be taken.
        allow_fill : bool, default False
            How to handle negative values in `indices`.
            * False: negative values in `indices` indicate positional indices
              from the right (the default). This is similar to
              :func:`numpy.take`.
            * True: negative values in `indices` indicate
              missing values. These values are set to `fill_value`. Any other
              other negative values raise a ``ValueError``.
        fill_value : any, optional
            Fill value to use for NA-indices when `allow_fill` is True.
            This may be ``None``, in which case the default NA value for
            the type, ``self.dtype.na_value``, is used.
            For many ExtensionArrays, there will be two representations of
            `fill_value`: a user-facing "boxed" scalar, and a low-level
            physical NA value. `fill_value` should be the user-facing version,
            and the implementation should handle translating that to the
            physical version for processing the take if nescessary.

        Returns
        -------
        ExtensionArray

        Notes
        -----
        ExtensionArray.take is called by ``Series.__getitem__``, ``.loc``,
        ``iloc``, when `indices` is a sequence of values. Additionally,
        it's called by :meth:`Series.reindex`, or any other method
        that causes realignemnt, with a `fill_value`.

        See Also
        --------
        numpy.take
        pandas.api.extensions.take
        """
        return type(self)(self.lower[indices], upper=self.upper[indices])


@pd.api.extensions.register_series_accessor("envelope")
class EnvelopeAccessor:
    def __init__(self, obj):
        self._data = obj.values
        self._index = obj.index
        self._name = obj.name

    def __call__(self):
        if type(self._data) == EnvelopeArray:
            return self._data.lower, self._data.upper
        else:
            raise ValueError("Only works for EnvelopeArrays")


class EnvelopeArrayTest(unittest.TestCase):
    def test_init(self):
        lower = np.array([1, 2, 3])
        upper = np.array([2, 3, 4])

        ea = EnvelopeArray(lower, upper=upper)
        self.assertTrue(isinstance(ea, EnvelopeArray))
    def test_series(self):
        lower = np.array([1, 2, 3])
        upper = np.array([2, 3, 4])

        ts = pd.Series(EnvelopeArray(lower, upper=upper))
        self.assertTrue(isinstance(ts, pd.Series))

    def test_dataframe(self):
        lower = np.array([1, 2, 3])
        upper = np.array([2, 3, 4])

        df = pd.DataFrame({'an_envelope': EnvelopeArray(lower, upper=upper)})
        self.assertTrue(isinstance(df, pd.DataFrame))

    def test_accessor(self):
        lower = np.array([1, 2, 3])
        upper = np.array([2, 3, 4])

        ts = pd.Series(EnvelopeArray(lower, upper=upper))
        minarr, maxarr = ts.envelope()
        self.assertTrue(np.equal(minarr, lower).all())
        self.assertTrue(np.equal(maxarr, upper).all())

if __name__ == '__main__':
    unittest.main()


