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

# - local imports -
from PyGenAlg.standards.PYGA_StandardMultiObjIndividual import PYGA_StandardMultiObjIndividual


class PYGA_StandardMultiObjIndividual_NSGAII(PYGA_StandardMultiObjIndividual):

    # ==================
    # v Public methods v
    # ==================

    # ----------------------
    # Public - Constructor
    def __init__(self):
        # 1- Init father class
        PYGA_StandardMultiObjIndividual.__init__(self)
        
        # 2- Define Pareto front index and crowding distance
        self.__iParetoFront = None
        self.__ParetoFront = []
        self.__crowdingDist = None
    # Public - End of Constructor
    # ----------------------

    # ==================
    # ^ Public methods ^
    # ==================

    # ======================
    # v Overloaded methods v
    # ======================

    # ----------------------
    # Public - Compute fitness for multiple objectives individuals
    @classmethod
    def computeMultiObjFitness(cls, population):
        # Call corresponding fitness function
        cls.NSGAII_fitness(population)
    # ----------------------

    # ----------------------
    # Public - Individual comparison
    def isBetter(self, otherIndividual, population):
        # 1- Check Pareto fronts of both individuals
        if self.__iParetoFront < otherIndividual.__iParetoFront:
            return True
        if self.__iParetoFront > otherIndividual.__iParetoFront:
            return False

        # 2- Check crowding distance
        if None in [self.__crowdingDist, otherIndividual.__crowdingDist] and\
           len(self.__ParetoFront) > 1:
            # Need to compute crowding distance
            self.__computeNSGAIICrowdingDist(self.__ParetoFront)
        return self.__crowdingDist < otherIndividual.__crowdingDist
    # ----------------------

    @classmethod
    def getBestIndividuals(cls, population):
        paretoFront = []
        for indiv in population:
            if indiv.__iParetoFront == 0:
                paretoFront.append(indiv)
        return paretoFront

    # ======================
    # ^ Overloaded methods ^
    # ======================

    # ===========================
    # v Standard NSGAII methods v
    # ===========================

    @classmethod
    def NSGAII_fitness(cls, population):
        # 1- Init the "ruled" population 
        # -- "ruled" means "from which a Pareto front will be extract"
        ruled = list(population)
        # 2- Keep a list of all extracted fronts
        fronts = []
        iFront = 0
        # 3- Treat all individuals
        while len(ruled) != 0:
            # 3.1- Extract the front of the current "ruled" population
            fronts.append([])
            fronts[iFront], ruled = cls.__computeNSGAIIParetoFront(ruled)
            # 3.2- Set the individuals attributs
            for indiv in fronts[iFront]:
                indiv.__ParetoFront = fronts[iFront]
                indiv.__iParetoFront = iFront
            # 3.3- Compute next front on current "ruled" population
            iFront += 1

    @classmethod
    def __computeNSGAIIParetoFront(cls, population):
        # 1- Init ruled and front population
        ruled = []
        front = list(population)
        # 2- Check each individual of the population...
        for indiv1 in population:
            # 2.1- ... with each other (contained in "front")
            i = 0
            while i < len(front):
                indiv2 = front[i]
                # 2.1.1- Check if indiv1 dominates indiv2
                if indiv1.dominate(indiv2):
                    # 2.1.1.1- Add it to "ruled" and remove it from "front"
                    # -------- indiv2 won't be compared with other individuals
                    # -------- because it is already dominated...
                    ruled.append(front.pop(i))
                else:
                    # 2.1.1.2- Go to next individual
                    # -------- As "pop" remove the individual, no need to
                    # -------- increment "i" when "pop" is used.
                    i += 1
        return front, ruled

    @classmethod
    def __computeNSGAIICrowdingDist(cls, population):
        # 1- Get the of the studied population
        l = len(population)
        # 2- Init the distances to 0.0
        for indiv in population:
            indiv.__crowdingDist = 0.0
        # 3- Go through each objective
        for obj in xrange(cls.NB_OBJECTIVES):
            # 3.1- Sort the population by the current objective
            sortedPop = cls.sortPop(population, obj)
            # 3.2- Set first and last distance
            sortedPop[0].__crowdingDist = float('inf')
            sortedPop[l-1].__crowdingDist = float('-inf')
            # 3.3- Compute the difference (of objective) between first and last
            fmaxDiff = sortedPop[l-1].getObj()[obj] - sortedPop[0].getObj()[obj]
            # 3.4- Compute distance for each other (than first and last) individual
            if fmaxDiff != 0.0:
                i = 1
                while i < l-1:
                    # 3.4.1- Compute objective difference between previous and next
                    fdiff = sortedPop[i+1].getObj()[obj] - sortedPop[i-1].getObj()[obj]
                    # 3.4.2- Get crowding distance
                    sortedPop[i].__crowdingDist += fdiff / fmaxDiff
                    # 3.4.3- Treat next individual...
                    i += 1

    # ===========================
    # ^ Standard NSGAII methods ^
    # ===========================
