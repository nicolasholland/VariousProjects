#include <iostream>
#include "adept.h"

using adept::adouble;

adouble simulate_throw (adouble* un, adouble* v_y, adouble v_x, int T, double h, double g) {
  // simulate using euler method
  for (int t=0; t < T; t++) {
    un[t+1] = un[t] + h*v_y[t];
    v_y[t+1] = v_y[t] + h*g;
  }

  return un[T];
}

adouble print_simulate (adouble* un, adouble* v_y, adouble v_x, int T, double h, double g) {
  // simulate using euler method
  for (int t=0; t < T; t++) {
    un[t+1] = un[t] + h*v_y[t];
    v_y[t+1] = v_y[t] + h*g;
    std::cout << t*h*v_x << " " << un[t+1] << std::endl;
  }

  return un[T];
}
