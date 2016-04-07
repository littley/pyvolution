import time
import signal
import os

from GenerationType import *
from ChromosomeType import *
from FileManager import *

class EvolutionManager(object):


    def __init__(self,
                 fitnessFunction,
                 individualsPerGeneration=100,
                 elitism=1,
                 randIndividuals=0,
                 randFitness=None,
                 mutationRate=0.2,
                 mutationSTDEV=0,
                 maxGenerations=None,
                 stopWithFitness=None,
                 stopAfterTime=None,
                 logDir=None,
                 generationsToKeep=0,
                 snapshotGenerations=None,
                 threads=1,
                 startingGeneration=None):
        """
        :param individualsPerGeneration: the size of the new generation
        :type individualsPerGeneration: int
        :param elitism: preserve the n most fit individuals without mutations or crossovers
        :type elitism: int
        :param randIndividuals: add n random chromosomes to the breeding population
        :type randIndividuals: int
        :param randFitness: random individuals may have very low fitness.  If not None, the maximum of this value and
                                the actual random fitness is used
        :type randFitness: float
        :param mutationRate: the average number of mutations each gene will undergo
        :type mutationRate: float
        :param mutationSTDEV: the standard deviation for the number of mutations each gene will undergo
        :type mutationSTDEV: float

        :param maxGenerations: stop computing after this many generations.  None means no limit
        :type maxGenerations: int
        :param stopWithFitness: stop computing if fitness meets or exceeds this value.  None means no limit
        :type stopWithFitness: float
        :param stopAfterTime: stop computing after this many seconds.  None means no limit
        :type stopAfterTime: float
        :param logDirL: if provided with a log directory then certain generations may be saved
        :type logDir: str
        :param generationsToKeep: the number of generations to save to the log directory.  For example, if set to 5
                                    then the 5 most recent generations will be saved
        :param snapshotGenerations: take a snapshot of the system very N trials
        :type snapshotGenerations: int
        :param threads: the number of threads to use for fitness tests
        :type threads: int
        :param startingGeneration: start with generation defined in YAML instead of a random generation
        :type startingGeneration: str

        """
        self.geneTypes = []
        self.startingChromosomes = []
        self.chromosomeType = None

        self.fitnessFunction = fitnessFunction
        self.individualsPerGeneration = individualsPerGeneration
        self.elitism = elitism
        self.randIndividuals  =  randIndividuals
        self.randFitness = randFitness
        self.mutationRate = mutationRate
        self.mutationSTDEV = mutationSTDEV
        self.maxGenerations = maxGenerations
        self.stopWithFitness = stopWithFitness
        self.stopAfterTime = stopAfterTime
        self.logDir = logDir
        self.generationsToKeep = generationsToKeep
        self.snapshotGenerations = snapshotGenerations
        self.threads = threads
        self.startingGenration = startingGeneration

        self.FM = FileManager()
        self.oldGenerations = []
        self.oldGenerations_perm = []

        def signal_handler(signal, frame):
            print "dumping data"
            self.dataDump()
            sys.exit(0)
        signal.signal(signal.SIGINT, signal_handler)


    def addGeneType(self, geneType):
        """
        Add a new gene type to the expiriment
        :type geneType: GeneType
        """
        if self.chromosomeType is not None:
            raise Exception("New gene types cannot be added after the chromosome template has been finalized!")
        self.geneTypes.append(geneType)

    def getChromomeTemplate(self):
        """
        Return a chromosome of the appropriate type.  Useful for creating specific chromosomes to be added
        :rtype: Chromosome
        """
        if self.chromosomeType is None:
            self.chromosomeType = ChromosomeType(self.fitnessFunction, self.geneTypes)
        return self.chromosomeType.getRandomChromosome()

    def addChromosome(self, chromsome):
        """
        Add a chomosome to the first generation.  This should not be called before adding all gene types
        :type chromsome: Chromosome
        """
        self.startingChromosomes.append(chromsome)

    def run(self):

        if self.chromosomeType is None:
            self.chromosomeType = ChromosomeType(self.fitnessFunction, self.geneTypes)

        generationType = GenerationType(self.chromosomeType)

        if self.startingGenration is None:
            currentGeneration = generationType.getRandomGeneration(max(0, self.individualsPerGeneration-len(self.startingChromosomes)))
        else:
            fobj = open(self.startingGenration)
            flist = []
            for line in fobj:
                flist.append(line)
            fline = "".join(flist)
            currentGeneration = generationType.fromYAML(fline)
            fobj.close()

        currentGeneration.population += self.startingChromosomes
        currentGeneration.doFitnessTests(threads=self.threads)

        print "The most fit individual in the starting generation is\n"
        print currentGeneration.getMostFit()

        startTime = None
        if self.stopAfterTime is not None:
            startTime = time.time()

        try:

            trials = 0
            while True:
                trials += 1

                #take a snapshot
                if self.snapshotGenerations is not None and trials % self.snapshotGenerations == 0:
                    self.oldGenerations_perm.append((trials, currentGeneration))
                #save this trial in temporary storage
                elif self.generationsToKeep > 0:
                    if len(self.oldGenerations) >= self.generationsToKeep:
                        self.oldGenerations = self.oldGenerations[1:]
                    self.oldGenerations.append((trials, currentGeneration))

                #exit conditions
                if self.maxGenerations is not None and trials > self.maxGenerations:
                    print "Maximum number of generations reached"
                    self.dataDump()
                    return currentGeneration.getMostFit()
                if self.stopWithFitness is not None and currentGeneration.getMostFit().fitness >= self.stopWithFitness:
                    print "Sufficient fitness achieved"
                    self.dataDump()
                    return currentGeneration.getMostFit()
                if self.stopAfterTime is not None and (time.time() - startTime) >= self.stopAfterTime:
                    print "Time limit reached"
                    self.dataDump()
                    return currentGeneration.getMostFit()

                print "-" * 100
                print "Begining computations for generation " + str(trials)

                nextGeneration = currentGeneration.getNextGeneration(self.individualsPerGeneration,
                                                                     self.elitism,
                                                                     self.randIndividuals,
                                                                     self.randFitness,
                                                                     self.mutationRate,
                                                                     self.mutationSTDEV)


                nextGeneration.doFitnessTests(threads=self.threads)


                print "The most fit individual in this generation is\n"
                print nextGeneration.getMostFit()

                currentGeneration = nextGeneration

        except Chromosome.PerfectMatch as e:
                print "A perfect match has been found"
                print e.message

                if self.generationsToKeep > 0:
                    if len(self.oldGenerations) >= self.generationsToKeep:
                        self.oldGenerations = self.oldGenerations[1:]
                    self.oldGenerations.append((trials, currentGeneration))
                self.dataDump()
                return e.message

    def dataDump(self):
        """
        Call this function to write all of the pending generations to disk
        """

        if self.logDir is not None:
            if not os.path.exists(self.logDir):
                os.mkdir(self.logDir)
            for trial in self.oldGenerations:
                self.FM.write(trial[1], self.logDir + "/" + str(trial[0]) + ".yaml")
            for trial in self.oldGenerations_perm:
                self.FM.write(trial[1], self.logDir + "/" + str(trial[0]) + ".yaml")


if __name__=="__main__":

    import math
    import sys
    import time

    from GeneLibrary import *

    """

    attempt to find a solution to the following system of equations

    a + b + c + d = 17
    a^2 + b^2 = 5
    sin(a) + c + d = 20

    """

    def fitnessFunction(chromosome):

        a = chromosome["a"]
        b = chromosome["b"]
        c = chromosome["c"]
        d = chromosome["d"]


        #for a perfect solution each of the values will be zero
        val1 = math.fabs(a + b + c + d - 17)
        val2 = math.fabs(math.pow(a, 2) + math.pow(b, 2) - 5)
        val3 = math.sin(a) + c - d - 20

        #minimize the distance from 0
        dist = math.sqrt(math.pow(val1, 2) + math.pow(val2, 2) + math.pow(val3, 2))

        #number returned must be a positive floating point value

        if dist != 0:
            return 1 / dist
        else:
            return None

    em = EvolutionManager(fitnessFunction,
                 individualsPerGeneration=100,
                 elitism=1,
                 randIndividuals=0,
                 randFitness=None,
                 mutationRate=0.2,
                 mutationSTDEV=0,
                 maxGenerations=1000,
                 stopWithFitness=None,
                 stopAfterTime=None,
                 logDir="./out",
                 generationsToKeep=3,
                 snapshotGenerations=100,
                 threads=1)


    mutator = FloatInverseFit("mut", maxVal=1, startVal=1)

    atype = FloatGeneType("a", generatorAverage=0, generatorSTDEV=100, averageMutation=0, mutatorGene="mut")
    btype = FloatGeneType("b", generatorAverage=0, generatorSTDEV=100, averageMutation=0, mutatorGene="mut")
    ctype = FloatGeneType("c", generatorAverage=0, generatorSTDEV=100, averageMutation=0, mutatorGene="mut")
    dtype = FloatGeneType("d", generatorAverage=0, generatorSTDEV=100, averageMutation=0, mutatorGene="mut")

    em.addGeneType(mutator)
    em.addGeneType(atype)
    em.addGeneType(btype)
    em.addGeneType(ctype)
    em.addGeneType(dtype)

    result = em.run()