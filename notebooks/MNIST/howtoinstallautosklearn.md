How to install auto sklearn
===========================

While scikit-learn and tensorflow can be simply installed through either pip or conda,
we found autosklearn to be a bit more complicated. (Mainly because of compiler trouble.)
So here's in short what we did.

Start by creating new conda environment

```
$ conda create -n autosk python=3
```

We found some info from [here](https://stackoverflow.com/questions/54817301/installing-autosklearn-in-anaconda-environment) on fixing the compiler trouble.
Comes down to this:

```
$ conda install gxx_linux-64 gcc_linux-64 swig
```

After that we simply followed the instructions from [auto-sklearn](https://automl.github.io/auto-sklearn/master/installation.html).

```
$ pip install auto-sklearn
```

While we still got some warnings etc.,
which are probably because we did not install the dependencies manually
as was adviced on the original installation page,
the installation went through an sklearn is ready to use.

```
>>> import autosklearn
```

This was done on Fedora release 28.

