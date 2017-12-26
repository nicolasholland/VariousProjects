#ifndef VECTOR
#define VECTOR

namespace vector {
    class Vector3d{
    public:
        double x, y, z;
        Vector3d();
        Vector3d(double x, double y, double z);
        double sum();
    };
}

#endif
