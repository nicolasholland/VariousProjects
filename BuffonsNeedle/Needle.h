#ifndef NEEDLE
#define NEEDLE
typedef struct Needle{

double x;
double y;
double phi;

} Needle;

// Create Needle
Needle Create(int g);

// If needle intersects line, return 1
int Intersect(Needle needle);
int Intersect2(Needle needle);

// Simulate Needle dropping
double Simulate(int nofNeedles, int b, Needle* needles);
#endif
