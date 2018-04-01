#include <fstream>
#include <string>
#include <cmath>
#include "gtest/gtest.h"
#include "poly.pb.h"

class Poly {
    private:
        polynom::Polynom p;

    public:
        Poly(std::string line) {
            p.ParseFromString(line);
        }

        float operator()(float x) {
            float retval = 0;
            for (int i=0; i < p.coefficient_size(); i++) {
                retval += std::pow(x, i) * p.coefficient(i);
            }

            return retval;
        }
};


TEST(PolynomTest, call) {
    std::ifstream myfile;
    std::string line;

    myfile.open("poly.dat");
    std::getline(myfile,line);
    myfile.close();

    Poly p = Poly(line);
    EXPECT_EQ(23., p(2.));
}


int main(int argc, char **argv) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}

