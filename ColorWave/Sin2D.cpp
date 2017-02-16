#include <iostream>
#include <stdlib.h>
#include <math.h>

double* Sin2D( double* mat, int W, int H, double t){
  for (int x=0; x < W; x++)
   for (int y=0; y < H; y++) {
     mat[y*H+x] = sin( (x*x + y*y)/1000. + t );
  }
  return mat;	
}

