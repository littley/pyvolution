import yaml

from internal.Generation import *

class GenerationType(object):
    """
    This class represents a type of a population of individuals
    """

    def __init__(self, chromosomeType):
        self.chromosomeType = chromosomeType

    def getRandomGeneration(self, size):
        """
        Get a generation of randomly generated individuals
        :param size:
        :rtype: Generation
        """
        newPopulation = []
        for i in xrange(size):
            newPopulation.append(self.chromosomeType.getRandomChromosome())
        return Generation(self, newPopulation)

    def fromYAML(self, data):
        data = yaml.load(data)
        newPopulation = []
        for key in data:
            newPopulation.append(self.chromosomeType.fromYAML(data[key]))
        return Generation(self, newPopulation)