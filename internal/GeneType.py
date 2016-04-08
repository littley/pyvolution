from Gene import *

class GeneType(object):
    """
    This class represents a category of genes.  For example, it could represent an integer gene
    """

    def __init__(self, generator, mutator, description, combiner=None):
        """
        :param generator: this function should return a random value.  The type of this value is the type of the gene
        :type generator: () -> type_of_gene
        :param mutator: this function should take a value for the gene and randomly mutate it.  It may be a function
                            of the chromosome.  Returning None indecates a perfect match
        :type mutator: (type_of_gene, chromosome) -> type_of_gene
        :param description: The name/description/ID of the gene
        :param combiner: An optinal function.  If provided, this function is used when crossing over two genes
                            Useful for when crossover needs to be more complex than "chose one or the other"
        :type combiner: (Gene, Gene) -> Gene
        """
        self.generator = generator
        self.mutator = mutator
        self.description = description
        self.combiner = combiner

    def getRandomGene(self):
        """
        Create a new gene using the generator function
        :rtype: Gene
        """
        return Gene(self, self.generator())

    def __str__(self):
        return self.description + "   (" + str(type(self.generator())) + ")"