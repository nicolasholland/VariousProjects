#include <iostream>
#include <time.h>

#include "Sin2Col.h"
#include "Sin2D.h"
#include "SDL2/SDL.h"


int VisualizeWave (SDL_Window* window, SDL_Renderer* renderer, SDL_Surface* surface, double* wave) {
  // Init SDL
  if ( SDL_Init( SDL_INIT_VIDEO) < 0) {
    std::cout << "Error: " << SDL_GetError() << std::endl;
    return 1;
  }

  if ( SDL_CreateWindowAndRenderer(WIDTH, HEIGHT, 0, &window, &renderer) != 0) {
    std::cout << "Error: " << SDL_GetError() << std::endl;
    return 1;
  }

  surface = SDL_GetWindowSurface(window);
  SDL_bool done = SDL_FALSE;

  clock_t this_time = clock();
  clock_t last_time = this_time;
  double time_counter = 0;

  double t = 0;

  // Start drawing
  while(!done) {
    // event that closes window
    SDL_Event event;

    // Background is white
    SDL_SetRenderDrawColor(renderer, 255, 255, 255, SDL_ALPHA_OPAQUE);
    SDL_RenderClear(renderer);

    // compute wave
    wave = Sin2D(wave, WIDTH, HEIGHT, t);

    // color wave
    for (int w=0; w < WIDTH; w++)
      for (int h=0; h < HEIGHT; h++) {
        RGB rgb = D2RGB(.5*(wave[w*WIDTH+h]+1));

        SDL_SetRenderDrawColor(renderer, rgb.R, rgb.G, rgb.B, SDL_ALPHA_OPAQUE);
        SDL_RenderDrawPoint(renderer, w, h);
    }

    t -= .5;

    // Render image
    SDL_RenderPresent(renderer);

    SDL_Delay(50);

    // save and quit
    while(SDL_PollEvent(&event)) {
      if (event.type == SDL_QUIT) {
        done = SDL_TRUE;
      }
    }
  }
}

// piecewise linear function from [0,1] to RGB
RGB D2RGB (double c) {
  RGB ret;

  if (c < .25) {
    ret.R = 51;
    ret.G = 816 * c;
    ret.B = 255;      
  } else if (c < .5) {
    ret.R = 51;
    ret.G = 255;
    ret.B = -816 * c + 459;      
  } else if (c < .75) {
    ret.R = 816 * c - 357;
    ret.G = 255;
    ret.B = 51;      
  } else if (c > .75) {
    ret.R = 255;
    ret.G = -816 * c + 867;
    ret.B = 51;
  }

  return ret;
}

