import random
import math

class BreedingPool(object):
    """
    This class is a container for Chromosomes.  Allows efficient selection of chromosomes to be "bred".

    This class implements a binary tree
    """

    class node():
        """
        Each node represents the "value" of a single chromosome.  Used to map a random number to a particular chromosome
        """
        def __init__(self, minVal, maxVal, chromosome):
            self.min = minVal
            self.max = maxVal
            self.chromosome = chromosome

            self.left = None
            self.right = None

        def __eq__(self, other):
            """
            Given a floating point number, a cmap will return true for "==" if the number
                falls within the range of the cmap
            """
            if type(other) is type(self):
                return self.min == other.min
            return self.min <= other and self.max >= other
        def __ne__(self, other):
            if type(other) is type(self):
                return self.min != other.min
            return not self.__eq__(other)
        def __lt__(self, other):
            if type(other) is type(self):
                return self.min < other.min
            return self.max < other
        def __gt__(self, other):
            if type(other) is type(self):
                return self.min > other.min
            return self.min > other
        def __le__(self, other):
            if type(other) is type(self):
                return self.min <= other.min
            return self.__eq__(other) or self.__lt__(other)
        def __ge__(self, other):
            if type(other) is type(self):
                return self.min >= other.min
            return self.__eq__(other) or self.__lt__(other)

    def __init__(self, population):
        allNodes = []
        self.max = 0.0        #used to track the maximum value, used by random number generator
        for chromosome in population:
            increase = chromosome.getFitness()
            allNodes.append(self.node(self.max, self.max + increase, chromosome))
            self.max += increase

        allNodes.sort()
        self.root = self.makeTree(allNodes)


    def makeTree(self, pop):
        """
        Given a sorted list of nodes, recursively construct a binary tree
        :param pop: a sorted list of nodes
        :return: the root of the tree
        """

        if len(pop) == 0:
            return None
        elif len(pop) == 1:
            return pop[0]


        middleIndex = int(math.floor(len(pop) / 2))
        leftList = pop[:middleIndex]
        root = pop[middleIndex]
        rightList = pop[middleIndex+1:]

        root.left = self.makeTree(leftList)
        root.right = self.makeTree(rightList)

        return root

    def findChromosome(self, n, target):
        """
        Recursively search the tree for a chromosome
        :param n: a node in the tree
        :type n: node
        :param target: look for a node that equals this target
        :type target: float
        :rtype: Chromosome
        """

        if n is None:
            return None

        if n == target:
            return n.chromosome
        elif target < n:
            return self.findChromosome(n.left, target)
        elif target > n:
            return self.findChromosome(n.right, target)
        else:
            return None


    def get(self):
        val = random.uniform(0, self.max)
        return self.findChromosome(self.root, val)