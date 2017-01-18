#include <iostream>
#include <cmath>
#include "adept.h"
#include "simulate.h"

using adept::adouble;

int main(int argc, char** argv) {
  // init stack
  adept::Stack stack;

  // Gravity
  double g = -9.81;

  // Timesteps and stepwidth
  int T = 100;
  double h = 20./T;


  // Position of the ball
  adouble un[T+1];
  un[0] = 0.;

  // speed of the ball
  adouble v_y[T+1];
  v_y[0] = 97.119;
  adouble v_x = 1.; // without air resistance this is constant

  adouble result;

  double dResult_dInitial; 
  double gdstepwidth = .001;
  double eps = .1;
  int maxiter = 10;
  do {
    stack.new_recording();

    // Simulate throw
    simulate_throw(un, v_y, v_x, T, h, g);
    //print_simulate(un, v_y, v_x, T, h, g); // Use to print trajectory

    result = un[T] * un[T];

    result.set_gradient(1.0);
    stack.compute_adjoint();

    dResult_dInitial = v_y[0].get_gradient();

    std::cout << "Initial: " << v_y[0].value() << std::endl;
    std::cout << "Result: " << un[T].value() << std::endl;
    std::cout << "dResult_dInitial: " << dResult_dInitial << std::endl;
    
    // gradient descent step
    v_y[0] -= gdstepwidth * dResult_dInitial;
    maxiter -= 1;
  }while(fabs(dResult_dInitial) > eps && maxiter);

  return 0;
}
