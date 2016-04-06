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
        """
        Generate a new individual randomly
        """
        genes = []
        for gType in self.geneTypes:
            genes.append(gType.getRandomGene())
        return Chromosome(self, genes)

    def __str__(self):
        result = "[\n"
        for gt in self.geneTypes:
            result += "\t" + str(gt) + "\n"
        result += "]"
        return result
