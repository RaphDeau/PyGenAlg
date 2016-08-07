# -*- mode: python; py-indent-offset: 4; tab-width: 4; coding: iso-8859-1 -*-

#######################################################################
# Author: Deau Raphaël
#
# Copyright 2011 - 2016
# License: Creative Commons Attribution Non-commercial 4.0
# Full text: https://creativecommons.org/licenses/by-nc/4.0/legalcode
#
#######################################################################

from PyGenAlg.standards.PYGA_StandardVectorMultiObjIndividual_NSGAII import PYGA_StandardVectorMultiObjIndividual_NSGAII

import random
import sys
import math

class Individual(PYGA_StandardVectorMultiObjIndividual_NSGAII):

    NB_VARIABLES = 2
#    VARIABLES_DEFAULT_VALUES = [None]
#    VARIABLES_RANGES = ['[-10, 10]']
#    VARIABLES_TYPE = float

    NB_OBJECTIVES = 3
    OBJ_TYPES = ["max", "max", "max"]

    @classmethod
    def f0(cls, x):
        return x*math.sin(1/(abs(x)+pow(10, -9)))

    # @classmethod
    # def f1(cls, x):
    #     return -x[0] + pow(x[1], 2)
    # @classmethod
    # def f2(cls, x):
    #     return -x[1] + pow(x[0], 2)
    # @classmethod
    # def f3(cls, x):
    #     return cls.f0(x[0]) + cls.f0(x[1])

    @classmethod
    def f1(cls, x):
        return pow(x[0] - x[1], 2)
    @classmethod
    def f2(cls, x):
        return pow(x[1] - x[0], 2)
    @classmethod
    def f3(cls, x):
        return pow(x[0] + x[1], 2)

    @classmethod
    def f(cls, x):
        return [cls.f1(x), cls.f2(x), cls.f3(x)]

    def __init__(self, values=None):
        PYGA_StandardVectorMultiObjIndividual_NSGAII.__init__(self)

    def __str__(self):
        return str(self.getObj()).replace('[', '').replace(']', '')

    @classmethod
    def computeObj(cls, variables):
        return cls.f(variables)
    
