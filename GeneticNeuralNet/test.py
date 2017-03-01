# params:
dim = 2
nofNodes = 3
nofLayers = 2
nofSamples = 50

############################
# CREATE NEURAL NET
import neuralNet

net = neuralNet.neuralNet(nofNodes, dim, nofLayers)

############################
# CREATE SYNTHETIC DATA
import synthData

f = synthData.F(dim)

data = synthData.synthData(nofSamples, dim, synthData.g)
synthData.diversity(data)

###########################
# VISUALIZE DATA
from matplotlib import pyplot as plt

for d in data:
  if d[1] > 0:
    c = "red"
  else:
    c = "green"
  plt.plot(d[0][0], d[0][1], '.', color=c)
plt.show()


###########################
# TRAIN NEURAL NET
import genOpt

score, total = neuralNet.TestNeuralNet(net, data)
print("Initial Score:\t%d of %d"%(score,total))

params = genOpt.geneticoptimize(nofLayers*nofNodes*dim, net, data, neuralNet.TestNeuralNet)

net.setParams(params)
score, total = neuralNet.TestNeuralNet(net, data)
print("Final Score:\t%d of %d"%(score,total))


###########################
# VISUALIZE RESULT
import numpy as np

for d in data:
  if np.sign(net.runNetwork(d[0])) > 0:
    c = "green"
  else:
    c = "red"
  plt.plot(d[0][0], d[0][1], '.', color=c)
plt.show()

