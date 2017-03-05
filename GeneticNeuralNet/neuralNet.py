import numpy as np

# A node takes an input vector and outputs an integer.
# Every layer has the same amount of nodes and they are fully connected.
class Node:
  def __init__(self, dim):
    self.dim = dim
    self.params = []

    # Init all params to zero
    for d in range(dim):
      self.params.append(0)

  def output(self, inputvector):
    # All nodes have the same amount of parameters.
    # However, the first hidden layer only needs the 
    # amount of parameters equal to the dimension of the input.
    Range = min(len(inputvector), len(self.params))    

    ret = 0
    for param in range(Range):
      ret = ret + self.params[param] * inputvector[param]
    return ret

# This neural network takes one input vector, 
# outputs an integer and uses one hidden layer.
class neuralNet:
  def __init__(self, nofnodes, dim, noflayers):
    self.dim = dim
    self.nofnodes = nofnodes
    self.nodes = []
    self.noflayers = noflayers

    for n in range(nofnodes * noflayers):
      node = Node(nofnodes)
      self.nodes.append(node)

  def printParams(self):
    count = 0
    for node in self.nodes:
      for param in node.params:
        print("%d:\t%f"%(count,param))
        count = count + 1

  def setParams(self, params):
    if len(params) != self.dim * self.nofnodes * self.noflayers:
      print("Not enough params")
      return
    
    count = 0
    for node in range(self.nofnodes * self.noflayers):
      for param in range(self.dim):
        self.nodes[node].params[param] = params[count]
        count = count + 1

  def runNetwork(self, inputvector):
    if len(inputvector) != self.dim:
      print("wrong input dimension")
      return
    ret = 0

    for l in range(self.noflayers-1):
      vec = []
      for n in range(self.nofnodes):
        vec.append(np.sign(
		self.nodes[l*self.nofnodes + n].output(inputvector)))
      inputvector = vec

    for n in range(self.nofnodes):
      ret = ret +  self.nodes[(self.noflayers-1) * self.nofnodes + n ].output(inputvector)
    return ret

def TestNeuralNet(net, data):
  nofCorrect = 0
  total = 0

  for d in data:
    res = np.sign(net.runNetwork(d[0]))

    if res == d[1]:
      nofCorrect = nofCorrect + 1

    total = total + 1

  return nofCorrect, total
