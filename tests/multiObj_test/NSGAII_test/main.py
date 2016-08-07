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


# - build-in imports -
import sys

# - PYGA imports -
from PyGenAlg.core.PYGA_GenAlg import PYGA_GenAlg

# - Local imports -
from Individual import Individual

# Create Genetic Algorithm with own individual definition
genAlg = PYGA_GenAlg(Individual)

# Set parameters of the GA
genAlg.setParameters(pop_size=50,
                     nb_gen=10,
                     crossrate=45,
                     mutaterate=45,
                     select='best',
                     cross_once=False,
                     exectime=0,
                     max_process=0
                     )

# Run it...
genAlg.run()

# Get the informations at the end of process
fid = open('pyga.res', 'w')
sys.stdout = fid
print str(genAlg.getPopulation()).replace('[', '').replace(']', '')
sys.stdout = sys.__stdout__
fid.close()

# Get the informations at the end of process
fid = open('pyga_pareto.res', 'w')
sys.stdout = fid
paretoFront = genAlg.getPopulation().getBestIndividual()
s = ''
for indiv in paretoFront:
    s += str(indiv) + '\n'
print s.replace('[', '').replace(']', '')
sys.stdout = sys.__stdout__
fid.close()

import os
os.system('gnuplot res.plot')
os.system('display figure.png')

