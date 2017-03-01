import random
import numpy as np
import math

# This fuction is used to create functions
def F(dim):
  values = []
  for d in range(dim):
    values.append((random.random() * 2 - 1))

  def f(vec):
    ret = 0
    for v in range(len(vec)):
      ret = ret + values[v]  * vec[v]  # linear
      #ret = ret + values[v]  * math.sin(vec[v]) # nonlinear
    return np.sign(ret)
  
  return f

# This function assumes 2 dim vectors
def g(vec):
    ret = 0
    if vec[0] < 5 and vec[1] < 5:
      ret = -1
    else:
      ret = 1
    return ret

# This function tells us how diverse the synthetic data is
def diversity(data):
  nofNeg = 0
  nofPos = 0

  for d in data:
   if d[1] > 0:
     nofPos = nofPos + 1
   else:
     nofNeg = nofNeg + 1
  print("nofPos:\t%d\nnofNeg:\t%d"%(nofPos,nofNeg))

# This function creates some synthetic data:
# (vector, label)
def synthData(size, dim, f, lX = 0, uX = 10, lY = 0, uY = 10):
  ret = []

  # create data
  for s in range(size):      
    valx = random.random() # [0,1]
    valy = random.random() # [0,1]

    valx = valx * (uX - lX) #[0, uX-lX]
    valy = valy * (uY - lY) #[0, uY-lY]

    valx = valx + lX #[lX, uX]
    valy = valy + lY #[lY, uY]

    vec = [valx, valy]  

    ret.append([vec,f(vec)])

  return ret
