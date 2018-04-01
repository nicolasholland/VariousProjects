from poly_pb2 import Polynom
import numpy as np


class Poly(object):
    polynom = Polynom()

    def __init__(self, bytestring):
        self.polynom.ParseFromString(bytestring)

    @property
    def coefficient(self):
        return self.polynom.coefficient

    def __call__(self, x):
        arr = np.array([np.power(x, i) for i in range(len(self.coefficient))])
        return (arr * np.array(self.coefficient)).sum()

if __name__ == '__main__':
    with open('poly.dat', 'wb') as fo:
        p = Polynom()
        p.coefficient.append(1)
        p.coefficient.append(2)
        p.coefficient.append(4.5)
        fo.write(p.SerializeToString())
