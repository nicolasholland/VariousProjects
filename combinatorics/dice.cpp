// FILE BUILD BY sides.py
#include <stdio.h>
#include <stdlib.h>

#include <map>

int main(int argc, char** argv) {
int n = 6;
int face = 0;
int total = 0;
 for (int i=1; i <= n; i++)
 for (int ii=1; ii <= n; ii++)
 for (int iii=1; iii <= n; iii++)
 for (int iiii=1; iiii <= n; iiii++)
 for (int iiiii=1; iiiii <= n; iiiii++)
 for (int iiiiii=1; iiiiii <= n; iiiiii++)
 for (int iiiiiii=1; iiiiiii <= n; iiiiiii++)
 for (int iiiiiiii=1; iiiiiiii <= n; iiiiiiii++)
 for (int iiiiiiiii=1; iiiiiiiii <= n; iiiiiiiii++)
 for (int iiiiiiiiii=1; iiiiiiiiii <= n; iiiiiiiiii++)
  {
  total++;  printf("%d %d %d %d %d %d %d %d %d %d \n",i,ii,iii,iiii,iiiii,iiiiii,iiiiiii,iiiiiiii,iiiiiiiii,iiiiiiiiii);
  std::map<int, int> ARR;
  // check if element shows only 2 faces
  ARR[i]++;
  ARR[ii]++;
  ARR[iii]++;
  ARR[iiii]++;
  ARR[iiiii]++;
  ARR[iiiiii]++;
  ARR[iiiiiii]++;
  ARR[iiiiiiii]++;
  ARR[iiiiiiiii]++;
  ARR[iiiiiiiiii]++;
  if (ARR.size() == 2)
   face++;
  }
printf("Number of elements with 2 faces is %d from %d\n", face, total);
return 0;
}
