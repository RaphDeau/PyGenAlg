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
from PyGenAlg.core.PYGA_Individual import PYGA_Individual


class PYGA_StandardMultiObjIndividual(PYGA_Individual):

    # Tell the population that we are in multiple objectives
    MULTI_OBJ = True

    NEEDED_VAR = ['NB_OBJECTIVES', "OBJ_TYPES"]

    # ==================
    # v Public methods v
    # ==================

    # ----------------------
    # Public - Constructor
    def __init__(self):
        PYGA_Individual.__init__(self)
        # 1- Check class needed variable
        for var in self.NEEDED_VAR:
            try:
                eval("self." + var)
            except:
                raise Exception("ERROR: MultiObjectives Individual class must define " + var)

        # 2- Define the objectives
        self.__objectives = None

    # Public - End of Constructor
    # ----------------------

    def getObj(self):
        return self.__objectives
    def setObj(self, obj):
        self.__objectives = obj

    def needCompute(self):
        return self.__objectives is None

    @classmethod
    def getBestIndividuals(cls, population):
        print 'ERROR: This function (StandardMultiObjIndividual.getBestIndividuals) must be defined in derivated class.'

    # ==================
    # ^ Public methods ^
    # ==================

    # ====================
    # v Specific methods v
    # ====================


    # ----------------------
    # Public - Sort the population according to an objective
    @classmethod
    def sortPop(cls, population, obj):
        return sorted(population, key = lambda indiv: indiv.__objectives[obj])
    # ----------------------

    # ----------------------
    # Public - Individual domination
    def dominate(self, indiv):
        better = True
        equal = True
        # Check each objective for the given individuals
        for iObj in xrange(self.NB_OBJECTIVES):
            if self.__objectives[iObj] != indiv.__objectives[iObj]:
                equal = False
            if self.OBJ_TYPES[iObj] == "max":
                if self.__objectives[iObj] < indiv.__objectives[iObj]:
                    better = False
            else:
                if self.__objectives[iObj] > indiv.__objectives[iObj]:
                    better = False
        return better and not equal
    # ----------------------


    # ====================
    # ^ Specific methods ^
    # ====================
