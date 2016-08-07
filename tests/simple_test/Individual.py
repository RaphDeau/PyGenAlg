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
#import PYGA
from PyGenAlg.core.PYGA_Individual import PYGA_Individual

# Function to maximize
def f(x):
    return (x[0] + x[1] - 1.0)**2


class Individual(PYGA_Individual):

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
    # Public - save Individual
    def saveIndividual(self, fid):
        fid.write(str(self.__value[0]))
        fid.write(';')
        fid.write(str(self.__value[1]) + '\n')
    # ----------------------

    # ----------------------
    # Public - load Individual
    @classmethod
    def loadIndividual(cls, fid):
        values = fid.readline()
        newInd = cls()
        newInd.__value[0] = float(values.split(';')[0])
        newInd.__value[1] = float(values.split(';')[1])
        return newInd
    # ----------------------

    # ----------------------
    # Public - Fitness
    def fitness(self, population):
        a = 0
        for i in xrange(100):
            a += 1
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
        # 1- Get the parents as a list (usefull to simplify code...)
        parents = [parent1, parent2]
        baseParent = 0
        baseIndex = 0
        # 2- Get each part of each parent to use
        # -- Proceed to a "best" selection...
        # -- Right now : parent1[0] is considered has the best (index 0 - 0)
        if parent1[0] < parent1[1]:
            # 2.1- parent1[1] is better -> 0 - 1
            baseIndex = 1
        if parent2[0] > parent1[baseIndex] and parent2[0] > parent2[1]:
            # 2.2- parent2[0] is better -> 1 - 0
            baseParent = 1
            baseIndex = 0
        elif parent2[1] > parent1[baseIndex]:
            # 2.3- parent2[1] is better -> 1 - 1
            baseParent = 1
            baseIndex = 1
        # 3- Set the value of the new individual
        newInd1 = cls()
        newInd1.__value[baseIndex] = parents[baseParent][baseIndex]
        newInd1.__value[1-baseIndex] = parents[1-baseParent][1-baseIndex]
        # Optional : crossover return multiple individuals
        newInd2 = cls()
        newInd2.__value[baseIndex] = parents[baseParent][1-baseIndex]
        newInd2.__value[1-baseIndex] = parents[1-baseParent][baseIndex]
        return [newInd1, newInd2]
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
        return str(self.getBirthGeneration()) + ' - ' + str(self.getValue()) + ' / ' + str(self.getFitness())
    # ----------------------

    # ===========================
    # ^ Operators overloading ^
    # ===========================
