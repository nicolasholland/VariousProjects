#include <vector.h>

namespace vector {
    Vector3d::Vector3d() { };

    Vector3d::Vector3d(double x, double y, double z) {
        this->x = x;
        this->y = y;
        this->z = z;
    };

    double Vector3d::sum() {
        return (this->y + this->x + this->z);
    };
}
