
from Gene import *

class GeneType(object):
    """
    This class represents a category of genes.  For example, it could represent an integer gene
    """

    def __init__(self, generator, mutator, description=""):
        """
        :param generator: this function should return a random value.  The type of this value is the type of the gene
        :type generator: () -> type_of_gene
        :param mutator: this function should take a value for the gene and randomly mutate it.
        :type mutator: (type_of_gene) -> type_of_gene
        :param description: Useful for debugging
        """
        self.generator = generator
        self.mutator = mutator
        self.description = description

    def getRandomGene(self):
        """
        Create a new gene using the generator function
        :rtype: Gene
        """
        return Gene(self, self.generator())

    def __str__(self):
        return self.description + "   (" + str(type(self.generator())) + ")"