# -*- mode: python; py-indent-offset: 4; tab-width: 4; coding: iso-8859-1 -*-

#######################################################################
# Author: Deau Raphaël
#
# Copyright 2011 - 2016
# License: Creative Commons Attribution Non-commercial 4.0
# Full text: https://creativecommons.org/licenses/by-nc/4.0/legalcode
#
#######################################################################

from PyGenAlg.standards.PYGA_StandardMultiObjIndividual_NSGAII import PYGA_StandardMultiObjIndividual_NSGAII

import random
import sys


class Individual(PYGA_StandardMultiObjIndividual_NSGAII):

    NB_VARIABLES = 1
    VARIABLES_DEFAULT_VALUES = [None]
    VARIABLES_RANGES = ['[-10, 10]']
    VARIABLES_TYPE = float

    NB_OBJECTIVES = 2
    OBJ_TYPES = ["min", "max"]

    def f(self, x):
        return [x*x, (x-2)*(x-2)]

    def __init__(self, values=None):
        # 1- Define the variables
        if values is None:
            self.__variables = []
            for i in xrange(self.NB_VARIABLES):
                if self.VARIABLES_DEFAULT_VALUES[i] is None:
                    self.__variables.append(self.__generateRandomVarValue(i))
                else:
                    self.__variables.append(self.VARIABLES_DEFAULT_VALUES[i])
        else:
            self.__variables = list(values)

        PYGA_StandardMultiObjIndividual_NSGAII.__init__(self)

    @classmethod
    def generate(cls):
        # 1- Create the new individual
        newInd = cls()
        # 2- Generate each variable
        for i in xrange(newInd.NB_VARIABLES):
            newInd.__variables[i] = newInd.__generateRandomVarValue(i)
        # 3- Return the generated individual...
        return newInd


    def __str__(self):
        return str(self.getObj()).replace('[', '').replace(']', '')

    def objectives(self, population):
        self.setObj(self.f(self.__variables[0]))

    @classmethod
    def computeMultiObjFitness(cls, population):
        # 1- Compute the objectives for each individual
        for indiv in population:
            if None in indiv.getObj():
                indiv.setObj(indiv.computeObj())
        

    # ----------------------
    # Private - Standard crossover
    @classmethod
    def crossover(cls, parent1, parent2):
        newInd = cls()
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
        return newInd
    # Private - End of Standard crossover
    # ----------------------

    # ----------------------
    # Private - Standard mutation
    @classmethod
    def mutation(cls, individual):
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

    # ----------------------
    # Private - Random variable value generation
    @classmethod
    def __generateRandomVarValue(cls, iVar):
        # 1- Get the definition domain of the variable
        defDomain = cls.VARIABLES_RANGES[iVar]
        if defDomain is None:
            randFloat = random.uniform(-sys.maxint-1, sys.maxint)
        else:
            # 2- Check the open/closed bounds
            includeFirst = defDomain[0] == '['
            includeLast = defDomain[-1] == ']'
            # 3- Get a random number in the domain
            defDomain = eval('[' + defDomain[1:-1] + ']')
            randFloat = random.random()*(defDomain[1]-defDomain[0]) + defDomain[0]
            # 4- Check the bounds
            while (randFloat == defDomain[0] and not includeFirst) or\
                    (randFloat == defDomain[1] and not includeLast):
                randFloat = random.random()*(defDomain[1]-defDomain[0]) + defDomain[0]
        # 5- Cast the variable type
        return cls.VARIABLES_TYPE(randFloat)
    # ----------------------
