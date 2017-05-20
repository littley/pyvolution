from multiprocessing import Process, Array

from BreedingPool import *

class Generation():
    """
    A group of chromosomes
    """

    def __init__(self, generationType, population):
        self.generationType = generationType
        self.population = population

    def copy(self):
        """
        Return a deep copy of this generation
        :rtype: Generation
        """
        newPopulation = []
        for chromosome in self.population:
            newPopulation.append(chromosome.copy())
        return Generation(self.generationType, newPopulation)

    def getNextGeneration(self, size, elitism, randIndividuals, randFitness, mutationRate, mutationSTDEV):
        """
        Return a new generation of individuals.  To get multithreading, call doFitnessTests before this function
        :param size: the size of the new generation
        :type size: int
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
        :rtype: Generation
        """

        newPopulation = []
        breedingPopulation = []

        #preserve some elite individuals
        newPopulation += self.getNMostFit(elitism)

        #add all individuals with fitness greater than 0 to the breeding population
        for chromosome in self.population:
            if chromosome.getFitness() > 0:
                breedingPopulation.append(chromosome)

        #add some randomized individuals to the breeding population
        for r in xrange(randIndividuals):
            rando = self.generationType.chromosomeType.getRandomChromosome()
            rando.doFitnessTest()
            if randFitness is not None:
                rando.fitness = max(rando.fitness, randFitness)
            breedingPopulation.append(rando)

        #breed a new generation of chromosomes
        breedingPool = BreedingPool(breedingPopulation)
        while len(newPopulation) < size:
            newChromosome = breedingPool.get() + breedingPool.get()
            newChromosome.mutate(mutationRate, mutationSTDEV)
            newPopulation.append(newChromosome)

        return Generation(self.generationType, newPopulation)



    def doFitnessTests(self, threads=1):
        """
        Measure the fitness of each chromosome (if the chromosome has not been previously measured)
        :param threads: the number of theads to use on this operation
        """
        
        print "Generation: fitness tests started. Threads = ", threads
        
        if threads <= 1:
            for chromosome in self.population:
                chromosome.doFitnessTest()
        else:
            fitness_calculation_result = Array('d', len(self.population))
            def testFunct(chromosomes, start, end):
                print end - start
                index = start;
                while index < end:
                    #print "Chromosome", index, "fitness test"
                    chromosomes[index].doFitnessTest()
                    fitness_calculation_result[index] = chromosomes[index].fitness
                    index += 1                
            
            # --- Commented by MR. I do not understand why we do this work twice: 
            # --- 1 in common, second in treads (in testFunct)
            #for chromosome in self.population:
            #    chromosome.doFitnessTest()

            procs = []
            begin = 0          
            chunksize = int(math.floor(len(self.population) / threads))
            for t in xrange(threads):
                p = None
                if t+1 == threads: #if it is the last thread then give it all remaining
                    p = Process(target=testFunct, args=(self.population,begin,len(self.population)))
                else:
                    p = Process(target=testFunct, args=(self.population,begin,begin+chunksize))
                p.start()
                begin += chunksize
                procs.append(p)
            for p in procs:
                p.join()
            # Added by MR Using shared array to get caclulated data in main thread
            for i in xrange(len(self.population)):
                self.population[i].fitness = fitness_calculation_result[i]
                
    def getMostFit(self):
        """
        Return the most fit individual in a generation.  Returns None if no individual is more than "0 fit"
        :rtype: Chromosome
        """
        mostFit = -1
        rVal = None
        for chromosome in self.population:
            fitness = chromosome.getFitness
            if fitness > 0 and fitness > mostFit:
                mostFit = fitness
                rVal = chromosome
        return rVal

    def getNMostFit(self, N):
        """
        Return the N members of this generation that have the highest fitness
        :rtype: [Chromosome]
        """
        if N == 0:
            return []
        self.population = sorted(self.population)
        return self.population[-1 * N:]

    def data(self):
        """
        Return an object that can be used to convert a generation to yaml
        """
        data = {}
        for index, chromosome in enumerate(self.population):
            data[index] = chromosome.data()
        return data