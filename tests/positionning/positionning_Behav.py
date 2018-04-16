# -*- mode: python; py-indent-offset: 4; tab-width: 4; coding: iso-8859-1 -*-

#######################################################################
# Author: Deau Raphaël
#
# Copyright 2011 - 2016
# License: Creative Commons Attribution Non-commercial 4.0
# Full text: https://creativecommons.org/licenses/by-nc/4.0/legalcode
#
#######################################################################

from PyGenAlg.standards.PYGA_StandardGenAlgBehavior import PYGA_StandardGenAlgBehavior


class PositionningBehavior(PYGA_StandardGenAlgBehavior):

    __PLOT_METHOD = None
    
    @classmethod
    def SET_PLOT_INFO(cls, plotIndiv):
        cls.__PLOT_METHOD = staticmethod(plotIndiv)
    
    def endOfGeneration(self, population, iGeneration, endOfRun, infoStr):
        sortedPop = population.getBestIndividual(4)
                
        self.__PLOT_METHOD(sortedPop[0], 1)
        self.__PLOT_METHOD(sortedPop[1], 2)
        self.__PLOT_METHOD(sortedPop[2], 3)
        self.__PLOT_METHOD(sortedPop[3], 4)
            

    def stopCriteria(self, population, iGeneration, startTime, infoStr):
        percent, stop = PYGA_StandardGenAlgBehavior.stopCriteria(self,
                                                                 population,
                                                                 iGeneration,
                                                                 startTime,
                                                                 infoStr)
        ownCriteria = population.getBestIndividual().getFitness() == 0.0
        return percent, stop or ownCriteria
        