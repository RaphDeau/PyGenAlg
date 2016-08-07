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

class MyGenAlgBehavior(PYGA_StandardGenAlgBehavior):

    PYGA_StandardGenAlgBehavior.ADD_METHOD(selection=['mysel', 'MySelection'])

    @classmethod
    def MySelection(cls, population, nbToSelect):
        print 'Calling MySelection'
        return population

    @classmethod
    def startOfGeneration(cls, population, iGeneration, infoStr):
        print 'start of #', iGeneration

    @classmethod
    def endOfGeneration(cls, population, iGeneration, endOfRun, infoStr):
        print 'end of #', iGeneration , '(', endOfRun, ')'

    @classmethod
    def stopCriteria(cls, population, iGeneration, infoStr):
        print 'Stop criteria'
        return False
