#include <iostream>

#include "SDL2/SDL.h"
#include "Sin2Col.h"


int main(int argc, char** argv) {

  // Visualization
  SDL_Window* window =  NULL;
  SDL_Renderer* renderer = NULL;
  SDL_Surface* surface = NULL;

  double* wave = (double *) malloc(HEIGHT*WIDTH*sizeof(double));

  VisualizeWave (window, renderer, surface, wave);

  std::cout<< "works fine" << std::endl;

  return 0;
}
