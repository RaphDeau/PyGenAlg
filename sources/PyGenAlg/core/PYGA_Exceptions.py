# -*- coding: utf-8 -*-
"""
Python Genetic Algorithm module.

This file contains all classes of exceptions of the GA.


License full text: https://creativecommons.org/licenses/by-nc/4.0/legalcode

Modification History:
**** 18/07/2011 ****
Creation
**** 26/09/2016 ****
Global:
- PEP8 update
- Docstring
- Meta data

TODO List:
- Complete each exception (at least "str" overloading).
"""

# Meta information
__author__ = "Raphaël Deau"
__copyright__ = "Copyright 2016, Raphaël Deau"
__license__ = "Creative Commons Attribution Non-commercial 4.0"
__version__ = "1.0.0"
__since__ = "18/07/2011"
__date__ = "26/09/2016"


class PYGA_Exception(Exception):
    """Base PYGA exception."""
    pass


class PYGA_CreationError(PYGA_Exception):
    """PYGA failed to instantiate."""
    pass


class PYGA_ParametersError(PYGA_Exception):
    """Wrong use of PYGA parameters."""
    pass


class PYGA_MethodMustBeOverloaded(PYGA_Exception):
    """A method needs to be overloaded."""

    def __init__(self, methodName):
        self.__methodName = methodName

    def __str__(self):
        s = "ERROR: This method ("
        s += self.__methodName
        s += ") must be defined in derived class."
        return s


class PYGA_PopulationError(PYGA_Exception):
    """The population is not consistent."""
    pass


class PYGA_BehaviorAddMethodError(PYGA_Exception):
    """The method cannot be added."""
    pass


class PYGA_FitnessComputation(PYGA_Exception):
    """The fitness cannot be computed."""
    pass
