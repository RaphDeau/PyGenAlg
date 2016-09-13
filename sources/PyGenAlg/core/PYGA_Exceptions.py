# -*- mode: python; py-indent-offset: 4; tab-width: 4; coding: iso-8859-1 -*-

#######################################################################
# Author: Deau Raphaël
#
# Copyright 2011 - 2016
# License: Creative Commons Attribution Non-commercial 4.0
# Full text: https://creativecommons.org/licenses/by-nc/4.0/legalcode
#
#######################################################################


class PYGA_Exception(Exception):
    """Base PYGA exception."""
    pass


class PYGA_CreationError(PYGA_Exception):
    """PYGA failed to instanciate."""
    pass


class PYGA_ParametersError(PYGA_Exception):
    """Wrong use of PYGA parameters."""
    pass


class PYGA_MethodMustBeOverloaded(PYGA_Exception):
    """A method needs to be overloaded."""
    pass


class PYGA_PopulationError(PYGA_Exception):
    """The population is not consistant."""
    pass


class PYGA_BehaviorAddMethodError(PYGA_Exception):
    """The method cannot be added."""
    pass


class PYGA_FitnessComputation(PYGA_Exception):
    """The fitness cannot be computed."""
    pass
