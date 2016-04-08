import math

from pyvolution.EvolutionManager import *
from pyvolution.GeneLibrary import *


"""
This example attempts to find a solution to the following system of equations:
a + b + c + d - 17 = 0
a^2 + b^2 - 5 = 0
sin(a) + c - d - 20 = 0

"""

def fitnessFunction(chromosome):
    """
    Given a "chromosome", this function must determine its fitness score
     The fitness score should be a floating point value.  If the fitness is zero or smaller
     then the chromosome will not be allowed to "reproduce"
    """

    #you can access the attributes of a chromosome using square brackets
    #the key is the description of the gene
    a = chromosome["a"]
    b = chromosome["b"]
    c = chromosome["c"]
    d = chromosome["d"]

    #for a perfect solution each of the values will be zero
    val1 = math.fabs(a + b + c + d - 17)
    val2 = math.fabs(math.pow(a, 2) + math.pow(b, 2) - 5)
    val3 = math.sin(a) + c - d - 20

    #minimize the "distance", this gives a better fitness estimate than summing the values
    dist = math.sqrt(math.pow(val1, 2) + math.pow(val2, 2) + math.pow(val3, 2))

    #number returned must be a positive floating point value
    if dist != 0:
        return 1 / dist #lower dist means better fitness, the closer to a good solution the higher this will be
    else:
        return None     #returning None indicates that a perfect solution has been found


#configure the evolution manager as you see fit
#see EvolutionManager.py for documentation on the arguments for this class
em = EvolutionManager(fitnessFunction,
                      individualsPerGeneration=100,
                      mutationRate=0.2,
                      maxGenerations=1000,
                      stopAfterTime=10,   #stop the simulation after 10 seconds
                      elitism=2,          #preserve the 2 most fit individuals unmutated in each generation
                      )

#this is a special gene type.  Instead of mutating randomly, the value of this gene is equal to 1/fitness.  As the
#fitness of the chromosome increases, this gene gets smaller and smaller
mutator = FloatInverseFit("mut", maxVal=0.01, startVal=1)

#standard floating point genes.  The mutation rate of these genes is dependant on the "mut" gene which is defined above
atype = FloatGeneType("a", generatorAverage=0, generatorSTDEV=100, mutatorGene="mut")
btype = FloatGeneType("b", generatorAverage=0, generatorSTDEV=100, mutatorGene="mut")
ctype = FloatGeneType("c", generatorAverage=0, generatorSTDEV=100, mutatorGene="mut")
dtype = FloatGeneType("d", generatorAverage=0, generatorSTDEV=100, mutatorGene="mut")

em.addGeneType(mutator)
em.addGeneType(atype)
em.addGeneType(btype)
em.addGeneType(ctype)
em.addGeneType(dtype)

result = em.run()