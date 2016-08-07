# -*- mode: python; py-indent-offset: 4; tab-width: 4; coding: iso-8859-1 -*-

#######################################################################
# Author: Deau Raphaël
#
# Copyright 2011 - 2016
# License: Creative Commons Attribution Non-commercial 4.0
# Full text: https://creativecommons.org/licenses/by-nc/4.0/legalcode
#
#######################################################################

class PYPM_ParamManager:

    def __init__(self):
        # Keep a list of all categories
        self.__paramCategories = []
        # And a dictionnary matching a category with the text to 
        # display if this caegory is "None"
        self.__possibleNoneCategories = {}
        # Finally create a dictionnary matching a category with a dictonnary
        # matching all parameter of this category (label) with:
        #      - its description (text to display)
        #      - its value
        #      - the method used to check its value
        #      - the method to launch when the value is set (or changed)
        self.__params = {}
        # And a dictionnary matching a keyword (used in setParameter) 
        # with the category and the label of the parameter.
        self.__allParamsKeywords = {}
        # Manage the id of all know params
        self.__allParamsID = []
        # Store the category of each param
        self.__categoryOfParam = {}

    def addParam(self, category, name, keywords, description, 
                 check_method, value, change_method, noneValue=None,
                 noneDescription=None):        
        # 1- Add the parameter to the list of all param and to the list of keywords
        if name not in self.__allParamsID:
            self.__allParamsID.append(name)
            for keyword in keywords:
                self.__allParamsKeywords[keyword] = [category, name]
        # 2- Add the category if needed
        if category not in self.__paramCategories:
            self.__paramCategories.append(category)
            self.__params[category] = {}
        # 3- Add the parameter to the main list of parameters
        self.__params[category][name] = {'description':description,
                                         'value':value,
                                         'checkMethod':check_method,
                                         'changeMethod':change_method,
                                         'noneValue':noneValue,
                                         'noneDescription':noneDescription,
                                         'keywords':keywords}
        self.__categoryOfParam[name] = category
        if noneValue is not None:
            self.__addPossibleNoneCategory(category, name)

    def __addPossibleNoneCategory(self, category, paramLabel):
        # 1- Check if the category already exists
        if category not in self.__possibleNoneCategories:
            self.__possibleNoneCategories[category] = []
        # 2- Add the category to the dictionnary of "None categories"
        self.__possibleNoneCategories[category].append(paramLabel)

    def getParam(self, paramLabel):
        # 1- Check if the parameter is known
        if paramLabel not in self.__allParamsID:
            raise Exception, 'ERROR: Unknown parameter ' + paramLabel + '.'
        # 2- Return the dictionnary of this parameter containing:
        #      - its description (text to display)
        #      - its value
        #      - the method used to check its value
        #      - the method to launch when the value is set (or changed)
        category = self.__categoryOfParam[paramLabel]
        return self.__params[category][paramLabel]['value']

    def __getParamDict(self, paramLabel):
        # 1- Check if the parameter is known
        if paramLabel not in self.__allParamsID:
            raise Exception, 'ERROR: Unknown parameter ' + paramLabel + '.'
        # 2- Return the dictionnary of this parameter containing:
        #      - its description (text to display)
        #      - its value
        #      - the method used to check its value
        #      - the method to launch when the value is set (or changed)
        category = self.__categoryOfParam[paramLabel]
        return self.__params[category][paramLabel]

    def setParameters(self, **kwargs):
        # 1- Get each parameter to set
        for key in kwargs.keys():
            # 1.1- Check if the parameter is known
            upKey = key.upper()
            if upKey not in self.__allParamsKeywords.keys():
                error = 'Unkown parameter ' + key + '.\n'
                error += 'Availables parameters are: ' + str(self.__allParamsID)
                raise Exception, error
            else:
                # 1.2.1- Store the new value and a string to get this value
                strKwarg = 'kwargs[key]'
                value = kwargs[key]
                # 1.2.2- Get the category and the label of the parameter
                _, paramLabel = self.__allParamsKeywords[upKey]
                # 1.2.3- Get the dictionnary of the parameter
                param = self.__getParamDict(paramLabel)
                # 1.2.4- Launch the check method with the right value
                eval('param[\'checkMethod\']('+strKwarg+')')
                # 1.2.5- The value is OK (exception if not), save it
                param['value'] = value
                # 1.2.6- Launch the "change method" if needed
                if param['changeMethod'] is not None:
                    eval('param[\'changeMethod\']('+strKwarg+')')

    def getParamFromKeyword(self, keyword):
        paramFound = None
        for catDict in self.__params.values():
            for paramName, paramDict in catDict.items():
                if keyword.upper() in paramDict["keywords"]:
                    paramFound = paramName
        return paramFound

    def getAllParameters(self):
        allParam = {}
        for pValue in self.__params.values():
            for attrName, val in pValue.items():
                allParam[attrName] = val['value']
        return allParam

    def getPrintInformation(self):
        param_dict = {}
        for paramCat in self.__paramCategories:
            catList = paramCat.split('.')
            paramDict = param_dict
            noneCat = False
            for i, cat in enumerate(catList):
                curCat = '.'.join(catList[:i+1])
                if curCat in self.__possibleNoneCategories.keys():
                    for paramLabel in self.__possibleNoneCategories[curCat]:
                        paramValue = self.getParam(paramLabel)
                        noneValue = self.__getParamDict(paramLabel)['noneValue']
                        if paramValue == noneValue:
                            paramDict[cat] = self.__getParamDict(paramLabel)['noneDescription']
                            noneCat = True
                if not noneCat:
                    if cat not in paramDict.keys():
                        paramDict[cat] = {}
                        paramDict = paramDict[cat]
                    else:
                        paramDict = paramDict[cat]

            if not noneCat:
                for label, param in self.__params[paramCat].items():
                    paramDict[label] = [param['description'], param['value']]

        return self.__getPrintInfo(param_dict)

    def __getPrintInfo(self, param, tab=0):
        s = ""
        for item, value in param.items():
            if type(value) == type({}):
                c = ''
                if tab != 0:
                    c = '- '
                s += '\t'*tab + c + item + ' information:\n'
                s += self.__getPrintInfo(value, tab+1)
            else:
                if type(value) == type([]):
                    s += '\t'*tab + '- ' + value[0] + ' = ' + str(value[1]) + '\n'
                else:
                    s += '\t'*tab + '- ' + value + '\n'
        return s

    def saveParameters(self, filename):
        fid = open(filename, 'w')
        for category, params in self.__params.items():
            for name, paramDict in params.items():
                fid.write(category + ';' + name + ';')
                fid.write(paramDict['description'] + ';')
                if type(paramDict['value']) == type(''):
                    fid.write('"'+str(paramDict['value']) + '";')
                else:
                    fid.write(str(paramDict['value']) + ';')
                fid.write(str(paramDict['checkMethod']) + ';')
                fid.write(str(paramDict['changeMethod']) + ';')
                fid.write(str(paramDict['noneValue']) + ';')
                if paramDict['noneDescription'] is None:
                    fid.write(str(paramDict['noneDescription']) + ';')
                else:
                    fid.write('"'+str(paramDict['noneDescription']) + '";')
                fid.write(str(paramDict['keywords']) + '\n')
        fid.close()

    def loadParameters(self, filename):
        fid = open(filename, 'r')
        lines = fid.readlines()
        fid.close()

        for line in lines:
            splitLine = line.split(';')
            category = splitLine[0]
            name = splitLine[1]
            description = splitLine[2]
            value = eval(splitLine[3])
            check_method = splitLine[4]
            change_method = splitLine[5]
            noneValue = eval(splitLine[6])
            noneDescription = eval(splitLine[7])
            keywords = eval(splitLine[8])
            self.addParam(category, name, keywords, description, check_method, 
                          value, change_method, noneValue, noneDescription)
