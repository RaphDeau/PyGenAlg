# -*- coding: utf-8 -*-
"""
Python Genetic Algorithm module.

This file contains the base class of the behavior of the GA: PYGA_GenAlgBehavior.
It defines how the GA must act at each step of the GA cycle.

License full text: https://creativecommons.org/licenses/by-nc/4.0/legalcode


Modification History:
**** 18/07/2011 ****
Creation
**** 29/09/2016 ****
Global:
- PEP8 update
- Docstring
- Meta data
TODO: complete the list!

TODO List:
-
"""
# - Build-in imports -
from multiprocessing import Process
from sys import version_info

# - Local imports -
from PyGenAlg.core.PYGA_Exceptions import PYGA_MethodMustBeOverloaded

# Manage python versions compatibility
if version_info[0] >= 3:
    unicode = str

# Meta information
__author__ = "Raphaël Deau"
__copyright__ = "Copyright 2016, Raphaël Deau"
__license__ = "Creative Commons Attribution Non-commercial 4.0"
__version__ = "1.0.0"
__since__ = "18/07/2011"
__date__ = "29/09/2016"


class PYGA_Individual(object):
    """
    This class is the base for the GA individual coding.
    It allows defining:
        - TODO:

    A "standard behavior and parameters set" is provided in PYGA_StandardGenAlgBehavior.

    Attributes:
        - TODO:
    """

    MULTI_OBJ = False # TODO: set this in standardIndiv
    CURRENT_GENERATION = 0 # Keep the current generation to store birth generation
    __behav = None # Keep the behavior to be able to get the parameters

    @classmethod
    def SET_BEHAVIOR(cls, behaviorInstance):
        """
        /!\ MAY ONLY BE CALLED BY PYGA_GenAlg /!\

        Set the behavior to use.

        :param behaviorInstance: The behavior to use.
        :type behaviorInstance: Derived from PYGA_GenAlgBehavior
        """
        cls.__behav = behaviorInstance

    @classmethod
    def getParam(cls, paramKeyword):
        """
        Get the value of the asked parameter.

        :param paramKeyword: The keyword of the parameter to get.
        :type paramKeyword: String
        :return: The value of the parameter.
        :rtype: Depending on the parameter
        """
        paramLabel = cls.__behav.getParamFromKeyword(paramKeyword)
        if paramLabel is None:
            # TODO: Own exception
            raise Exception(u"Unknown parameter " + unicode(paramKeyword))
        return cls.__behav.getParam(paramLabel)

    def __init__(self):
        """Constructor of PYGA_Individual."""
        self.__fitness = None
        self.__optimised_fitness = None # TODO: review how it works?
        self.__numGenCreation = self.CURRENT_GENERATION

    @classmethod
    def generate(cls):
        # TODO: Set this in StandardIndiv? (See Population)
        """
        [ MUST BE OVERLOADED ]

        This class method must generate an individual.

        :return: The generated individual
        :rtype: Individual
        """
        raise PYGA_MethodMustBeOverloaded("Individual.generate")

    def saveIndividual(self, ostream):
        # TODO: Set this in StandardIndiv? (See Population)
        """
        [ MUST BE OVERLOADED ]

        Saves the individual to an open output stream

        :param ostream: The output stream within the individual must be saved.
        :type ostream: Opened output stream
        """
        raise PYGA_MethodMustBeOverloaded("Individual.saveIndividual")
        
    @classmethod
    def loadIndividual(cls, istream):
        # TODO: Set this in StandardIndiv? (See Population)
        """
        [ MUST BE OVERLOADED ]

        Load an individual from an opened input stream.

        :param istream: The input stream within the individual is loaded.
        :type istream: Opened input stream
        :return: The individual
        :rtype: Derived from PYGA_Individual
        """
        raise PYGA_MethodMustBeOverloaded("Individual.loadIndividual")

    @classmethod
    def parseIndividual(cls, indivStruct):
        # TODO: Set this in StandardIndiv? (See Population)
        """
        [ MUST BE OVERLOADED ]

        Parse an individual from a given python object.

        :param indivStruct: The object to read.
        :type indivStruct: Depending on the individual
        :return: The individual
        :rtype: Derived from PYGA_Individual
        """
        raise PYGA_MethodMustBeOverloaded("Individual.parseIndividual")

    def fitness(self, population):
        """
        [ MUST BE OVERLOADED ]

        Returns the computed fitness of the individual.

        :param population: The entire population (if needed).
        :type population: Derived from PYGA_Population
        :return: The fitness of the individual
        :rtype: Depending on the individual
        """
        raise PYGA_MethodMustBeOverloaded("Individual.fitness")

    def objectives(self, population):
        # TODO: Set this in StandardIndiv
        raise PYGA_MethodMustBeOverloaded("Individual.objectives")

    def needCompute(self):
        # TODO: Set this in StandardIndiv? (See Population)
        """Check if the individual needs computation of fitness."""
        return self.__fitness is None

    def __computeObjectives(self, population, pipe=None, indivID=None):
        # TODO: Set this in StandardIndiv? (See Population)
        """
        Launch the fitness computation.
        May be in separate thread.

        :param population: The entire population (if needed)
        :type population: Derived from PYGA_Population
        :param pipe: The associated pipe to return to the parent thread.
        :type pipe: Pipe
        :param indivID: The id of the individual (in the parent thread)
        :type indivID: int
        :return: The fitness
        :rtype: Depending on the individual
        """
        if self.MULTI_OBJ: # TODO: Set this in StandardIndiv
            obj = self.objectives(population)
        else:
            obj = self.fitness(population)
        if pipe is not None:
            # TODO: may not work, use shared object
            # TODO: Check if it works... Fitness is not set...
            pipe.send([self, indivID])
            pipe.close()
        return obj

    def computeObjectives(self, population, processList=None, pipe=None, indivID=None):
        # TODO: Set this in StandardIndiv? (See Population)
        """
        Launch the fitness computation.
        Manage parallel launch.

        :param population: The entire population (if needed)
        :type population: Derived from PYGA_Population
        :param processList: The parent thread process list to update
        :type processList: list
        :param pipe: The pipe to connect to the parent thread.
        :type pipe: Pipe
        :param indivID: The id of the individual in the parent thread.
        :type indivID: int
        :return: True if the fitness has been computed. False otherwise.
        :rtype: bool
        """
        needCompute = self.needCompute()
        if needCompute:
            if self.getParam("max_process") != 1:
                p = Process(target=self.__computeObjectives, args=(population, pipe, indivID))
                p.start()
                processList.append(p)
            else:
                # TODO: check why self.__fitness is set (and sometimes not)
                self.__fitness = self.__computeObjectives(population)
                # TODO: check how optimised fit works.
                self.__optimised_fitness = self.__fitness
        return needCompute

    @classmethod
    def computeMultiObjFitness(cls, population):
        # TODO: Set this in StandardIndiv?
        raise PYGA_MethodMustBeOverloaded("Individual.computeMultiObjFitness")

    def getFitness(self):
        """Returns the current fitness (optimised) of the individual"""
        return self.__optimised_fitness
    
    def getBirthGeneration(self):
        """Get the birth generation of the individual."""
        return self.__numGenCreation

    def setOptimizedFitness(self, newFit):
        # TODO: Check how optimize works...
        self.__optimised_fitness = newFit

    def isBetter(self, otherIndividual, population):
        # TODO: Set this in StandardIndiv? (See Population)
        """
        [ MUST BE OVERLOADED ]

        Check if the "self" individual is better than the given one.

        :param otherIndividual: The other individual to compare.
        :type otherIndividual: self.__class__
        :param population: The entire population (if needed)
        :type population: Derived from PYGA_Population
        :return: True if self is better than otherIndividual. False otherwise.
        :rtype: bool
        """
        raise PYGA_MethodMustBeOverloaded("Individual.isBetter")

    def isDuplication(self, otherIndiv):
        # TODO: Set this in StandardIndiv? (See Population)
        """
        [ MAY BE OVERLOADED ]

        Check if the given individual is the same as "self".

        :param otherIndiv: The other individual to compare.
        :type otherIndiv: self.__class__
        :return: True if they are the same.
        :rtype: bool
        """
        # Default check "==" (pointer, or method if overloaded)
        return self == otherIndiv
 
    def distance(self, otherIndiv, population):
        # TODO: Set this in StandardIndiv? (See Population)
        """
        [ MAY BE OVERLOADED ]

        Get the distance between two individuals.

        :param otherIndiv: The other individual to get the distance with.
        :type otherIndiv: self.__class__
        :param population: The entire population (if needed)
        :type population: Derived from PYGA_Population
        :return: The distance between the individuals.
        :rtype: float
        """
        return None

    @classmethod
    def individualSearchSpaceInfo(cls):
        # TODO: Set this in StandardIndiv?
        return None, None # May be overloaded

    @classmethod
    def canBeCrossed(cls, parent1, parent2):
        # TODO: Set this in StandardIndiv?
        return parent1 != parent2 # May be overloaded

    @classmethod
    def canBeMuted(cls, indiv):
        # TODO: Set this in StandardIndiv?
        return indiv is not None # May be overloaded

    @classmethod
    def crossover(cls, parent1, parent2):
        # TODO: Set this in StandardIndiv?
        raise PYGA_MethodMustBeOverloaded("Individual.crossover")

    @classmethod
    def mutation(cls, individual):
        # TODO: Set this in StandardIndiv?
        raise PYGA_MethodMustBeOverloaded("Individual.mutation")
