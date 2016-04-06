import copy

class Gene(object):
    """
    An instance of a gene
    """

    def __init__(self, geneType, value):
        self.geneType = geneType
        self.value = value

    def copy(self):
        """
        Return a deep copy of this gene
        """
        return Gene(self.geneType, copy.deepcopy(self.value))

    def mutate(self):
        """
        Cause this gene to be mutated
        """
        self.value = self.geneType.mutator(self.value)

    def __str__(self):
        return self.geneType.description + "   (" + str(self.value) + ")"