import random

# Code inspired by Programming Collective Intelligence by Toby Segaran
def geneticoptimize(nofparams, net, data, costf, popsize=50, step=1, mutprob=0.2, elite=0.2, maxiter=300):
  # Mutation Operation
  def mutate(vec):
    i=random.randint(0, nofparams-1)
    return vec[0:i]+[vec[i] + random.random() * 2 - 1] + vec[i+1:]


  # Crossover Operation
  def crossover(r1,r2):
    i=random.randint(1,nofparams-1)
    return r1[0:i]+r2[i:]

  # Build the initial population
  pop=[]
  for i in range(popsize):
    vec=[random.random() * 2 - 1
          for i in range(nofparams)]
    pop.append(vec)

  # How many winners from each generation?
  topelite=int(elite*popsize)

  # Main loop
  for i in range(maxiter):
    scores = []
    for v in pop:
      net.setParams(v)
      scores.append((-costf(net, data)[0], v))

    scores.sort( )
    ranked=[v for (s,v) in scores]

    # Start with the pure winners
    pop=ranked[0:topelite]

    # Add mutated and bred forms of the winners
    while len(pop)<popsize:
      if random.random( )<mutprob: 
        # Mutation
        c=random.randint(0,topelite)
        pop.append(mutate(ranked[c]))

      else:
        # Crossover
        c1=random.randint(0,topelite)
        c2=random.randint(0,topelite)
        pop.append(crossover(ranked[c1],ranked[c2]))

    # Print current best score
    if i%10 == 0:
	print "gen.opt.: ", scores[0][0], i
  return scores[0][1]
