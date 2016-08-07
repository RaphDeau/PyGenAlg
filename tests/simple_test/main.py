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

POP_FILE = 'myPop'

if __name__ == '__main__':

    genAlg = PYGA_GenAlg(Individual)
    
    genAlg.setParameters(pop_size=100, nb_gen=100,
                         repro_select_only=False,
                         del_duplicated_indiv=True,
                         crossrate=10, mutaterate=10,
                         selection='ranking',
                         scaling='linear', scalerate=0.2,
                         exectime=0.0, max_process=1)

    genAlg.run()

    genAlg.savePopulation(POP_FILE)

    endPop = genAlg.getPopulation()
#    print endPop
#    print '----'
    print endPop.getBestIndividual()
