#include <iostream>
#include <stdlib.h>

#include "SDL2/SDL.h"

#include "Visualize.h"
#include "Needle.h"

int main (int argc, char** argv) {
  // Simulation
  int nofNeedles = 100000;
  Needle* needles = (Needle*) malloc(nofNeedles * sizeof(Needle));

  double pi = Simulate(nofNeedles, 10, needles);
  std::cout << "PI: " << pi << std::endl;


  // Visualization
  SDL_Window* window =  NULL;
  SDL_Renderer* renderer = NULL;
  SDL_Surface* surface = NULL;

  //visualize::DrawAll(window, renderer, surface, needles, nofNeedles, 0, 10);

  SDL_Quit();

  return 0;
}
