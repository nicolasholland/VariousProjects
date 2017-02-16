#include "SDL2/SDL.h"

#ifndef VISUALIZE
#define VISUALIZE

typedef struct RGB {
 int R;
 int G;
 int B;
} RGB;

const int WIDTH = 400;
const int HEIGHT = 400;

int VisualizeWave (SDL_Window* window, SDL_Renderer* renderer, SDL_Surface* surface, double* wave);

RGB D2RGB (double c);
#endif
