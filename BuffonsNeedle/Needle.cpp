#include <iostream>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#include "Needle.h"

Needle Create(int g){
  Needle needle;
  needle.x = (double (rand() % (100*g)))/100;
  needle.y = (double (rand() % (100*g)))/100;
  needle.phi = (rand() % 180 - 90);
	
  return needle;
}

int Intersect2(Needle needle) {
  double v_x = cos(needle.phi * 3.14159 / 180 );

  // compute endpoints of needle
  double x1 = needle.x + .5 * v_x;
  double x2 = needle.x - .5 * v_x;

  // sort
  double max = (x1 < x2) ? x2 : x1;
  double min = (x1 > x2) ? x2 : x1;

  if (min < 0)
    min = -1;  

  // intersect
  if ((int)min + 1 == (int)max)
    return 1;

  return 0;
}

int Intersect(Needle needle){
	double a;
	if ( needle.phi != 0 && fabs(needle.phi) != 90 ) {
		int x1 = needle.x;
		double x = needle.x -x1;
		if (x <= 0.5){
			a = x/cos(needle.phi * 3.14159 /180 );	
		}
		if (x > 0.5){
			a = (1-x)/cos(-1 * needle.phi * 3.14159 /180 );
		}
	}
	if ( a >= 0.5){
		return 0;
	}
	return 1;
}

// create Needle and determine the quotient
double Simulate(int o, int g, Needle* needles){
  // initialize Random- Number
  srand (time(NULL));

  int z = 0;
  for (int j = 0; j < o; j++){
    Needle needle = Create(g);
    needles[j] = needle;
    z = z + Intersect(needle);
  }
  return 2*(double) o/z;
}
