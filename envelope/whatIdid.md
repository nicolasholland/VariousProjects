Forecast Envelope
=================

A while ago we saw a talk about adding a fast string type into pandas using arrow and numba.
Besides the fact how awesome that is, we were fascinated by the idea of adding custom data types into pandas.
So we decided to try and implement our own custom data type.

In order to learn how to do that we looked at the package from the talk [fletcher](https://github.com/xhochy/fletcher), as well as some other examples
like [cyberpandas](), which implements a custom data type for ip addresses.
And of course there is a documentation page by [pandas](https://pandas.pydata.org/pandas-docs/stable/extending.html) that also explains how to do that.


But before we could implement a data type we had to come up with one.
So we thought of a problem that a new data type could help in solving.
Let's assume it is our business to forecast stock values.

We can download stock values using the [pandas-datareader](https://pandas-datareader.readthedocs.io/en/latest/remote_data.html#iex).
As an example we use the google stock GOOG.

```
>>> from pandas_datareader import data
>>> df = data.DataReader('GOOG', start='2017-11-01', end='2018-11-01', data_source='iex')
```

We want to forecast the 'closed' stock value for the day ahead.
In order to create the forecasts we take a time series of the last 30 days before the day we want to forecast.
Then we create a bunch of sklearn regressors and fit them to the timeseries e.g. [support vector regression](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVR.html)
Once we have the fitted curves we extrapolate them by one step and now we have an assemble of forecasts.

Here is how our fits and forecasts may look like:

PICTURE


We know that our forecasts themselfs are not reliable, so instead of using them directly we look at their minmax range.
This minmax range is the subject of our imaginary business.
We create those range forecasts for stocks and therefore predict how the stocks may develop.
And since ideally the stock curves should be within those ranges we call them envelopes.
Here is an example of the envelope created by our sklearn regressor forecasts:

PICTURE


Even though we use an ansemble of forecasts to create the envelopes, an envelope itself can be stored with just two arrays.
Since these envelopes are our business, it is important to us that they are reasonable,
e.g. there must be no envelope where the max curve is lower than the min curve.
There are many ways to ensure this property e.g. we could add constraints to our database, or add assertions to the forecasting process.
But to be really sure that the envelopes are ok, we create a custom envelope data type, which we use to extend pandas!

There are two pandas classes that we need to subclass for that, ExtensionDtype and ExtensionArray

```
>>> from pandas.api.extensions import ExtensionDtype
>>> from pandas.core.arrays import ExtensionArray
```

The pandas documentation tells us what methods and attributes we have to overwrite.
Note that the classes are not abc, so there is no imideat??? way to see if you've implemented everything you need.
Since our data type is basically just two numpy arrays, we learned a lot from pandas' categorical array [pandas.categorical](https://github.com/pandas-dev/pandas/blob/v0.23.4/pandas/core/arrays/categorical.py#L170-L2343).
We put our minmax constraint right in the constructor:

```
def __init__(self, array, upper=None, dtype=None, copy=None):
    ...
    if not (self.lower < upper).all():
        raise ValueError("Upper array must be greater than lower.")
    ...
```

Here is how our Extension Array looks in action:

```
>>> minarray, maxarray = np.array([14, 9, 12]), np.array([15, 13, 17])
>>> df = pd.DataFrame({'an_envelope': EnvelopeArray(minarray, upper=maxarray)})
>>> df
  an_envelope
0     l14 u15
1      l9 u13
2     l12 u17
```

Now we can create dataframes with forecast envelopes!
Different stocks can have different columns and we can use many of pandas great features. =D
We also learned how to register cusom accessors for both Series and DataFrame objects.
Basically you create an accessor class, that does what ever you want and you decorate it with pandas' accessor decorators:

```
@pd.api.extensions.register_series_accessor("envelope")
class EnvelopeAcessor:
    ...
```

We Added an envelope accessor that makes it easy to retrieve the underlying lower and upper numpy arrays from our envelope arrays.
You can find the code on our [github](https://github.com/nicolasholland/VariousProjects/tree/master/envelope).

