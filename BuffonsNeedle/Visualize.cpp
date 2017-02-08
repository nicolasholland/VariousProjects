#include "SDL2/SDL.h"

#include <iostream>
#include <math.h>

#include "Needle.h"
#include "Visualize.h"

namespace visualize {

void DrawNeedle (SDL_Renderer* renderer, Needle needle, int a, int b) {
  // turn angle into vector
  double v_y = sin(needle.phi * 3.1415 / 180 );
  double v_x = cos(needle.phi * 3.1415 / 180 );

  // compute endpoints of needle
  double x1 = needle.x + .5 * v_x;
  double y1 = needle.y + .5 * v_y;
  double x2 = needle.x - .5 * v_x;
  double y2 = needle.y - .5 * v_y;

  // translate points to frame
  x1 = x1/b * 400 + 50;
  y1 = y1/b * 400 + 50;
  x2 = x2/b * 400 + 50;
  y2 = y2/b * 400 + 50;

  // draw needle
  if (Intersect(needle))
	SDL_SetRenderDrawColor(renderer, 255, 0, 0, SDL_ALPHA_OPAQUE);
  else
	SDL_SetRenderDrawColor(renderer, 0, 0, 0, SDL_ALPHA_OPAQUE);

  SDL_RenderDrawLine(renderer, x1, y1, x2, y2);
}

void DrawBoard (SDL_Renderer* renderer, int a, int b) {
     // line color black
    SDL_SetRenderDrawColor(renderer, 0, 0, 0, SDL_ALPHA_OPAQUE);

    double x;

    for (int line = a; line < b + 1; line++) {
      x = (double)line/b * 400 + 50; // where to draw the lines

      SDL_RenderDrawLine(renderer, x, 50, x, 450);
    }    
}

int DrawAll (SDL_Window* window, SDL_Renderer* renderer, SDL_Surface* surface, Needle* needles, int nofneedle, int a, int b) {
  // Init SDL
  int width = 500;
  int height = 500;

  if ( SDL_Init( SDL_INIT_VIDEO) < 0) {
    std::cout << "Error: " << SDL_GetError() << std::endl;
    return 1;
  }

  if ( SDL_CreateWindowAndRenderer(width, height, 0, &window, &renderer) != 0) {
    std::cout << "Error: " << SDL_GetError() << std::endl;
    return 1;
  }

  surface = SDL_GetWindowSurface(window);
  SDL_bool done = SDL_FALSE;

  // Start drawing
  while(!done) {
    // event that closes window
    SDL_Event event;

    // Background is white
    SDL_SetRenderDrawColor(renderer, 255, 255, 255, SDL_ALPHA_OPAQUE);
    SDL_RenderClear(renderer);

    // Draw Board
    DrawBoard(renderer, a, b);

    // Draw Needles
    for (int needle_it = 0; needle_it < nofneedle; needle_it++) {
      DrawNeedle(renderer, needles[needle_it], a, b);
    }

    // Render image
    SDL_RenderPresent(renderer);

    // save and quit
    while(SDL_PollEvent(&event)) {
      if (event.type == SDL_QUIT) {
        done = SDL_TRUE;
      }
    }
  }
}

}
