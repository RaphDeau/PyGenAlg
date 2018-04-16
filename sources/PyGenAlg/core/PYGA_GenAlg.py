# -*- coding: utf-8 -*-
"""
Python Genetic Algorithm module.

This file contains the main class of the GA: PYGA_GenAlg.
This class allows creating, setting, and running the GA.


License full text: https://creativecommons.org/licenses/by-nc/4.0/legalcode



Modification History:
**** 18/07/2011 ****
Creation
**** 26/09/2016 ****
Global:
- PEP8 update
- Inline methods
- Docstring
- Meta data
Coding:
- __print definition
- __oneIteration definition

TODO List:
-
"""
# - Build-in imports -
from time import time, asctime
from sys import stdout, version_info

# - Local imports -
from PyGenAlg.core.PYGA_Population import PYGA_Population
from PyGenAlg.core.PYGA_Individual import PYGA_Individual
from PyGenAlg.core.PYGA_GenAlgBehavior import PYGA_GenAlgBehavior
from PyGenAlg.core.PYGA_Exceptions import PYGA_CreationError
from PyGenAlg.standards.PYGA_StandardGenAlgBehavior import PYGA_StandardGenAlgBehavior

# Manage python versions compatibility
if version_info[0] >= 3:
    unicode = str

# Meta information
__author__ = "Raphaël Deau"
__copyright__ = "Copyright 2016, Raphaël Deau"
__license__ = "Creative Commons Attribution Non-commercial 4.0"
__version__ = "1.0.0"
__since__ = "18/07/2011"
__date__ = "26/09/2016"


class PYGA_GenAlg:
    """
    The main class of the GA.

    Needing an individual class to be used. It allows running a
    GA on this kind of individual.

    Attributes:
        :ivar __debugMode: Defines if debug is activated.
        :type __debugMode: bool
        :ivar __outputPrint: The output stream to write log in.
        :type __outputPrint: Opened output stream
        :ivar __genAlgBehavior: The instance of the behavior of the GA.
        :type __genAlgBehavior: Derived from PYGA_GenAlgBehavior
        :ivar __individualClass: The individual class to use.
        :type __individualClass: type derived from PYGA_Individual
        :ivar __population: The population
        :type __population: subclass of PYGA_Population
        :ivar __evolveStartTime: The start time of the evolution
        :type __evolveStartTime: float
    """
    # ==================
    # v Public methods v
    # ==================

    # --------------------
    # Public - Constructor
    def __init__(self, 
                 individualClass, 
                 genAlgBehaviorClass=PYGA_StandardGenAlgBehavior,
                 populationClass=PYGA_Population,
                 debugMode=False,
                 outputPrint=None):
        """
        The constructor of PYGA_GenAlg.

        :param individualClass: The individual class to use
        :type individualClass: Python class, inherited from PYGA_Individual
        :param genAlgBehaviorClass: A class defining the behavior of the GA.
        :type genAlgBehaviorClass: Python class, inherited from PYGA_GenAlgBehavior
        :param populationClass: A class defining the structure of a population of the GA
        :type populationClass: Python class, inherited from PYGA_Population
        :param debugMode: Setting debug mode up or down.
        :type debugMode: Bool
        :param outputPrint: A stream within the logs will be written
        :type outputPrint: Opened output stream
        """
        
        self.__debugMode = debugMode
        if outputPrint is None:
            outputPrint = stdout
        self.__outputPrint = outputPrint
        
        # 1- Check given classes
        if not issubclass(individualClass, PYGA_Individual):
            raise PYGA_CreationError("ERROR: individual class must inherit from PYGA_Individual")
        if not issubclass(genAlgBehaviorClass, PYGA_GenAlgBehavior):
            raise PYGA_CreationError("ERROR: behavior class must inherit from PYGA_GenAlgBehavior")
        if not issubclass(populationClass, PYGA_Population):
            raise PYGA_CreationError("ERROR: population class must inherit from PYGA_Population")

        # 2- Store class information
        self.__genAlgBehavior = genAlgBehaviorClass(individualClass, populationClass, self.__print)
        self.__individualClass = individualClass
        # Initialise the individual high level data
        self.__individualClass.CURRENT_GENERATION = 0
        self.__individualClass.SET_BEHAVIOR(self.__genAlgBehavior)
        
        # 3- Create the population
        self.__population = populationClass(individualClass, self.__genAlgBehavior, self.__print)

        self.__evolveStartTime = None
    # Public - End of Constructor
    # ---------------------------

    # ------------------
    # Public - Main loop
    def run(self):
        """
        Main loop of the GA.

        Execute following GA's steps:
         1- Initialise the population
         2- Evaluate the initial population
         3- Optimise parameters (second order evolution)
         4- Compute optimised fitness (sharing, scaling ...)
         5- Select individuals
         6- Reproduction
         7- Set the new population according to siblings
         8- Evaluate the new population
         9- Check for stop criteria
            -> Go to "3-" if not stopped
        """
        self.__writeHeaders()
        # Get the start time
        self.__evolveStartTime = time()
        iGen = 0  # Current generation number
        # 1- Generate the initial population
        infoStr = "\rInitialising..."
        self.__genAlgBehavior.initPopulation(self.__population, infoStr)
        # 2- Try an evaluation: maybe initial population already have best solution...
        #    Or not...
        infoStr = "\rFirst evaluation..."
        self.__print(infoStr)
        percent, continueEvolution, nbEval = self.__evaluation(iGen, infoStr)
        self.__print(infoStr + " Done" + ' '*50 + '\n')
        # 3- Population is initialised, process to the evolution loop
        while continueEvolution:
            infoStr = "\rEvolving... " + unicode(percent) + "% (Generation #" + unicode(iGen) + ')'
            self.__print(infoStr + ' ' * 10)
            curNbEval, percent, continueEvolution = self.__oneIteration(iGen, infoStr)
            nbEval += curNbEval
            iGen += 1
        self.__print("\rEvolving... 100% (Generation #" + unicode(iGen) + ')' + ' ' * 70 + '\n')
        # 4- Compute the time of evolving
        evolveEndTime = time()
        evolveTime = evolveEndTime - self.__evolveStartTime
        # 5- Get a human readable time
        evolveHour = int(evolveTime / 3600)
        evolveMin = int((evolveTime / 60) % 60)
        evolveSec = int(evolveTime % 60)
        strEvolveHour = unicode(evolveHour)
        strEvolveMin = unicode(evolveMin)
        if evolveMin < 10:
            strEvolveMin = '0' + strEvolveMin
        strEvolveSec = unicode(evolveSec)
        if evolveSec < 10:
            strEvolveSec = '0' + strEvolveSec
        strEvolveTime = strEvolveHour + ':' + strEvolveMin + ':' + strEvolveSec
        # 6- Display final statistics
        self.__print("Total number of evaluation: " + unicode(nbEval) + '\n')
        self.__print("Evolution time: " + strEvolveTime + " (" + unicode(evolveTime) + " seconds).\n")
        self.__print("***********************************************************************\n")
    # Public - End of Main loop
    # -------------------------

    def getBestIndividual(self):
        """Returns the best individual of the current population."""
        return self.__population.getBestIndividual()

    def getPopulation(self):
        """Returns the current population."""
        return self.__population

    def setParameters(self, **kwargs):
        """Set the given parameters values (see Behavior for parameters list)."""
        self.__genAlgBehavior.setParameters(**kwargs)

    def getParameters(self):
        """Get all parameters values."""
        return self.__genAlgBehavior.getParameters()

    def savePopulation(self, fileName):
        """Save the current population to a given file."""
        self.__population.savePopulation(fileName)

    # ==================
    # ^ Public methods ^
    # ==================

    # ===================
    # v Private methods v
    # ===================

    def __print(self, s, debug=False):
        """
        Print s to the output stream given in constructor.

        :param s: The string to print
        :type s: str
        :param debug: Write text only in debug mode if True.
        :type debug: bool
        """
        if not debug or self.__debugMode:
            self.__outputPrint.write(s)
            self.__outputPrint.flush()

    def __writeHeaders(self):
        """Write the global information at launch."""
        self.__outputPrint.write("***********************************************************************\n")
        self.__outputPrint.write("PPPPPP   Y     Y   GGGGG     EEEEEE  N     N     A     L         GGGGG \n")
        self.__outputPrint.write("P     P   Y   Y   G     G   E        NN    N    A A    L        G     G\n")
        self.__outputPrint.write("P     P    YYY    G         E        N N   N   A   A   L        G      \n")
        self.__outputPrint.write("PPPPPP      Y     G  GGGG   EEEEE    N  N  N  A     A  L        G  GGGG\n")
        self.__outputPrint.write("P          Y      G     G   E        N   N N  AAAAAAA  L        G     G\n")
        self.__outputPrint.write("P         Y       G     G   E        N    NN  A     A  L        G     G\n")
        self.__outputPrint.write("P        Y         GGGGG     EEEEEE  N     N  A     A  LLLLLLL   GGGGG \n")
        self.__outputPrint.write("***********************************************************************\n")
        self.__outputPrint.write("Running with parameters:\n")
        self.__outputPrint.write(self.__genAlgBehavior.getPrintInformation())

        self.__outputPrint.write("------------------------\n")
        self.__outputPrint.write("Start time: " + unicode(asctime()) + '\n')
        self.__outputPrint.write("\rInitialising...")
        self.__outputPrint.flush()

    def __evaluation(self, iGeneration, infoStr):
        """
        Launch the evaluation of the current population.

        :param iGeneration: The if of the current generation.
        :type iGeneration: int
        :param infoStr: A string within logs are propagated.
        :type infoStr: str
        :return: The percent of GA progress (if known),\
                 the stop flag (True to continue),\
                 the number of evaluated individuals
        :rtype: int, bool, int
        """
        self.__print("PYGA_GenAlg / __evaluation - launch Population.computObjectives\n", debug=True)
        # 1- Compute all objectives
        nbEval = self.__population.computeObjectives(infoStr)

        self.__print("PYGA_GenAlg / __evaluation - launch Behavior.stopCriteria\n", debug=True)
        # 2- Check stop criteria
        #########
        # TODO: Give all population of each generation as argument?
        percent, stopCriteria = self.__genAlgBehavior.stopCriteria(self.__population,
                                                                   iGeneration,
                                                                   self.__evolveStartTime,
                                                                   infoStr)
        #########
        debugMsg = "PYGA_GenAlg / __evaluation - returning " + unicode(percent) + ", "
        debugMsg += unicode(not stopCriteria) + '\n'
        self.__print(debugMsg, debug=True)
        return percent, not stopCriteria, nbEval

    def __oneIteration(self, iGen, infoStr):
        """
        One iteration of the GA.

        :param iGen: Current number of generation
        :type iGen: int
        :param infoStr: A string within logs are propagated.
        :type infoStr: str
        :return: The percent of GA progress (if known), the stop flag, the number of evaluated individuals
        :rtype: int, bool, int
        """
        # Update individual current generation
        self.__individualClass.CURRENT_GENERATION = iGen + 1
        self.__genAlgBehavior.startOfGeneration(self.__population, iGen, infoStr)
        # 1- Self optimizing (second order evolution)
        self.__genAlgBehavior.selfOptimize(self.__population, iGen, infoStr)
        # 2- Apply optimisation method (scaling, sharing, ...)
        self.__print("PYGA_GenAlg / run - Optimizing\n", debug=True)
        self.__genAlgBehavior.optimise(self.__population, infoStr)
        # 3- Select the kept individuals in this generation
        self.__print("PYGA_GenAlg / run - Selecting\n", debug=True)
        selectedPopulation = self.__genAlgBehavior.selection(self.__population, infoStr)
        # 4- Applie reproduction method
        self.__print("PYGA_GenAlg / run - Reproducing\n", debug=True)
        reproducedPopulation = self.__genAlgBehavior.reproduction(self.__population, selectedPopulation, infoStr)
        # 5- Set the new population
        self.__print("PYGA_GenAlg / run - Setting new population\n", debug=True)
        del self.__population
        self.__population = reproducedPopulation + selectedPopulation
        # 6- Manage end of generations
        self.__print("PYGA_GenAlg / run - Evaluating\n", debug=True)
        percent, continueEvolution, nbEval = self.__evaluation(iGen, infoStr)
        self.__genAlgBehavior.endOfGeneration(self.__population, iGen, not continueEvolution, infoStr)
        return nbEval, percent, continueEvolution

    # ===================
    # ^ Private methods ^
    # ===================
