# -*- mode: python; py-indent-offset: 4; tab-width: 4; coding: iso-8859-1 -*-

#######################################################################
# Author: Deau Raphaël
#
# Copyright 2011 - 2016
# License: Creative Commons Attribution Non-commercial 4.0
# Full text: https://creativecommons.org/licenses/by-nc/4.0/legalcode
#
#######################################################################

# - build-in imports -
import random

# - local imports -
from PyGenAlg.core.PYGA_Individual import PYGA_Individual
from PyGenAlg.standards.PYGA_StandardGenAlgBehavior import PYGA_StandardGenAlgBehavior

class SphereIndiv(PYGA_Individual):
    
    __DIM = 30
    __BOUNDS = [-5.12, 5.12]
    
    def __init__(self):
        PYGA_Individual.__init__(self)
        self.__x = None
        self.__fitness = None
    
    @classmethod
    def generate(cls):
        newInd = cls()
        newInd.__x = []
        for _ in xrange(cls.__DIM):
            newInd.__x.append(random.uniform(cls.__BOUNDS[0], cls.__BOUNDS[1]))
        return newInd
    
    def getFitness(self):
        return self.__fitness
    
    def fitness(self, population):
        self.__fitness = 0.0
        for x in self.__x:
            self.__fitness += x*x
        return self.__fitness
    
    def duplicate(self):
        newInd = self.__class__()
        newInd.__x = list(self.__x)
        newInd.__fitness = self.__fitness
        return newInd
    
    def isDuplication(self, otherInd):
        dupl = True
        i = 0
        while dupl and i < len(self.__x):
            if self.__x[i] != otherInd.__x[i]:
                dupl = False
            i += 1
        return dupl
    
    def isBetter(self, otherIndiv, population):
        return self.__fitness < otherIndiv.__fitness
    
    @classmethod
    def crossover(cls, parent1, parent2):
        newInd = cls()
        newInd.__x = []
        for i in xrange(len(parent1.__x)):
            if abs(parent1.__x[i]) > abs(parent2.__x[i]):
                newInd.__x.append(parent2.__x[i])
            else:
                newInd.__x.append(parent1.__x[i])
        return newInd
    
    @classmethod
    def mutation(cls, indiv):
        newInd = indiv.duplicate()
        nbMute = int(random.random()*(len(newInd.__x)-1))+1
        toMute = []
        for i, x in enumerate(indiv.__x):
            if len(toMute) < nbMute:
                toMute.append(i)
            else:
                iMin = 0
                for im, i2 in enumerate(toMute):
                    if abs(indiv.__x[i2]) < abs(indiv.__x[toMute[iMin]]):
                        iMin = im
                if abs(x) > abs(indiv.__x[toMute[iMin]]):
                    toMute[iMin] = i
        for i in toMute:
            newInd.__x[i] = random.uniform(cls.__BOUNDS[0], cls.__BOUNDS[1])
        return newInd
    
    def __str__(self):
        return str(self.__fitness) + " - " + str(self.__x) 
        
        
class SphereBehav(PYGA_StandardGenAlgBehavior):
    def biasCrossoverSelection(self, individuals, nbToSelect):
        return self.__rouletteSelection(individuals, nbToSelect)
    
    def getMaxFit(self, individuals):
        fitMax = None
        for indiv in individuals:
            if fitMax is None or fitMax < indiv.getFitness():
                fitMax = indiv.getFitness()
        return fitMax
    
    def __computeProba(self, individuals):
        # 1.1- Check the fitness function monotonic
        indiv1 = individuals[int(random.random() * len(individuals))]
        fit1 = indiv1.getFitness()
        indiv2 = None
        fit2 = fit1
        # Get 2 individuals with different fitness to compare them
#         for indiv in individuals:
#             self._outputPrint.write(str(indiv) + "\n")
        while fit2 == fit1:
            indiv2 = individuals[int(random.random() * len(individuals))]
            fit2 = indiv2.getFitness()
        fitFunc = 1
        # "isBetter" is given by the Individual creator 
        # so it will give us the order of the individuals
        if indiv1.isBetter(indiv2, individuals):
            if fit1 < fit2:
                fitFunc = -1
        else:
            if fit1 > fit2:
                fitFunc = -1
        maxFit = self.getMaxFit(individuals)
        fitSum = 0.0
        for indiv in individuals:
            indivFit = indiv.getFitness()
            # 1.2.1- Consider the fitness function monotony
            # If fitness function is decreasing, the proba to be selected must
            # be inverted (take "(maxFit - fit) / sum" instead of "fit / sum")
            if fitFunc == -1:
                indivFit = maxFit - indivFit
            fitSum += indivFit
        proba = []
        prevProba = 0.0
        for ip, indiv in enumerate(individuals):
            indivFit = indiv.getFitness()
            # 1.3.1- Consider the fitness function monotony
            if fitFunc == -1:
                indivFit = maxFit - indivFit
            # 1.3.2- Get the proba of the individual to be choosen 
            # (between 0.0 and 1.0)
            nextProba = prevProba + indivFit / fitSum
            # 1.3.3- Simulate the wheel with a range for each individual
            proba.append([prevProba, nextProba, ip])
            prevProba = nextProba
        return proba
    
    def __rouletteSelection(self, individuals, nbIndSelected):
        # 1- Create the new population
        # -- It will contain only the selected individuals
        currentIndivs = []
        for indiv in individuals:
            currentIndivs.append(indiv.duplicate())
        selectedPop = []
        if nbIndSelected > 0:
            proba = self.__computeProba(currentIndivs)
            # 1.4- Fill the new population
            while len(selectedPop) < nbIndSelected:
                # 1.4.1- Pick a random number between 0.0 and 1.0
                pickedProba = random.random()
                # 1.4.2- Find the corresponding proba in the wheel
                selectedProba = None
                for prob in proba:
                    if pickedProba >= prob[0] and pickedProba < prob[1]:
                        selectedProba = prob
                # 1.4.3- Manage a selected individual
                if selectedProba is not None:
                    # 1.4.3.1- Add the chosen on the new population 
                    selectedPop.append(currentIndivs.pop(selectedProba[2]))
                    # 1.4.3.2- Remove it from the eligible list
                    proba = self.__computeProba(currentIndivs)
        return selectedPop
    
        