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

# - Build-in imports -
import time
import sys

# - Local imports -
from PyGenAlg.core.PYGA_Population import PYGA_Population
from PyGenAlg.core.PYGA_Individual import PYGA_Individual
from PyGenAlg.core.PYGA_GenAlgBehavior import PYGA_GenAlgBehavior
from PyGenAlg.core.PYGA_Exceptions import PYGA_CreationError
from PyGenAlg.standards.PYGA_StandardGenAlgBehavior import PYGA_StandardGenAlgBehavior


class PYGA_GenAlg:

    DEBUG_MODE = False
    # ==================
    # v Public methods v
    # ==================

    # --------------------
    # Public - Constructor
    def __init__(self, 
                 individualClass, 
                 genAlgBehaviorClass = PYGA_StandardGenAlgBehavior,
                 populationClass = PYGA_Population,
                 debugMode = False,
                 outputPrint = None):
        
        self.DEBUG_MODE = debugMode
        if outputPrint is None:
            outputPrint = sys.stdout
        self.__outputPrint = outputPrint
        
        # 1- Check given classes
        if not issubclass(individualClass, PYGA_Individual):
            raise PYGA_CreationError('ERROR: individual class must inherit from PYGA_Individual')
        if not issubclass(genAlgBehaviorClass, PYGA_GenAlgBehavior):
            raise PYGA_CreationError('ERROR: behavior class must inherit from PYGA_GenAlgBehavior')
        if not issubclass(populationClass, PYGA_Population):
            raise PYGA_CreationError('ERROR: population class must inherit from PYGA_Population')
        
        # 2- Store class information
        self.__genAlgBehavior = genAlgBehaviorClass(individualClass, populationClass, debugMode, outputPrint)
        self.__individualClass = individualClass
        self.__individualClass.CURRENT_GENERATION = 0
        self.__individualClass.SET_BEHAVIOR(self.__genAlgBehavior)
        
        # 3- Create the population
        self.__population = populationClass(individualClass, self.__genAlgBehavior, debugMode, outputPrint)
    # Public - End of Constructor
    # ---------------------------

        
    # ------------------
    # Public - Main loop
    def run(self):
        self.__outputPrint.write('***********************************************************************\n')
        self.__outputPrint.write('PPPPPP   Y     Y   GGGGG     EEEEEE  N     N     A     L         GGGGG \n')
        self.__outputPrint.write('P     P   Y   Y   G     G   E        NN    N    A A    L        G     G\n')
        self.__outputPrint.write('P     P    YYY    G         E        N N   N   A   A   L        G      \n')
        self.__outputPrint.write('PPPPPP      Y     G  GGGG   EEEEE    N  N  N  A     A  L        G  GGGG\n')
        self.__outputPrint.write('P          Y      G     G   E        N   N N  AAAAAAA  L        G     G\n')
        self.__outputPrint.write('P         Y       G     G   E        N    NN  A     A  L        G     G\n')
        self.__outputPrint.write('P        Y         GGGGG     EEEEEE  N     N  A     A  LLLLLLL   GGGGG \n')
        self.__outputPrint.write('***********************************************************************\n')
        self.__outputPrint.write('Running with parameters:\n')
        self.__outputPrint.write(self.__genAlgBehavior.getPrintInformation())

        self.__outputPrint.write('------------------------\n')
        self.__outputPrint.write('Start time: ' + str(time.asctime()) + '\n')
        infoStr = '\rInitialising...'
        self.__outputPrint.write(infoStr)
        self.__outputPrint.flush()
        # Get the start time
        self.__evolvStartTime = time.time()
        iGen = 0 # Current generation number
        # 1- Generate the initial population
        self.__initPopulation(infoStr)
        # 2- Try an evaluation: maybe inital population already have best solution...
        # Or not...
        # __evaluation() return False if end criteria is reached
        infoStr = '\rFirst evaluation...'
        self.__outputPrint.write(infoStr) 
        self.__outputPrint.flush()
        percent, continu = self.__evaluation(iGen, infoStr)
        infoStr += ' Done' + ' '*50 + '\n'
        self.__outputPrint.write(infoStr) 
        self.__outputPrint.flush()
        while continu:
            infoStr = '\rEvolving... ' + str(percent) + '% (Generation #' + str(iGen) + ')'
            self.__outputPrint.write(infoStr + ' '*10)
            self.__outputPrint.flush()
            self.__startOfGeneration(iGen, infoStr)
            # Self optimizing (second order evolution)
            self.__selfOptimize(iGen, infoStr)
            # 2.1- Apply optimisation method (scaling, sharing, ...)
            if self.DEBUG_MODE:
                self.__outputPrint.write("PYGA_GenAlg / run - Optimizing\n")
                self.__outputPrint.flush()
            self.__optimise(infoStr)
            # 2.2- Apply selection method
            if self.DEBUG_MODE:
                self.__outputPrint.write("PYGA_GenAlg / run - Selecting\n")
                self.__outputPrint.flush()
            selectedPopulation = self.__selection(infoStr)
            # 2.3- Applie reproduction method
            if self.DEBUG_MODE:
                self.__outputPrint.write("PYGA_GenAlg / run - Reproducing\n")
                self.__outputPrint.flush()
            reproducedPopulation = self.__reproduction(self.__population, 
                                                       selectedPopulation,
                                                       infoStr)
            # 2.4- Set the new population
            if self.DEBUG_MODE:
                self.__outputPrint.write("PYGA_GenAlg / run - Setting new population\n")
                self.__outputPrint.flush()
            self.__setNewPopulation(reproducedPopulation + selectedPopulation, infoStr)
            # 2.5- Manage generations number
            iGen += 1
            if self.DEBUG_MODE:
                self.__outputPrint.write("PYGA_GenAlg / run - Evaluating\n")
                self.__outputPrint.flush()
            percent, continu = self.__evaluation(iGen, infoStr)
            self.__endOfGeneration(iGen, not continu, infoStr)
        infoStr = '\rEvolving... 100% (Generation #' + str(iGen) + ')                                                                     \n'
        self.__outputPrint.write(infoStr)
        self.__outputPrint.flush()
        # Compute the time of evolving
        evolvEndTime = time.time()
        evolvTime = evolvEndTime - self.__evolvStartTime
        # Get a human readable time
        evolvHour = int(evolvTime / 3600)
        evolvMin = int((evolvTime / 60) % 60)
        evolvSec = int(evolvTime % 60)
        strEvolvHour = str(evolvHour)
        strEvolvMin = str(evolvMin)
        if evolvMin < 10:
            strEvolvMin = '0' + strEvolvMin
        strEvolvSec = str(evolvSec)
        if evolvSec < 10:
            strEvolvSec = '0' + strEvolvSec
        strEvolvTime = strEvolvHour + ':' + strEvolvMin + ':' + strEvolvSec
        self.__outputPrint.write('Evolution time: ' + strEvolvTime + ' (' + str(evolvTime) + ' seconds).\n')
        self.__outputPrint.write('***********************************************************************\n')
    # Public - End of Main loop
    # -------------------------

    # --------------------------------------------------
    # Public - Get the best individual of the population
    def getBestIndividual(self):
        return self.__population.getBestIndividual()
    # --------------------------------------------------
        
    # ------------------------------
    # Public - Get the population...
    def getPopulation(self):
        return self.__population
    # ------------------------------

    def setPopSize(self, popSize):
        self.__genAlgBehavior.setPopSize(popSize)

    def setNbGen(self, nbGen):
        self.__genAlgBehavior.setNbGen(nbGen)

    def setParameters(self, **kwargs):
        self.__genAlgBehavior.setParameters(**kwargs)

    def getParameters(self):
        return self.__genAlgBehavior.getParameters()

    def savePopulation(self, fileName):
        self.__population.savePopulation(fileName)

    # ==================
    # ^ Public methods ^
    # ==================

    # ===================
    # v Private methods v
    # ===================
        
    # --------------------------------
    # Private - Check end of evolution
    def __evaluation(self, iGeneration, infoStr):
        if self.DEBUG_MODE:
            self.__outputPrint.write("PYGA_GenAlg / __evaluation - launch Population.computObjectives\n")
            self.__outputPrint.flush()
        # 1- Compute all objectives
        self.__population.computeObjectives(infoStr)

        if self.DEBUG_MODE:
            self.__outputPrint.write("PYGA_GenAlg / __evaluation - launch Behavior.generationStop\n")
            self.__outputPrint.flush()
        # 2- Check the end criteria of the used behavior
        percent, stopGen = self.__genAlgBehavior.generationStop(iGeneration, 
                                                                self.__population,
                                                                self.__evolvStartTime,
                                                                infoStr)
        
        if self.DEBUG_MODE:
            self.__outputPrint.write("PYGA_GenAlg / __evaluation - launch Behavior.stopCriteria\n")
            self.__outputPrint.flush()
        # 3- Check specific end criteria
        #########
        # TODO: Give all population of each generation as argument?
        stopCriteria = self.__genAlgBehavior.stopCriteria(self.__population, 
                                                          iGeneration,
                                                          infoStr)
        # TODO
        #########
        if self.DEBUG_MODE:
            self.__outputPrint.write("PYGA_GenAlg / __evaluation - returning " + str(percent) + ", " + str(not stopGen and not stopCriteria) + '\n')
            self.__outputPrint.flush()
        return percent, not stopGen and not stopCriteria
    # Private - End of check end of evolution
    # ---------------------------------------

    # -------------------------
    # Private - Init population
    def __initPopulation(self, infoStr):
        self.__genAlgBehavior.initPopulation(self.__population, infoStr)
    # -------------------------

    # --------------------------
    # Private - Start generation
    def __startOfGeneration(self, iGeneration, infoStr):
        self.__individualClass.CURRENT_GENERATION = iGeneration+1
        self.__genAlgBehavior.startOfGeneration(self.__population, 
                                                iGeneration, 
                                                infoStr)
    # --------------------------

    # ---------------------------
    # Private - End of generation
    def __endOfGeneration(self, iGeneration, endOfRun, infoStr):
        self.__genAlgBehavior.endOfGeneration(self.__population, 
                                              iGeneration, 
                                              endOfRun,
                                              infoStr)
    # ---------------------------

    def __selfOptimize(self, iGen, infoStr):
        self.__genAlgBehavior.selfOptimize(self.__population, iGen, infoStr)
    
    # -----------------
    # Private - scaling
    def __optimise(self, infoStr):
        self.__genAlgBehavior.optimise(self.__population, infoStr)
    # -----------------

    # -------------------
    # Private - selection
    def __selection(self, infoStr):
        return self.__genAlgBehavior.selection(self.__population, infoStr)
    # -------------------

    # ----------------------
    # Private - Reproduction
    def __reproduction(self, population, selectedPopulation, infoStr):
        if self.DEBUG_MODE:
            self.__outputPrint.write('PYGA_GenAlg / __reproduction - ' + str(self.__genAlgBehavior.__class__) +'\n')
            self.__outputPrint.flush()
        reproductedPopulation = self.__genAlgBehavior.reproduction(population, 
                                                                   selectedPopulation, 
                                                                   infoStr)
        return reproductedPopulation
    # ----------------------

    # ----------------------------
    # Private - Set the population
    def __setNewPopulation(self, population, infoStr):
        del self.__population
        self.__population = population
    # ----------------------------

    # ===================
    # ^ Private methods ^
    # ===================
        
