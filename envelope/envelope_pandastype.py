#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  2 21:42:15 2018

@author: dutchman

Doesnt work yet...
Im missing something.
"""
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

    def __init__(self, array, dtype=None, copy=None):
        #assert array.shape[1] == 2
        #assert (array[:, 0] <= array[:, 1]).all()
        self.data = array
        self.lower = array[:, 0]
        self.upper = array[:, 1]

    @classmethod
    def _from_factorized(cls, values, original):
        return cls(values)

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, item):
        retval = type(self)(self.data[item])
        if self.data.shape == (2,):
            retval = type(self)(self.data)
        #print("I AM CALLED getitem ", "item: ", item, "retval: ", retval, "shape ", self.data.shape)
        return retval

    def __len__(self):
        """
        Length of this array
        Returns
        -------
        length : int
        """
        retval = self.data.shape[0]
        if len(self.data.shape) == 1:
            retval = 1
        #print("Are you looking at me? ", "shape: ", self.data.shape, "retval ", retval)
        return retval

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
        return cls(np.concatenate(ea.data for ea in to_concat))

    def isna(self):
        """
        Boolean NumPy array indicating if each value is missing.
        """
        print("Is this happening?")
        return (self.data[:, 0] == np.nan) & (self.data[:, 1] == np.nan)

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
            return type(self)(self.data.copy(deep=True))
        return type(self)(self.data)

    def __array2__(self):
        return self.upper

    @property
    def nbytes(self):
        """
        The number of bytes needed to store this object in memory.
        """
        return self.data.nbytes


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
        Raises
        ------
        IndexError
            When the indices are out of bounds for the array.
        ValueError
            When `indices` contains negative values other than ``-1``
            and `allow_fill` is True.
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
        return type(self)(self.data[indices])


@pd.api.extensions.register_series_accessor("envelope")
class EnvelopeAccessor:
    def __init__(self, obj):
        self._data = obj.values
        self._index = obj.index
        self._name = obj.name


bound_array = np.array([[2,3], [3,4], [4,5]])
#bound_array = np.array([1,2])

c = EnvelopeArray(bound_array)
print("Im an array ", c)

#c = EnvelopeArray((2,3))


print("make a dataframe")
#df = pd.DataFrame({'aha': c})
df = pd.Series(c)

#print(df)

