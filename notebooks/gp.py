"""
Code inspired by Toby Segarans Collective Intelligence.
"""
import numpy as np
from copy import deepcopy

np.warnings.filterwarnings('ignore')

class fwrapper:
    """
    A wrapper for the functions that will be used on function nodes. Its member
    variables are the name of the function, the function itself, and the number
    of parameters it takes.
    """
    def __init__(self,function,childcount,name):
            self.function=function
            self.childcount=childcount
            self.name=name

class node:
    """
    The class for function nodes (nodes with children). This is initialized
    with an fwrapper. When evaluate is called, it evaluates the child nodes
    and then applies the function to their results.
    """
    def __init__(self,fw,children):
        self.function=fw.function
        self.name=fw.name
        self.children=children

    def evaluate(self,inp):
        results=[n.evaluate(inp) for n in self.children]
        return self.function(results)

    def display(self,indent=0):
        print((' '*indent)+self.name)
        for c in self.children:
            c.display(indent+1)

class paramnode:
    """
    The class for nodes that only return one of the parameters passed to the
    program. Its evaluate method returns the parameter specified by idx.
    """
    def __init__(self,idx):
        self.idx=idx

    def evaluate(self,inp):
        return inp[self.idx]

    def display(self,indent=0):
        print('%sp%d' % (' '*indent,self.idx))

    def __gt__(self, other):
        return False


class constnode:
    """
    Nodes that return a constant value. The evaluate method simply returns the
    value with which it was initialized.
    """
    def __init__(self,v):
        self.v=v

    def evaluate(self,inp):
        return self.v

    def display(self,indent=0):
        print('%s%f' % (' '*indent,self.v))


addw=fwrapper(lambda l:l[0]+l[1],2,'add')
subw=fwrapper(lambda l:l[0]-l[1],2,'subtract')
mulw=fwrapper(lambda l:l[0]*l[1],2,'multiply')
expw=fwrapper(lambda l:np.exp(l[0]), 1,'exp')
sinw=fwrapper(lambda l:np.sin(l[0]), 1,'sin')
cosw=fwrapper(lambda l:np.cos(l[0]), 1,'cos')

flist=[addw,mulw,subw, expw, sinw, cosw]

def makerandomtree(pc,maxdepth=4,fpr=0.5,ppr=0.6):
    if np.random.rand()<fpr and maxdepth>0:
        f=np.random.choice(flist)
        children=[makerandomtree(pc,maxdepth-1,fpr,ppr)
                  for i in range(f.childcount)]
        return node(f,children)
    elif np.random.rand()<ppr:
        return paramnode(np.random.randint(0,pc-1))
    else:
        return constnode(np.random.rand()*10)


def mutate(t,pc,probchange=0.1):
    if np.random.rand()<probchange:
        return makerandomtree(pc)
    else:
        result=deepcopy(t)
        if isinstance(t,node):
            result.children=[mutate(c,pc,probchange) for c in t.children]
        return result

def crossover(t1,t2,probswap=0.7,top=1):
    if np.random.rand()<probswap and not top:
        return deepcopy(t2)
    else:
        result=deepcopy(t1)
        if isinstance(t1,node) and isinstance(t2,node):
            result.children=[crossover(c,np.random.choice(t2.children),
                                       probswap,0) for c in t1.children]

        return result

def evolve(pc,popsize,rankfunction,maxgen=500,
           mutationrate=0.1,breedingrate=0.4,pexp=0.7,pnew=0.05):

    def selectindex( ):
        """
        Returns a random number, tending towards lower numbers. The lower pexp
        is, more lower numbers you will get
        """
        return int(np.log(np.random.rand())/np.log(pexp))

    population=[makerandomtree(pc) for i in range(popsize)]
    for i in range(maxgen):
        scores=rankfunction(population)
        if scores[0][0]==0: break

        newpop=[scores[0][1],scores[1][1]]
        while len(newpop)<popsize:
            if np.random.rand()>pnew:
                entry = mutate(crossover(scores[selectindex()][1],
                                         scores[selectindex()][1],
                                         probswap=breedingrate),
                                         pc,probchange=mutationrate)
            else:
                entry = makerandomtree(pc)
            newpop.append(entry)

        population=newpop

    scores[0][1].display()
    return scores[0][1]

def getrankfunction(dataset, scorefunction):
    def rankfunction(population):
        scores=[(scorefunction(t,dataset), t) for t in population]
        scores.sort(key=lambda x: x[0])
        return scores
    return rankfunction
