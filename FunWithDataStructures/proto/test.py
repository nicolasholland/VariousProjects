import unittest
from poly import Poly
import numpy as np


class TestPolynom(unittest.TestCase):

    def test_init(self):
        with open('poly.dat', 'rb') as fi:
            p = Poly(fi.read())

        self.assertTrue(np.array_equal(np.array(p.coefficient),
                                       np.array([1., 2., 4.5])))

    def test_call(self):
        with open('poly.dat', 'rb') as fi:
            p = Poly(fi.read())

        self.assertEqual(p(2), 23.0)


if __name__ == '__main__':
    unittest.main()
