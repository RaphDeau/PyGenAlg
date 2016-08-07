# -*- mode: python; py-indent-offset: 4; tab-width: 4; coding: iso-8859-1 -*-

#######################################################################
# Author: Deau Raphaël
#
# Copyright 2011 - 2016
# License: Creative Commons Attribution Non-commercial 4.0
# Full text: https://creativecommons.org/licenses/by-nc/4.0/legalcode
#
#######################################################################

########################################
#                                      #
# /!\ Currently on development...  /!\ #
#                                      #
########################################

import sys

import ui_mainWindow
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import pyqtSignature, SIGNAL
from Code_Editor import Code_Editor

import PYGA_GenAlgBehavior

import inspect

class MyMainWindow(QtGui.QMainWindow, ui_mainWindow.Ui_MainWindow):

    MULTI_OBJ_INDIV = ['PYGA_StandardMultiObjIndividual',
                       'PYGA_StandardMultiObjIndividual_NSGAII',
                       'PYGA_StandardVectorMultiObjIndividual_NSGAII']
                       
    BASE_INDIV_METHODS = ['generate', 'saveIndividual', 'loadIndividual', 'isBetter', 'crossover', 'mutation']
    OPTIONAL_BASE_METHODS = ['isDuplication', 'distance', 'canBeCrossed', 'canBeMuted']
    MULTI_OBJ_METHODS = ['objectives', 'computeMultiObjFitness']
    MONO_OBJ_METHODS = ['fitness']
    
    BASE_BEHAV_METHODS = []
    for item, value in PYGA_GenAlgBehavior.PYGA_GenAlgBehavior.__dict__.items():
        if hasattr(value, '__name__'):
            code = inspect.getsource(value)
            lines = code.split('\n')
            if len(lines) == 2 or len(lines) == 3 and lines[2].strip() == '':
                if lines[1].strip().startswith('print'):
                    BASE_BEHAV_METHODS.append(item)
    
    
    def __init__(self):
        super(MyMainWindow, self).__init__()
        self.setupUi(self)
        
        for treeId in ['indiv', 'behav']:
            layoutItem = eval('self.verticalLayout_'+treeId)
            # Methods display
            exec('self.'+treeId+'ItemCode = Code_Editor(self.'+treeId+'_groupBox)')
            codeItem = eval('self.'+treeId+'ItemCode')
            codeItem.setObjectName(treeId+'ItemCode')
            codeItem.installEventFilter(self)
            exec('self.connect(codeItem, SIGNAL("textChanged()"), self.'+treeId+'ItemCode_modif)')
            exec('self.'+treeId+'Desc = QtGui.QLabel(self.'+treeId+'_groupBox)')
            descItem = eval('self.'+treeId+'Desc')
            descItem.setText('')
            descItem.setObjectName(treeId+'Desc')
            layoutItem.addWidget(descItem)
            layoutItem.addWidget(codeItem)
            # Attributs display
            exec('self.'+treeId+'AttrVerticalLayout = QtGui.QVBoxLayout()')
            attrVerticalLayout = eval('self.'+treeId+'AttrVerticalLayout')
            exec('self.'+treeId+'AttrList = QtGui.QListWidget(self.'+treeId+'_groupBox)')
            attrList = eval('self.'+treeId+'AttrList')
            attrList.setObjectName(treeId+'AttrList')
            attrVerticalLayout.addWidget(attrList)
            layoutItem.addLayout(attrVerticalLayout)
            self.__showMethodsInput(treeId, False)
            self.__showAttributsInput(treeId, False)
            
        self.__currentItems = {'behav':None, 'indiv':None}
        self.__codes = {}
        
        self.__updateAllTabs()
        
    @pyqtSignature('int')
    def on_tabWidget_currentChanged(self, newTab):
        oldTreeId = 'indiv'
        newTreeId = 'behav'
        if newTab == 0:
            oldTreeId = 'behav'
            newTreeId = 'indiv'
        exec('self.'+oldTreeId+'ItemCode.hide()')
        item = eval('self.'+newTreeId+'_treeWidget.currentItem()')
        if item is not None and item.parent() is not None and\
           item.parent().text(0) == 'Overloaded methods':
            codeItem = eval('self.'+newTreeId+'ItemCode') 
            codeItem.show()
            #layoutItem = eval('self.verticalLayout_'+newTreeId)
            #layoutItem.addWidget(codeItem)
    
    @pyqtSignature('QString')
    def on_indivBaseClass_comboBox_activated(self, newValue):
        self.__updateIndivTab()
    
    @pyqtSignature('QString')
    def on_behavBaseClass_comboBox_activated(self, newValue):
        self.__updateBehavTab()
        
    @pyqtSignature('int')
    def on_multiObj_checkBox_stateChanged(self, i):
        self.__updateIndivTab()
        
    @pyqtSignature('QTreeWidgetItem *, int')
    def on_indiv_treeWidget_itemClicked(self, item, i):
        self.__manageTreeClic('indiv', item, i)
       
    @pyqtSignature('QTreeWidgetItem *, int')
    def on_behav_treeWidget_itemClicked(self, item, i):
        self.__manageTreeClic('behav', item, i)
        
    def indivItemCode_modif(self):
        self.__manageCodeModif('indiv')
        
    def behavItemCode_modif(self):
        self.__manageCodeModif('behav')
   
    def __manageTreeClic(self, treeId, item, col):
        title = item.text(col)
        codeItem = eval('self.'+treeId+'ItemCode')
        descItem = eval('self.'+treeId+'Desc')
        attrList = eval('self.'+treeId+'AttrList')
        if item.parent() is not None:
            if item.parent().text(0) == 'Overloaded methods':
                self.__currentItems[treeId] = item
                title = item.parent().text(col) + ' - ' + title
                module = str(eval('self.'+treeId+'BaseClass_comboBox.currentText()'))
                exec('from '+module+' import '+module) 
                doc = module+'.'+item.text(col)+'.__doc__'
                docStr = eval(str(doc))
                if docStr is None:
                    docStr = 'The description of this element is not available.'
                descItem = eval('self.'+treeId+'Desc')
                descItem.setText(docStr)
                codeItem.setEnabled(True)
                code = ''
                if item in self.__codes.keys():
                    code = self.__codes[item]
                codeItem.setText(code)
                
                self.__showMethodsInput(treeId)
                self.__showAttributsInput(treeId, False)
        else:
            self.__showMethodsInput(treeId, False)
            if item.text(0) == 'Attributs':
                self.__showAttributsInput(treeId)
            else:
                self.__showAttributsInput(treeId, False)
            
        groupBox = eval('self.'+treeId+'_groupBox')
        groupBox.setTitle(title)
        
        
    def __showMethodsInput(self, treeId, show=True):
        codeItem = eval('self.'+treeId+'ItemCode')
        descItem = eval('self.'+treeId+'Desc')
        if show:
            descItem.show()
            codeItem.show()
        else:
            descItem.hide()
            codeItem.hide()
        
    def __showAttributsInput(self, treeId, show=True):
        attrList = eval('self.'+treeId+'AttrList')
        if show:
            attrList.show()
        else:
            attrList.hide()
            
    def __manageCodeModif(self, itemId):
        exec('code = self.'+itemId+'ItemCode.text()')
        self.__codes[self.__currentItems[itemId]] = str(code)
   
    def __updateAllTabs(self):
        self.__updateIndivTab()
        self.__updateBehavTab()
        self.__updateParamTab()
    
    def __updateIndivTab(self):
        className = str(self.indivBaseClass_comboBox.currentText())
        isMulti = self.multiObj_checkBox.checkState() == 2
        multiForced = className in self.MULTI_OBJ_INDIV
        self.multiObj_checkBox.setEnabled(not multiForced)
        if not isMulti and multiForced:
            self.multiObj_checkBox.setChecked(multiForced)
            isMulti = True
            
        overloadMethItem = self.indiv_treeWidget.topLevelItem(1)
        allMethods = list(self.BASE_INDIV_METHODS)
        
        if isMulti:
            allMethods += self.MULTI_OBJ_METHODS
        else:
            allMethods += self.MONO_OBJ_METHODS
        
        self.__updateTree(className, 'PYGA_Individual', allMethods, overloadMethItem)
        
    def __updateBehavTab(self):
        className = str(self.behavBaseClass_comboBox.currentText())
        overloadMethItem = self.behav_treeWidget.topLevelItem(0)
        allMethods = list(self.BASE_BEHAV_METHODS)
        
        self.__updateTree(className, 'PYGA_GenAlgBehavior', allMethods, overloadMethItem)
        
        self.__updateParamTab()
    
    def __updateParamTab(self):
        behavClassName = str(self.behavBaseClass_comboBox.currentText())
        exec('import '+ behavClassName)
        behavClassPtr = eval(behavClassName+'.'+behavClassName)
      
        allCat = {}
        for param in behavClassPtr.ALL_PARAMS:
            newCat = eval('behavClassPtr.'+param.upper()+'_CATEGORY')
            catPath = newCat.split('.')
            curCatDict = allCat
            for c in catPath:
                if c not in curCatDict.keys():
                    curCatDict[c]= {}
                curCatDict = curCatDict[c]
            curCatDict[param] = eval('behavClassPtr.'+param.upper()+'_DEFAULT_VALUE')
        self.param_treeWidget.clear()
  
        curParamTreeItem = self.param_treeWidget.topLevelItem(0)
        self.__createCatTree(allCat, self.param_treeWidget)
    
                
    def __createCatTree(self, currentCat, currentParamTreeItem):
        for cat, subcats in currentCat.items():
            newCat = QtGui.QTreeWidgetItem(currentParamTreeItem)
            newCat.setText(0, cat)
            if type(subcats) == type({}):
                self.__createCatTree(subcats, newCat)
            else:
                newCat.setText(1, str(subcats))
                flags = newCat.flags()
                newCat.setFlags(flags|QtCore.Qt.ItemIsEditable)
    
        
    def __updateTree(self, className, baseClass, methods, overloadMethItem):
        
        overloadMethItem.takeChildren()
        
        exec('import '+ className)
        classPtr = eval(className+'.'+className)
        
        for m in methods:
            isKnown = False
            i = 0
            while not isKnown and i < overloadMethItem.childCount():
                if m == overloadMethItem.child(i).text(0):
                    isKnown = True
                i += 1
            if not isKnown:
                if self.originalClassMethod(m, classPtr) == baseClass:
                    newItem = QtGui.QTreeWidgetItem(overloadMethItem)
                    newItem.setText(0, m)
    
    def originalClassMethod(self, methName, classPtr):
        if methName in classPtr.__dict__.keys():
            return classPtr.__name__
        else:
            return self.originalClassMethod(methName, classPtr.__bases__[0])
        
    
       
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myWindow = MyMainWindow()
    myWindow.show()
    sys.exit(app.exec_())