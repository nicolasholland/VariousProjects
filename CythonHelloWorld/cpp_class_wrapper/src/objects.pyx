cdef extern from "vector.h" namespace "vector":
    cdef cppclass Vector3d:
        Vector3d() except +
        Vector3d(double x, double y, double z) except +
        double x, y, z
        double sum()

cdef class PyVector3d:
    cdef Vector3d ref

    def __cinit__(self, double x, double y, double z):
        self.ref = Vector3d(x, y, z)

    def sum(self):
        return self.ref.sum()

    @property
    def x(self):
        return self.ref.x

    @x.setter
    def x(self, val):
        self.ref.x = val
