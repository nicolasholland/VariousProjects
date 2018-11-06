import os
import pandas as pd
import inspect
import yaml

class FC(object):
    """ FC Base class """

    def __init__(self, function):
        self.filterfunc = function
        self.signature = inspect.signature(function)


    def __call__(self, *args, **kwargs):
        if len(args) == 1 and os.path.exists(args[0]):
            self.args, self.kwargs = self._readfromyml(args[0])
        else:
            self.args, self.kwargs = args, kwargs
        return self

    def __str__(self):
        return " : ".join(['original header', str(self.signature)])

    def __repr__(self):
        return "\n".join([self.__doc__, self.__str__()])

    def _readfromyml(self, ymlfile):
        with open(ymlfile, 'r') as stream:
            try:
                retval = yaml.load(stream)[self.__name__]['filter_kwargs']
            except yaml.YAMLError as exc:
                print(exc)
        return [], retval


class SingleFC(FC):
    """ FC Class for single time series input """
    def run(self, ts):
        return self.filterfunc(ts, *self.args, **self.kwargs)

class DoubleFC(FC):
    """ FC Class for two time series input """
    def run(self, ts1, ts2):
        return self.filterfunc(ts1, ts2, *self.args, **self.kwargs)

def makefc(argument):
    def _decorator(function):
        if argument == 'single':
            retval = SingleFC(function)
        if argument == 'double':
            retval = DoubleFC(function)

        retval.__doc__ = function.__doc__
        retval.__name__ = function.__name__
        return retval
    return _decorator


@makefc('single')
def lowerthan(ts, bound, lowerflag, aboveflag):
    """
    Parameters
    ----------
    pd.Series
    bound : numeric, upper boundary
    lowerflag : numeric or string, values lower than bound get this flag
    aboveflag : numeric or string, values above bound get this flag
    """
    crit = ts < bound
    retval = ts.copy()
    retval[crit] = lowerflag
    retval[~crit] = aboveflag
    return retval

@makefc('double')
def lowerthants(ts, bound, lowerflag, aboveflag):
    """
    Parameters
    ----------
    ts : pd.Series
    bound : pd.Series, upper boundary
    lowerflag : numeric or string, values lower than bound get this flag
    aboveflag : numeric or string, values above bound get this flag
    """
    crit = ts < bound
    retval = ts.copy()
    retval[crit] = lowerflag
    retval[~crit] = aboveflag
    return retval



f = lowerthan(4, 'good', 'bad')
f = lowerthan('fc.yml')
ff = lowerthants('good', 'bad')

ats = pd.Series([2,3,4,2], pd.date_range('2018-10-06', periods=4))
fours = pd.Series([4,4,4,4], pd.date_range('2018-10-06', periods=4))

res = f.run(ats)
res = ff.run(ats, fours)
print(res)

