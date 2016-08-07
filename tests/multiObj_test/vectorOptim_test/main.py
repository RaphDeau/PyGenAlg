# -*- mode: python; py-indent-offset: 4; tab-width: 4; coding: iso-8859-1 -*-

#######################################################################
# Author: Deau Raphaël
#
# Copyright 2011 - 2016
# License: Creative Commons Attribution Non-commercial 4.0
# Full text: https://creativecommons.org/licenses/by-nc/4.0/legalcode
#
#######################################################################

# - build-in imports -

# - PYGA imports -
from PyGenAlg.core.PYGA_GenAlg import PYGA_GenAlg

# - Local imports -
from Individual import Individual
from Behav import MyGenAlgBehavior

# Create Genetic Algorithm with own individual definition
genAlg = PYGA_GenAlg(Individual, MyGenAlgBehavior)

# Set paramaters of the GA
genAlg.setParameters(pop_size=100,
                     nb_gen=5,
                     crossrate=20,
                     mutaterate=20,
                     select='best',
                     cross_once=False,
                     del_duplicated_indiv=True,
                     exectime=0,
                     max_process=0
                     )

# Run it...
genAlg.run()

# Get the informations at the end of process
fid = open('pyga.res', 'w')
fid.write(str(genAlg.getPopulation()).replace('[', '').replace(']', ''))
fid.close()

# Get the informations at the end of process
fid = open('pyga_pareto.res', 'w')
paretoFront = genAlg.getPopulation().getBestIndividual()
s = ''
for indiv in paretoFront:
    s += str(indiv) + '\n'
fid.write(s.replace('[', '').replace(']', ''))
fid.close()

import os
os.system('gnuplot res.plot')
os.system('display figure.png')

