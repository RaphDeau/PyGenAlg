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

    @classmethod
    def startOfGeneration(cls, population, iGeneration, infoStr):
        if iGeneration == 0:
            fid = open('pyga_init.res', 'w')
            fid.write(str(population).replace('[', '').replace(']', ''))
            fid.close()
