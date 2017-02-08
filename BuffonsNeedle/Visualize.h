#include "SDL2/SDL.h"

#include "Needle.h"

#ifndef VISUALIZE
#define VISUALIZE
namespace visualize {

// Draw a single needle
// a and b are the boundarys within the needles were dropped
void DrawNeedle (SDL_Renderer* renderer, Needle needle, int a, int b);

// Draw the Board
void DrawBoard (SDL_Renderer* renderer, int a, int b);

// Draw the board and a stack of needles
int DrawAll (SDL_Window* window,  SDL_Renderer* renderer, SDL_Surface* surface,  Needle* needles, int nofneedle, int a, int b);
}
#endif
