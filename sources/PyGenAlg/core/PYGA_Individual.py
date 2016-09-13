# -*- mode: python; py-indent-offset: 4; tab-width: 4; coding: iso-8859-1 -*-

#######################################################################
# Author: Deau Raphaël
#
# Copyright 2011 - 2016
# License: Creative Commons Attribution Non-commercial 4.0
# Full text: https://creativecommons.org/licenses/by-nc/4.0/legalcode
#
#######################################################################

#-----------------------
#
# Start date: 18/07/2011
#
#-----------------------

from sys import version_info
if version_info[0] >= 3:
    unicode = str

from multiprocessing import Process

from PyGenAlg.core.PYGA_Exceptions import PYGA_MethodMustBeOverloaded

class PYGA_Individual(object):

    MULTI_OBJ = False
    CURRENT_GENERATION = 0

    @classmethod
    def SET_BEHAVIOR(cls, behaviorInstance):
        cls.__behav = behaviorInstance

    @classmethod
    def getParam(cls, paramName):
        paramLabel = cls.__behav.getParamFromKeyword(paramName)
        if paramLabel is None:
            # TODO: Exception
            raise Exception(u"Unkown parameter " + unicode(paramName))
        return cls.__behav.getParam(paramLabel)

    def __init__(self):
        self.__fitness = None
        self.__optimised_fitness = None
        self.__numGenCreation = self.CURRENT_GENERATION

    @classmethod
    def generate(cls):
        """
        This class method must generate an individual.
        @return: The generated individual
        @rtype: Individual 
        """
        raise PYGA_MethodMustBeOverloaded('ERROR: This function (Individual.generate) must be defined in derivated class.')

    def saveIndividual(self, fid):
        raise PYGA_MethodMustBeOverloaded('ERROR: This function (Individual.saveIndividual) must be defined in derivated class.')
        
    @classmethod
    def loadIndividual(cls, fid):
        raise PYGA_MethodMustBeOverloaded('ERROR: This function (Individual.loadIndividual) must be defined in derivated class.')

    @classmethod
    def parseIndividual(cls, indivStruct):
        raise PYGA_MethodMustBeOverloaded('ERROR: This function (Individual.parseIndividual) must be defined in derivated class.')

    def fitness(self, population):
        raise PYGA_MethodMustBeOverloaded('ERROR: This function (Individual.fitness) must be defined in derivated class.')

    def objectives(self, population):
        raise PYGA_MethodMustBeOverloaded('ERROR: This function (Individual.objectives) must be defined in derivated class.')

    def needCompute(self):
        return self.__fitness is None

    def __computeObjectives(self, population, pipe=None, indivID=None):
        if self.MULTI_OBJ:
            obj = self.objectives(population)
        else:
            obj = self.fitness(population)
        if pipe is not None:
            # TODO: may not work, use shared object
            pipe.send([self, indivID])
            pipe.close()
        return obj

    def computeObjectives(self, population, processList=None, pipe=None, indivID=None):
        needCompute = self.needCompute()
        if needCompute:
            if self.getParam("max_process") != 1:
                p = Process(target=self.__computeObjectives, args=(population, pipe, indivID))
                p.start()
                processList.append(p)
            else:
                self.__fitness = self.__computeObjectives(population)
                self.__optimised_fitness = self.__fitness
        return needCompute

    @classmethod
    def computeMultiObjFitness(cls, population):
        raise PYGA_MethodMustBeOverloaded('ERROR: This function (Individual.computeMultiObjFitness) must be defined in derivated class.')  

    # TODO: Remove?
    # def setFitness(self, fitness):
    #     self.__optimised_fitness = fitness

    # TODO: Remove?
    # def setOriginalFitness(self, fitness):
    #     self.__fitness = fitness

    def getFitness(self):
        return self.__optimised_fitness
    
    def getBirthGeneration(self):
        return self.__numGenCreation

    def getOptimisedFitness(self):
        return self.__optimised_fitness
    
    def setOptimizedFitness(self, newFit):
        self.__optimised_fitness = newFit

    def isBetter(self, otherIndividual, population):
        raise PYGA_MethodMustBeOverloaded('ERROR: This function (Individual.isBetter) must be defined in derivated class.')

    def isDuplication(self, otherIndiv):
        return (self == otherIndiv)
 
    def distance(self, otherIndiv, population):
        return None

    @classmethod
    def individualSearchSpaceInfo(cls):
        return None, None # May be overloaded

    @classmethod
    def canBeCrossed(cls, parent1, parent2):
        return True # May be overloaded

    @classmethod
    def canBeMuted(cls, indiv):
        return True # May be overloaded

    @classmethod
    def crossover(cls, parent1, parent2):
        raise PYGA_MethodMustBeOverloaded('ERROR: This function (Individual.crossover) must be defined in derivated class.')

    @classmethod
    def mutation(cls, individual):
        raise PYGA_MethodMustBeOverloaded('ERROR: This function (Individual.mutation) must be defined in derivated class.')

