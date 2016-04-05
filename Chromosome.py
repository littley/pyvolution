import math

class Chromosome(object):

    def __init__(self, chromosomeType, genes, mutationRate=-1, mutationSTDEV=1):
        """
        :param chromosomeType: a template for the chromosome
        :type chromosomeType: ChromosomeType
        :param genes: a list of genes
        :param mutationRate: the average number of genes that will be mutated in each round
        :type mutationRate: float
        :param mutationSTDEV: the standard deviation of the number of genes to be mutated each round
        :type mutationSTDEV: float
        :type genes: [Gene]
        """
        self.chromosomeType = chromosomeType
        self.genes = genes

        self.mutationRate = mutationRate
        self.mutationSTDEV = mutationSTDEV

        if self.mutationRate == -1:
            self.mutationRate = math.ceil(0.1 * len(genes)) #heuristic


    def copy(self):
        newGenes = []
        for gene in self.genes:
            newGenes.append(gene.copy())
        return Chromosome(self.chromosomeType, newGenes)

    def mutate(self):
        pass

    def combine(self, other):
        pass

    def test(self):
        """
        Measure the fitness of this individual
        :return:
        """
        return self.chromosomeType.fitnessFunction(self)