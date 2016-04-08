import random
import math

class Chromosome(object):

    class PerfectMatch(Exception):
        def __init___(self, perfectSpecimen):
            Exception.__init__(self, "Perfect match found")

    def __init__(self, chromosomeType, genes):
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
        self.fitness = None

        self.perfectMatch = False

    def copy(self):
        """
        Create a deep copy of this chromosome
        :rtype: Chromosome
        """
        newGenes = []
        for gene in self.genes:
            newGenes.append(gene.copy())
        return Chromosome(self.chromosomeType, newGenes)

    def mutate(self, mutationRate, mutationSTDEV):
        """
        Mutate genes with given probability
        :param mutationRate: the average number of times that each gene should be mutated.
                                0.5 means each gene has a 50% of being mutated
                                2.0 means each gene will be mutated two times, on average
        :type mutationRate: float
        :param mutationSTDEV: genes are mutated a number of times depending on a normal distribution, This is the
                                standard deviation
        """
        for gene in self.genes:
            mutations = random.normalvariate(mutationRate, mutationSTDEV)
            wholeMutations = int(math.floor(mutations))
            partialMutations = mutationRate - wholeMutations
            if partialMutations > random.uniform(0, 1):
                wholeMutations += 1
            for mutation in xrange(wholeMutations):
                gene.mutate(self)


    def doFitnessTest(self):
        self.fitness = self.chromosomeType.fitnessFunction(self)

        #we have tested the fitness.  If it is still None, then a perfect match must have been found
        if self.fitness is None:
            self.perfectMatch = True
            raise self.PerfectMatch(self)

    def getFitness(self):
        """
        Measure the fitness of this individual
        :return:
        """
        if self.perfectMatch:
            return "perfect match"
        elif self.fitness is None:
            self.doFitnessTest()
            return self.fitness
        else:
            return self.fitness

    def __str__(self):
        result = "[\n"
        for gene in self.genes:
            result += "\t" + str(gene) + "\n"
        result += "]"
        if self.fitness is not None:
            result += "  fitness: " + str(self.fitness)
        return result

    def __setitem__(self, key, value):
        """
        Set the value of a particular gene
        """
        for gene in self.genes:
            if gene.geneType.description == key:
                gene.value = value
                break

    def __getitem__(self, item):
        """
        Get the value of a particular gene
        :rtype: Gene
        """
        for gene in self.genes:
            if gene.geneType.description == item:
                return gene.value

    def __add__(self, other):
        """
        Takes two chromosomes and returns a child chromosome that is a mix of their genes
        :type other: Chromosome
        :rtype: Chromosome
        """
        newGenes = []
        for geneIndex in xrange(len(self.genes)):
            chosen = random.choice((self.genes[geneIndex], other.genes[geneIndex]))
            newGenes.append(chosen.copy())
        return Chromosome(self.chromosomeType, newGenes)

    def __lt__(self, other):
        return self.getFitness() < other.getFitness()

    def __gt__(self, other):
        return self.getFitness() > other.getFitness()

    def __le__(self, other):
        return self.getFitness() <= other.getFitness()

    def __ge__(self, other):
        return self.getFitness() >= other.getFitness()

    def __eq__(self, other):
        return self.getFitness() == other.getFitness()

    def __ne__(self, other):
        return self.getFitness() != other.getFitness()

    def data(self):
        """
        Convert to a form that can easily be encorporated into a yaml file
        """
        data = {}
        data["fitness"] = self.getFitness()
        data["genes"] = {}
        for gene in self.genes:
            data["genes"][gene.geneType.description] = gene.value
        return data