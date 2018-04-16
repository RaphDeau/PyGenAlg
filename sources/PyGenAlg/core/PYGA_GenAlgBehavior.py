# -*- coding: utf-8 -*-
"""
Python Genetic Algorithm module.

This file contains the base class of the behavior of the GA: PYGA_GenAlgBehavior.
It defines how the GA must act at each step of the GA cycle.

License full text: https://creativecommons.org/licenses/by-nc/4.0/legalcode



Modification History:
**** 20/07/2011 ****
Creation
**** 28/09/2016 ****
Global:
- PEP8 update
- Docstring
- Meta data
- Removed unused methods
- Removed method that had no sens to be here (used in Standard behavior)

TODO List:
-
"""
# - Build-in imports -
from lxml import etree
from os.path import join as osjoin, dirname, abspath
from sys import version_info

# - Local imports -
from PyParamManager.PYPM_ParamManager import PYPM_ParamManager
from PyGenAlg.core.PYGA_Exceptions import PYGA_ParametersError, PYGA_MethodMustBeOverloaded

# Manage python versions compatibility
if version_info[0] >= 3:
    unicode = str

# Meta information
__author__ = "Raphaël Deau"
__copyright__ = "Copyright 2016, Raphaël Deau"
__license__ = "Creative Commons Attribution Non-commercial 4.0"
__version__ = "1.0.0"
__since__ = "20/07/2011"
__date__ = "28/09/2016"


class PYGA_GenAlgBehavior(object):
    """
    This class is the base for the GA behavior coding.
    It allows defining:
        - The parameters of the GA:
            * The existing ones
            * The news that you may create
            * Methods available:
                + getParamFromKeyword
                + getParam
                + setParameters
                + getParameters
        - The behavior of the GA for following basic actions that must be overwritten:
            * stopCriteria
            * startOfGeneration
            * endOfGeneration
            * selection
            * reproduction
            * selfOptimize
            * optimise

    A "standard behavior and parameters set" is provided in PYGA_StandardGenAlgBehavior.

    Attributes:
        :ivar __paramManager: The parameters manager.
        :type __paramManager: PYPM_ParamManager
        :ivar __individualClass: The individual class to use.
        :type __individualClass: type derived from PYGA_Individual
        :ivar __populationClass: The population class to use.
        :type __populationClass: type derived from PYGa_Population
    """

    ALL_PARAMS = []
    __paramFileName = "baseParameters.xml"
    __paramsFile = osjoin(dirname(abspath(__file__)), __paramFileName)
    
    @classmethod
    def clearAllParams(cls):
        """Delete all known parameters."""
        PYGA_GenAlgBehavior.ALL_PARAMS = []
    
    @classmethod
    def addParamFile(cls, paramsFile):
        """
        Parse a parameter file to load them in the behavior.

        :param paramsFile: The file within the parameters are read. Must exists.
        :type paramsFile: str
        """
        # TODO: This parameter management must be reviewed!
        paramXmlRoot = etree.parse(paramsFile)
        for param in paramXmlRoot.getroot():
            if param.tag == "Parameter":
                paramLabel = param.get("name")
                exec("cls."+paramLabel.upper()+"_LABEL=\""+paramLabel+"\"")
                for element in param:
                    if element.tag == "Check_Method":
                        exec(element.text)
                        methodName = element.text.split(' ')[1].split('(')[0]
                        exec("cls."+paramLabel.upper()+"_"+element.tag.upper()+"="+methodName)
                    elif element.tag != "NeededAttributes":
                        exec("cls."+paramLabel.upper()+"_"+element.tag.upper()+"="+element.text)
                    else:
                        for attribute in element:
                            if attribute.tag == "Attribute":
                                exec("cls."+attribute.get("name")+"="+attribute.text)
                if paramLabel not in cls.ALL_PARAMS:
                    cls.ALL_PARAMS.append(paramLabel)
                else:
                    raise PYGA_ParametersError("ERROR: Parameter " + unicode(paramLabel) + " defined twice.")

    def __init__(self, individualClass, populationClass, printMethod):
        """
        Constructor of the behavior.

        :param individualClass: The class coding an individual
        :type individualClass: type derived from PYGA_Individual
        :param populationClass: The class coding a population (set of individual)
        :type populationClass: type Derived from PYGA_Population
        :param printMethod: The method to print the logs
        :type printMethod: Python method
        """
        self.addParamFile(self.__paramsFile)
        self.__paramManager = PYPM_ParamManager()
        self.__individualClass = individualClass
        self.__populationClass = populationClass
        # Store outputPrint public so derived class can use it.
        self.printLog = printMethod
        for param in self.ALL_PARAMS:
            self.__addParam(param)

    def __addParam(self, paramLabel):
        """
        Add a parameter to the known parameters list.

        :param paramLabel: The identifier of the parameter
        :type paramLabel: str
        """
        # TODO: Rework this...?
        upParam = paramLabel.upper()
        category = eval('self.' + upParam + '_CATEGORY')
        keywords = eval('self.' + upParam + '_KEYWORDS')
        description = eval('self.' + upParam + '_DESCRIPTION')
        check_method = eval('self.' + upParam + '_CHECK_METHOD')
        value = eval('self.' + upParam + '_DEFAULT_VALUE')
        try:
            change_method = eval('self.' + upParam + '_CHANGE_METHOD')
        except:
            change_method = None
        try:
            noneValue = eval('self.' + upParam + '_NONE_VALUE')
            noneDescription = eval('self.' + upParam + '_NONE_DESCRIPTION')
        except:
            noneValue = None
            noneDescription = None

        self.__paramManager.addParam(category, paramLabel, keywords, description, 
                                     check_method, value, change_method, noneValue,
                                     noneDescription)

    def getIndividualClass(self):
        """Allows child classes to know the individual class."""
        return self.__individualClass

    def createPopulation(self):
        """Create a new population."""
        return self.__populationClass(self.__individualClass, self, self.printLog)

    def initPopulation(self, population, infoStr):
        """
        [ MUST BE OVERLOADED ]

        Initialise the given population.

        :param population: The population to initialise
        :type population: Derived from PYGA_Population
        :param infoStr: The log string to concatenate.
        :type infoStr: str
        """
        raise PYGA_MethodMustBeOverloaded("GenAlgBehavior.initPopulation")

    def stopCriteria(self, population, iGeneration, startTime, infoStr):
        """
        [ MUST BE OVERLOADED ]

        Defines the stop criteria of the GA.

        :param iGeneration: The current generation number.
        :type iGeneration: int
        :param population: The current population.
        :type population: Derived from PYGA_Population
        :param startTime: The start time of the evolution
        :type startTime: float
        :param infoStr: The log string to concatenate.
        :type infoStr: str
        :return: The percent of evolution, True if the evolution must stop
        :rtype: int, bool
        """
        raise PYGA_MethodMustBeOverloaded("GenAlgBehavior.stopCriteria")

    def startOfGeneration(self, population, iGeneration, infoStr):
        """
        [ MUST BE OVERLOADED ]

        Called at the beginning of each generation.

        :param population: The current population
        :type population: Derived from PYGA_Population
        :param iGeneration: The current generation number.
        :type iGeneration: int
        :param infoStr: The log string to concatenate.
        :type infoStr: str
        """
        raise PYGA_MethodMustBeOverloaded("GenAlgBehavior.startOfGeneration")

    def endOfGeneration(self, population, iGeneration, endOfRun, infoStr):
        """
        [ MUST BE OVERLOADED ]

        Called at the end of each generation.

        :param population: The current population
        :type population: Derived from PYGA_Population
        :param iGeneration: The current generation number.
        :type iGeneration: int
        :param endOfRun: True if the stop criteria returned "True" (last generation)
        :type endOfRun: bool
        :param infoStr: The log string to concatenate.
        :type infoStr: str
        """
        raise PYGA_MethodMustBeOverloaded("GenAlgBehavior.endOfGeneration")
 
    def selection(self, population, infoStr):
        """
        [ MUST BE OVERLOADED ]

        The selection operation of the GA.
        The selected individuals will be kept for the next generation.

        :param population: The current population.
        :type population: Derived from PYGA_Population
        :param infoStr: The log string to concatenate.
        :type infoStr: str
        :return: The selected individuals as a Population.
        :rtype: Derived from PYGA_Population
        """
        raise PYGA_MethodMustBeOverloaded("GenAlgBehavior.selection")

    def reproduction(self, population, selectedPopulation, infoStr):
        """
        [ MUST BE OVERLOADED ]

        The reproduction phase of the GA.

        :param population: The current population.
        :type population: Derived from PYGA_Population
        :param selectedPopulation: The selected population (will be kept for next generation).
        :type selectedPopulation: Derived from PYGA_Population
        :param infoStr: The log string to concatenate.
        :type infoStr: str
        :return: The generated individuals as a Population.
        :rtype: Derived from PYGA_Population
        """
        raise PYGA_MethodMustBeOverloaded("GenAlgBehavior.reproduction")

    def selfOptimize(self, population, infoStr):
        """
        [ MUST BE OVERLOADED ]

        Optimise the parameters by itself (Second order evolution).

        :param population: The current population.
        :type population: Derived from PYGA_Population
        :param infoStr: The log string to concatenate.
        :type infoStr: str
        """
        raise PYGA_MethodMustBeOverloaded("GenAlgBehavior.selfOptimize")

    def optimise(self, population, infoStr):
        """
        [ MUST BE OVERLOADED ]

        Optimise the fitness of the individuals (scaling, sharing ...)

        :param population: The current population.
        :type population: Derived from PYGA_Population
        :param infoStr: The log string to concatenate.
        :type infoStr: str
        """
        raise PYGA_MethodMustBeOverloaded("GenAlgBehavior.optimise")

    def getParamFromKeyword(self, keyword):
        """Return a parameter name according to a keyword."""
        return self.__paramManager.getParamFromKeyword(keyword)

    def getParam(self, paramLabel):
        """Get the value of the given parameter name."""
        value = self.__paramManager.getParam(paramLabel)
        # If a parameter has possible methods associated, its value
        # must be uppercase to be used to find the method.
        if hasattr(self.__class__, 'POSSIBLE_' + paramLabel.upper() + '_METHODS'):
            value = value.upper()
        return value

    def setParameters(self, **kwargs):
        """
        Set the values of the parameters.
        Parameters are given has "paramKeyword=paramValue".
        """
        self.__paramManager.setParameters(**kwargs)
        
    def getParameters(self):
        """Return the values of all parameters."""
        return self.__paramManager.getAllParameters()

    def getPrintInformation(self):
        """Get a formated string containing all parameters values sorted by categories."""
        return self.__paramManager.getPrintInformation()
