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
# Start date: 20/07/2011
#
#-----------------------

from sys import version_info
if version_info[0] >= 3:
    unicode = str

from PyParamManager.PYPM_ParamManager import PYPM_ParamManager

from lxml import etree

from os.path import join as osjoin, dirname, abspath

from PyGenAlg.core.PYGA_Exceptions import PYGA_ParametersError, PYGA_MethodMustBeOverloaded

from sys import version_info
if version_info[0] >= 3:
    unicode = str

class PYGA_GenAlgBehavior(object):

    ALL_PARAMS = []
    __paramFileName = "baseParameters.xml"
    __paramsFile = osjoin(dirname(abspath(__file__)), __paramFileName)
    
    @classmethod
    def clearAllParams(cls):
        PYGA_GenAlgBehavior.ALL_PARAMS = []
    
    @classmethod
    def addParamFile(cls, paramsFile):
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

    def __init__(self, individualClass, populationClass, debugMode, outputPrint):
        self.addParamFile(self.__paramsFile)
        self.DEBUG_MODE = debugMode
        self.__paramManager = PYPM_ParamManager()
        self.__individualClass = individualClass
        self.__populationClass = populationClass
        self._outputPrint = outputPrint
        for param in self.ALL_PARAMS:
            self.__addParam(param)

    def getPopSize(self):
        return self.getParam(self.POPULATION_SIZE_LABEL)

    def __addParam(self, paramLabel):
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

    def isMultiObj(self):
        return self.__individualClass.MULTI_OBJ

    def isIndividualBetter(self, indiv1, indiv2, population):
        return self.__individualClass.isBetter(indiv1, indiv2, population)

    def createPopulation(self):
        return self.__populationClass(self.__individualClass, self, self.DEBUG_MODE, self._outputPrint)

    def initPopulation(self, population, infoStr):
        raise PYGA_MethodMustBeOverloaded('ERROR: This function (GenAlgBehavior.initPopulation) must be defined in derived class.')

    def generateIndiv(self):
        return self.__individualClass.generate()

    def generationStop(self, iGeneration, population, infoStr):
        raise PYGA_MethodMustBeOverloaded('ERROR: This function (GenAlgBehavior.generationStop) must be defined in derived class.')

    def stopCriteria(self, population, iGeneration, infoStr):
        raise PYGA_MethodMustBeOverloaded('ERROR: This function (GenAlgBehavior.stopCriteria) must be defined in derived class.')

    def startOfGeneration(self, population, iGeneration, infoStr):
        raise PYGA_MethodMustBeOverloaded('ERROR: This function (GenAlgBehavior.startOfGeneration) must be defined in derived class.')

    def endOfGeneration(self, population, iGeneration, endOfRun, infoStr):
        raise PYGA_MethodMustBeOverloaded('ERROR: This function (GenAlgBehavior.endOfGeneration) must be defined in derived class.')
 
    def selection(self, population, nbIndivToSelect, infoStr):
        raise PYGA_MethodMustBeOverloaded('ERROR: This function (GenAlgBehavior.selection) must be defined in derived class.')

    def reproduction(self, population, nbCrossInd, nbMutInd, infoStr):
        raise PYGA_MethodMustBeOverloaded('ERROR: This function (GenAlgBehavior.reproduction) must be defined in derived class.')

    def biasReproductionSelection(self, individuals, nbToSelect):
        raise PYGA_MethodMustBeOverloaded('ERROR: This function (GenAlgBehavior.biasReproductionSelection) must be defined in derived class.')

    def individualCrossover(self, parent1, parent2):
        return self.__individualClass.crossover(parent1, parent2)

    def individualCanBeCrossed(self, parents):
        return self.__individualClass.canBeCrossed(parents[0], parents[1])

    def individualCanBeMuted(self, indiv):
        return self.__individualClass.canBeMuted(indiv)

    def individualMutation(self, indiv):
        return self.__individualClass.mutation(indiv)

    def individualSearchSpaceInfo(self):
        return self.__individualClass.individualSearchSpaceInfo()

    def selfOptimize(self, population, infoStr):
        raise PYGA_MethodMustBeOverloaded('ERROR: This function (GenAlgBehavior.selfOptimize) must be defined in derived class.')

    def optimise(self, population, infoStr):
        raise PYGA_MethodMustBeOverloaded('ERROR: This function (GenAlgBehavior.optimise) must be defined in derived class.')

    def getParamFromKeyword(self, keyword):
        return self.__paramManager.getParamFromKeyword(keyword)

    def getParam(self, paramLabel):
        value = self.__paramManager.getParam(paramLabel)
        if hasattr(self.__class__, 'POSSIBLE_' + paramLabel.upper() + '_METHODS'):
            value = value.upper()
        return value

    def setParameters(self, **kwargs):
        self.__paramManager.setParameters(**kwargs)
        
    def getParameters(self):
        return self.__paramManager.getAllParameters()

    def getPrintInformation(self):
        return self.__paramManager.getPrintInformation()
