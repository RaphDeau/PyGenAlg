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
# Start date: 29/11/2011
#
#-----------------------

# - build-in imports -
import random
import sys

# - local imports -
from PyGenAlg.standards.PYGA_StandardMultiObjIndividual_NSGAII import PYGA_StandardMultiObjIndividual_NSGAII


class PYGA_StandardVectorMultiObjIndividual_NSGAII(PYGA_StandardMultiObjIndividual_NSGAII):

    @classmethod
    def FLOATCMP(cls, a, b, epsilon=20):
        if (abs(a-b) < pow(10, -epsilon)):
            return 0
        elif a < b :
            return -1
        return 1

    # Define a default number of variable
    #  --> May be overloaded in subclass
    NB_VARIABLES = 2
    # Define a default value for each variables
    #  --> May be overloaded in subclass
    DEFAULT_VARIABLES_VALUE = []
    # Define a default range for each variables
    #  --> May be overloaded in subclass
    VARIABLES_RANGES = []
    # Define a default type for the variables
    #  --> May be overloaded in subclass
    VARIABLES_TYPE = float
    VARIABLES_COMPARE = FLOATCMP

    RANDOM_METHOD = random.expovariate
    RANDMETHOD_ARGS = {'lambd':1}
    RANDOM_IS_ONLY_POSITIVE = True

    # ==================
    # v Public methods v
    # ==================

    # ----------------------
    # Public - Constructor
    def __init__(self, values=None):
        PYGA_StandardMultiObjIndividual_NSGAII.__init__(self)
        if len(self.__class__.DEFAULT_VARIABLES_VALUE) != self.__class__.NB_VARIABLES:
            self.__class__.DEFAULT_VARIABLES_VALUE = [None]
            for i in xrange(self.__class__.NB_VARIABLES-1):
                self.__class__.DEFAULT_VARIABLES_VALUE.append(None)
        if len(self.__class__.VARIABLES_RANGES) != self.__class__.NB_VARIABLES:
            self.__class__.VARIABLES_RANGES = [None]
            for i in xrange(self.__class__.NB_VARIABLES-1):
                self.__class__.VARIABLES_RANGES.append(None)
        # 1- Define the variables
        if values is None:
            self.__variables = []
            for i in xrange(self.NB_VARIABLES):
                if self.__class__.DEFAULT_VARIABLES_VALUE[i] is not None:
                    self.__variables.append(self.__class__.DEFAULT_VARIABLES_VALUE[i])
                else:
                    self.__variables.append(self.__generateRandomVarValue(i))
        else:
            self.__variables = list(values)
    # Public - End of Constructor
    # ----------------------

    # ==================
    # ^ Public methods ^
    # ==================

    # ======================
    # v Overloaded methods v
    # ======================

    def getVariables(self):
        return self.__variables

    # ----------------------
    # Public - Random generation
    @classmethod
    def generate(cls):
        # 1- Create the new individual
        newInd = cls()
        # 2- Generate each variable
        for i in xrange(newInd.NB_VARIABLES):
            newInd.__variables[i] = newInd.__generateRandomVarValue(i)
        # 3- Return the generated individual...
        return newInd
    # Public - End of Random generation
    # ----------------------

    def isDuplication(self, otherIndiv):
        isDupl = True
        for i, x in enumerate(self.__variables):
            if self.__class__.VARIABLES_COMPARE(x, otherIndiv.__variables[i]) != 0:
                isDupl = False
                break
        return isDupl

    # ----------------------
    # Public - Reproduction methods
    @classmethod
    def crossover(cls, parent1, parent2):
        return cls.__simple_crossover(parent1, parent2)

    @classmethod
    def mutation(cls, individual):
        return cls.__simple_mutation(individual)
    # ----------------------

    def objectives(self, population):
        # Compute the objectives
        self.setObj(self.computeObj(self.__variables))
        
    # ======================
    # ^ Overloaded methods ^
    # ======================

    # ====================
    # v Specific methods v
    # ====================

    # ----------------------
    # Private - Random variable value generation
    @classmethod
    def __generateRandomVarValue(cls, iVar):
        # 1- Get the definition domain of the variable
        defDomain = cls.VARIABLES_RANGES[iVar]
        if defDomain is None:
            defDomain = '[' + str(-sys.maxint-1) + ',' + str(sys.maxint) + ']'
#        print '-----'
#        print defDomain
        # 2- Check the open/closed bounds
        includeFirst = defDomain[0] == '['
        includeLast = defDomain[-1] == ']'
        # 3- Get a random number in the domain
        defDomain = eval('[' + defDomain[1:-1] + ']')
#        print defDomain
        randFloat = cls.RANDOM_METHOD(**cls.RANDMETHOD_ARGS)
        if not cls.RANDOM_IS_ONLY_POSITIVE:
            if random.random() < 0.5:
                randFloat = -randFloat
#        print randFloat
        # 4- Check the bounds
        while (randFloat == defDomain[0] and not includeFirst) or\
              (randFloat == defDomain[1] and not includeLast) or \
              (randFloat < defDomain[0]) or (randFloat > defDomain[1]):
            randFloat = cls.RANDOM_METHOD(**cls.RANDMETHOD_ARGS)
#        print '-----'
        # 5- Cast the variable type
        return cls.VARIABLES_TYPE(randFloat)
    # ----------------------

    # ----------------------
    # Private - Standard crossover
    @classmethod
    def __simple_crossover(cls, parent1, parent2):
        newInd = cls()
        if newInd.NB_VARIABLES > 1:
            nbVar = newInd.NB_VARIABLES
            # 1 - Choose randomly a number of param to keep from parent1 
            nbVarFromP1 = 1 + int(random.random()*(nbVar - 2))
            # 2 - Choose randomly nbVarFromP1 param from parent1
            choosed = []
            while len(choosed) < nbVarFromP1:
                iVar = int(random.random()*nbVar)
                while iVar in choosed:
                    iVar = int(random.random()*nbVar)
                choosed.append(iVar)
                newInd.__variables[iVar] = parent1.__variables[iVar]
            # 3 - Take other params from parent2
            for iVar in xrange(nbVar):
                if iVar not in choosed:
                    newInd.__variables[iVar] = parent2.__variables[iVar]
        else:
            newInd.__variables[0] = cls.VARIABLES_TYPE((parent1.__variables[0] + parent2.__variables[0]) / 2)
            
        return newInd
    # Private - End of Standard crossover
    # ----------------------

    # ----------------------
    # Private - Standard mutation
    @classmethod
    def __simple_mutation(cls, individual):
        newInd = cls()
        nbVar = newInd.NB_VARIABLES
        # 1 - Copy the individual to mutate
        for iVar in xrange(nbVar):
            newInd.__variables[iVar] = individual.__variables[iVar]
        # 2 - change randomly a param
        iVar = int(random.random()*nbVar)
        newInd.__variables[iVar] = cls.__generateRandomVarValue(iVar)
        return newInd
    # Private - End of Standard mutation
    # ----------------------

    # ====================
    # ^ Specific methods ^
    # ====================
