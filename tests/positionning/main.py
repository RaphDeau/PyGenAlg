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

from positionning_Behav import PositionningBehavior
from positionning_indiv import PositionningIndiv
# import random
# random.seed(0)

import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from numpy import arange

SPACE_MATRIX = [8, 8]
OBJECT_TO_PLACE = [[1, 4], [3, 2], [5, 1], [2, 2], [6, 3], [3, 1], [2, 3], [1, 5]]
OBJECT_TO_PLACE_COL = ["red", "green", "yellow", "orange", "lightgreen", "blue", [0.5, 0.5, 0.5], "black"]

fig = plt.figure()
ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)
xTicks = arange(0, SPACE_MATRIX[0] + 1, 1)
yTicks = arange(0, SPACE_MATRIX[1] + 1, 1)

plt.show(block=False)

def plotIndiv(indiv, i):
    ax = eval("ax" + str(i))
    ax.cla()
    ax.set_xticks(xTicks)
    ax.set_yticks(yTicks)
    ax.grid()
    codes = [Path.MOVETO,
             Path.LINETO,
             Path.LINETO,
             Path.LINETO,
             Path.CLOSEPOLY,
             ]
    for rectVertices, color in indiv.getAllObjectRect():
        path = Path(rectVertices, codes)
        patch = patches.PathPatch(path, facecolor=color, lw=2)
        ax.add_patch(patch)
    plt.draw()

if __name__ == "__main__":
    
    logFid = open("logGA_positionning.log", 'w')
    
    PositionningBehavior.SET_PLOT_INFO(plotIndiv)
    PositionningIndiv.INIT_PARAM(SPACE_MATRIX, OBJECT_TO_PLACE, OBJECT_TO_PLACE_COL)
    
    genAlg = PYGA_GenAlg(PositionningIndiv, PositionningBehavior, outputPrint=logFid)

    genAlg.setParameters(pop_size=50,
                         nb_gen=0,
                         repro_selected_only=False,
                         del_duplicated_indiv=True,
                         crossrate=10,
                         mutaterate=85,
                         selection='best',
                         sharing_rate=0.0,
                         influence_dist=23,
                         scaleRate=1.0
                         )
    genAlg.run()
    endPop = genAlg.getPopulation()
    bestInd = endPop.getBestIndividual()
    print(endPop)
    print('----')
    print(bestInd)
    print("Generation: ", endPop[0].getBirthGeneration())
    sortedPop = endPop.getBestIndividual(4)
            
    plotIndiv(sortedPop[0], 1)
    plotIndiv(sortedPop[1], 2)
    plotIndiv(sortedPop[2], 3)
    plotIndiv(sortedPop[3], 4)
    plt.show()
    logFid.close()
