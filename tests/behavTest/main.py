# -*- mode: python; py-indent-offset: 4; tab-width: 4; coding: iso-8859-1 -*-

#######################################################################
# Author: Deau Raphaël
#
# Copyright 2011 - 2016
# License: Creative Commons Attribution Non-commercial 4.0
# Full text: https://creativecommons.org/licenses/by-nc/4.0/legalcode
#
#######################################################################

from PyGenAlg.core.PYGA_GenAlg import PYGA_GenAlg

from Individual import Individual
from MyBehav import MyGenAlgBehavior

Individual.SLEEP = False

genAlg = PYGA_GenAlg(Individual, MyGenAlgBehavior)
genAlg.setParameters(pop_size=100, nb_gen=10,
                     repro_select_only=True,
                     crossrate=40, mutaterate=40, 
                     selection='MySel',
                     scaling='linear', scalerate=0.2,
                     exectime=10.0, max_process=1)

import random
random.seed(0)

genAlg.run()
