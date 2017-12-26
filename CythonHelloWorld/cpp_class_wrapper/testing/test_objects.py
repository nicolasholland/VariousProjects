import objects
import unittest

class objects_test(unittest.TestCase):

    def test_PyVector3d_init(self):
        v3d = objects.PyVector3d(3, 5, 6)

    def test_PyVector3d_sum(self):
        v3d = objects.PyVector3d(3, 5, 6)
        self.assertEqual(v3d.sum(), 14)

    def test_PyVector3d_get(self):
        v3d = objects.PyVector3d(3, 5, 6)
        self.assertEqual(v3d.x, 3)

    def test_PyVector3d_set(self):
        v3d = objects.PyVector3d(3, 5, 6)
        v3d.x = 8
        self.assertEqual(v3d.x, 8)

if __name__ == '__main__':
    unittest.main() 
