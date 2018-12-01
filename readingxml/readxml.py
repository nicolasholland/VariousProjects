import xml.etree.ElementTree as ET
import xml
import time
import pickle
import numpy as np
import h5py

from distributed.protocol import dask_serialize, dask_deserialize

start = time.time()
tree = ET.parse('example.xml')
end = time.time()
print("Parsing runtime (sec) ", end-start)

root = tree.getroot()

def load(fn):
    with open(fn, 'rb') as inputfile:
        binarystring = inputfile.read()
    return pickle.loads(binarystring)



def xmltree_from_childlist(cl):
    xml = ET.fromstring("<data></data>")
    for c in cl:
        xml.append(x)
    return xml

def tree2hdf(tree):
    root = tree.getroot()
    arr = np.array([pickle.dumps(c) for c  in root])

    hh = h5py.File('xml.hdf', 'w') 
    hh.create_dataset('data', data=arr)
    hh.close()


def hdf2tree(filename):
    hdf = h5py.File(filename, 'r')
    arr = hdf['data'][:]
    return arr

@dask_serialize.register(xml.etree.ElementTree.Element)
def serialize(tree):
    header = {}
    frames = [pickle.dumps(tree)]
    return header, frames


@dask_deserialize.register(xml.etree.ElementTree.Element)
def deserialize(Dict, frames):
    return pickle.loads(frames[0])





#ET.dump(xml) 
