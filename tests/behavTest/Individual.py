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
# Start date: 21/07/2011
#
#-----------------------

# - build-in imports
import random

# - local imports -
from PyGenAlg.core.PYGA_Individual import PYGA_Individual

# Function to maximize
def f(x):
    return (x[0] + x[1] - 1.0)**2


class Individual(PYGA_Individual):

    SLEEP = False

    # ===========================
    # v Public methods v
    # ===========================

    # ----------------------
    # Public - Constructor
    def __init__(self):
        PYGA_Individual.__init__(self)
        self.__value = [0., 0.]
    # ----------------------
        
    # ----------------------
    # Public - Get value
    def getValue(self):
        return self.__value
    # ----------------------

    # ----------------------
    # Public - Set value
    def setValue(self, value):
        self.__value = value
    # ----------------------

    # ----------------------
    # Public - Duplicate
    def duplicate(self):
        newInd = self.__class__()
        newInd.__value[0] = self.__value[0]
        newInd.__value[1] = self.__value[1]
        return newInd
    # ----------------------

    # ===========================
    # ^ Public methods ^
    # ===========================



    # ===========================
    # v Overloaded methods v
    # ===========================

    # ----------------------
    # Public - Generate
    @classmethod
    def generate(cls):
        newIndiv = cls()
        newIndiv.setValue([random.random(), random.random()])
        return newIndiv
    # ----------------------

    # ----------------------
    # Public - Fitness
    def fitness(self, population):
        if self.SLEEP:
            import time
            time.sleep(0.05)
        return f(self.getValue())
    # ----------------------

    def distance(self, otherInd, population):
        return abs(self.getFitness() - otherInd.getFitness())

    # ----------------------
    # Public - Is better
    def isBetter(self, otherInd, population):
        return self.getFitness() < otherInd.getFitness()
    # ----------------------
    
    # ----------------------
    # Public - Crossover
    @classmethod
    def crossover(cls, parent1, parent2):
        # 1- Instanciate the new individual
        newInd = cls()
        # 2- Get the parents as a list (usefull to simplify code...)
        parents = [parent1, parent2]
        baseParent = 0
        baseIndex = 0
        # 3- Get each part of each parent to use
        # -- Proceed to a "best" selection...
        # -- Right now : parent1[0] is considered has the best (index 0 - 0)
        if parent1[0] < parent1[1]:
            # 3.1- parent1[1] is better -> 0 - 1
            baseIndex = 1
        if parent2[0] > parent1[baseIndex] and parent2[0] > parent2[1]:
            # 3.2- parent2[0] is better -> 1 - 0
            baseParent = 1
            baseIndex = 0
        elif parent2[1] > parent1[baseIndex]:
            # 3.3- parent2[1] is better -> 1 - 1
            baseParent = 1
            baseIndex = 1
        # 4- Set the value of the new individual
        newInd.__value[baseIndex] = parents[baseParent][baseIndex]
        newInd.__value[1-baseIndex] = parents[1-baseParent][1-baseIndex]
        return newInd
    # Public - End of Crossover
    # ----------------------

    # ----------------------
    # Public - Mutation
    @classmethod
    def mutation(cls, individual):
        # 1- Create the new individual
        newInd = individual.duplicate()
        # 2- Get a random part of the individual to mutate
        i = int(random.random() * 2)
        # 3- Set the new value (assert it won't be the same even randomly...)
        oldValue = newInd.__value[i]
        while newInd.__value[i] == oldValue:
            newInd.__value[i] = random.random()
        return newInd
    # Public - End of Mutation
    # ----------------------

    # ===========================
    # ^ Overloaded methods ^
    # ===========================



    # ===========================
    # v Operators overloading v
    # ===========================

    # ----------------------
    # Operator "[]"
    def __getitem__(self, index):
        return self.__value[index]
    # ----------------------

    # ----------------------
    # Operator "str"
    def __str__(self):
        return str(self.getValue()) + ' / ' + str(self.getFitness())
    # ----------------------

    # ===========================
    # ^ Operators overloading ^
    # ===========================
