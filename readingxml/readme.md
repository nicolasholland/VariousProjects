Binary XML
==========

The goal of this project is to store xml data in such a way, that it can be
read faster than regular xml but still have its structure so that other
applications that may need an actual xml file can still be used.


We are using pythons [xml package](https://docs.python.org/3.7/library/xml.etree.elementtree.html)
Here is an example document from their tutorial:

```
<?xml version="1.0"?>
<data>
    <country name="Liechtenstein">
        <rank>1</rank>
        <year>2008</year>
        <gdppc>141100</gdppc>
        <neighbor name="Austria" direction="E"/>
        <neighbor name="Switzerland" direction="W"/>
    </country>
    <country name="Singapore">
        <rank>4</rank>
        <year>2011</year>
        <gdppc>59900</gdppc>
        <neighbor name="Malaysia" direction="N"/>
    </country>
    <country name="Panama">
        <rank>68</rank>
        <year>2011</year>
        <gdppc>13600</gdppc>
        <neighbor name="Costa Rica" direction="W"/>
        <neighbor name="Colombia" direction="E"/>
    </country>
</data>
```

We created an xml file of almost 40mb by repeating this example data over an over.
This 40mb example file was used to compare parse runtimes.

```
>>> import xml.etree.ElementTree as ET
>>> %timeit tree = ET.parse('example2.xml')
867 ms ± 12.1 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```


1st Approach: Serializing Tree Object
-------------------------------------

Parsing the textfile is one way to get a tree object.
Another would be to serialize the tree object and than deserialize that bytestring.


```
>>> import pickle
>>> serialized_tree = pickle.dumps(tree)
>>> with open('binarytree.dat', 'wb') as output:
... 	output.write(serialized_tree)
```

Now we have stored the tree object as binary string.
Instead of parsing the xml tree we can load that string and deserialize it.


```
def load(fn):
    """ read and deserialize binary xml tree object """
    with open(fn, 'rb') as inputfile:
        binarystring = inputfile.read()
    return pickle.loads(binarystring)
```

However this method turns out to be slower than parsing the text file.

```
%timeit tree = load('binaryxml.dat')
2.15 s ± 13.6 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
```

Simply reading the binary string is not the problem:

```
>>> %timeit bs = open('binarytree.dat', 'rb').read()
65.4 ms ± 154 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
```

It is the deserialization that takes a long time.
Maybe we can parallize it on the xml tree nodes?


2nd Approach: Serializing Tree Nodes
------------------------------------

Idea: serialize tree nodes separately and store in an hdf5 file.
This is how we get the nodes / write the hdf file:

```
import numpy as np
import h5py
def tree2hdf(tree):
    """ store tree nodes in an hdf5 file """
    root = tree.getroot()
    arr = np.array([pickle.dumps(c) for c  in root])

    hh = h5py.File('xml.hdf', 'w')
    hh.create_dataset('data', data=arr)
    hh.close()
```

Reading hdf file rather fast:

```
>>> def hdf2tree(filename):
...    hdf = h5py.File(filename, 'r')
...    arr = hdf['data'][:]
...    return arr
>>> %timeit arr = hdf2tree('xml.hdf')
62.3 ms ± 950 µs per loop (mean ± std. dev. of 7 runs, 10 loops each)
```

Now we need fast deserialization!

```
>>> from multiprocessing import Pool
>>> p = Pool(4)
>>> %time tree = p.map(pickle.loads, arr)
CPU times: user 11.3 s, sys: 547 ms, total: 11.8 s
Wall time: 12.7 s
```

Even slower than before!
Maybe if we have more CPU cores?

Site Note
---------

Of course we can store the actual data in a different format e.g.
in a [dataframe](http://www.austintaylor.io/lxml/python/pandas/xml/dataframe/2016/07/08/convert-xml-to-pandas-dataframe/), however if we have other applications that need an xml file as input we must be able to create an equivalent xml file back from the dataframe.
Not that simple...



