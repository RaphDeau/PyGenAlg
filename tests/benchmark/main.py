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

from PyGenAlg.core.PYGA_GenAlg import PYGA_GenAlg

from Sphere_indiv import SphereIndiv, SphereBehav
import random

if __name__ == "__main__":
    logFid = open("logGA_sphere.log", 'w')
    random.seed(0)
    genAlg = PYGA_GenAlg(SphereIndiv, SphereBehav, outputPrint=logFid)

    genAlg.setParameters(pop_size=50, 
                         nb_gen=64,
                         repro_selected_only=False,
                         del_duplicated_indiv=True,
                         crossrate=5, 
                         mutaterate=0,
                         selection='best')

    genAlg.run()

    endPop = genAlg.getPopulation()
    print endPop
    print '----'
    print endPop.getBestIndividual()
    
    logFid.close()
