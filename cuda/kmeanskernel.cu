#include <stdio.h>
#include <ctime>
#include <stdlib.h>

__global__
void kmeanspredict(int n, int nofc, float *x, float *y, float* model, float* label)
{
  int i = blockIdx.x*blockDim.x + threadIdx.x;

  if (i >= n)
  	return;

  int iter;
  double dist = 9999;
  double tmp = 0;
  double res = 2;

  for (iter = 0; iter < nofc; iter++) {
  	tmp = sqrt((x[i] - model[iter]) * (x[i] - model[iter]) +
  			   (y[i] - model[iter + nofc]) * (y[i] - model[iter + nofc]));
  	res = tmp < dist ? iter : res;
  	dist = tmp < dist ? tmp : dist;
  }
  label[i] = res;
}

int main(void)
{
  int N = 100000000;
  float *feature1, *feature2, *d_feature1, *d_feature2, *d_model;
  float *label, *d_label;
  feature1 = (float*)malloc(N*sizeof(float));
  feature2 = (float*)malloc(N*sizeof(float));
  label = (float*)malloc(N*sizeof(int));

  cudaMalloc(&d_feature1, N*sizeof(float));
  cudaMalloc(&d_feature2, N*sizeof(float));
  cudaMalloc(&d_label, N*sizeof(float));

  float model[] = {0.79314066 , 0.40563098, 0.27847279,
                   0.27847279, 0.8073302, 0.28528738};
  cudaMalloc(&d_model, 6*sizeof(float));

  std::srand(time(NULL));

  for (int i = 0; i < N; i++) {
	feature1[i] = rand();
	feature2[i] = rand();
  }

  clock_t begin = std::clock();

  cudaMemcpy(d_feature1, feature1, N*sizeof(float), cudaMemcpyHostToDevice);
  cudaMemcpy(d_feature2, feature2, N*sizeof(float), cudaMemcpyHostToDevice);
  cudaMemcpy(d_model, model, 6*sizeof(float), cudaMemcpyHostToDevice);


  kmeanspredict<<<(N+255)/256, 256>>>(N, 3, d_feature1, d_feature2, d_model, d_label);


  cudaMemcpy(feature2, d_feature2, N*sizeof(float), cudaMemcpyDeviceToHost);
  cudaMemcpy(label, d_label, N*sizeof(float), cudaMemcpyDeviceToHost);

  clock_t end = std::clock();
  double elapsed_secs = double(end - begin) / CLOCKS_PER_SEC;
  printf("measured time: %lf\n", elapsed_secs);

  cudaFree(d_feature1);
  cudaFree(d_feature2);
  cudaFree(d_label);
  free(feature1);
  free(feature2);
  free(label);
}
