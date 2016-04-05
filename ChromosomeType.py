from Chromosome import *

class ChromosomeType(object):


    def __init__(self, fitnessFunction, geneTypes):
        """
        :param fitnessFunction: A function to measure the fitness of an individual
        :type fitnessFunction: (Chromosome) -> float
        :param geneTypes: a list of gene types that make up a chromosome of this type
        :type geneTypes: [GeneType]
        """
        self.geneTypes = geneTypes                       #type: [GeneType]
        self.fitnessFunction = fitnessFunction           #type: (Chromosome) -> float


    def getRandomChromosome(self):

        genes = []

        for gType in self.geneTypes:
            genes.append(gType.getRandomGene())

        return Chromosome(self, genes)
