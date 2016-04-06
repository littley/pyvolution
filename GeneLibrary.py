import random
import sys

from GeneType import *

def FloatGeneType(description,
                  minVal=None,
                  maxVal=None,
                  generatorAverage=None,
                  generatorSTDEV=1,
                  averageMutation=0,
                  mutationSTDEV=1):
    """
    Regurn a GeneType configured as specified
    :param description: the description/name of this gene
    :type description: str
    :param minVal: the minimum value allowed for this gene.  Values that end up smaller will be rounded to the minVal
                    A value of None means that there is no minVal
    :type minVal: float
    :param maxVal: the maximum value allowed for this gene.  Values that end up larger will be rounded to the maxVal
                    A value of None means that there is no maxVal
    :param generatorAverage: the average value that is generated for new genes
                    A value of None will cause a flat distribution to be used
    :param generatorSTDEV: the standard devation of the values generated for new genes
    :param averageMutation: the average amount that this gene changes during each mutation
    :param mutationSTDEV:
    :rtype: GeneType
    """

    if minVal is None:
        minVal = -1 * sys.maxint
    if maxVal is None:
        maxVal = sys.maxint

    def generator():
        if generatorAverage is None:
            return random.uniform(minVal, maxVal)
        else:
            result = random.normalvariate(generatorAverage, generatorSTDEV)
            if maxVal is not None:
                result = min(result, maxVal)
            if minVal is not None:
                result = max(result, minVal)
            return result

    def mutator(originalValue):
        result = originalValue + random.normalvariate(averageMutation, mutationSTDEV)
        result = max(min(result, maxVal), minVal)
        return result

    return GeneType(generator, mutator, description)
