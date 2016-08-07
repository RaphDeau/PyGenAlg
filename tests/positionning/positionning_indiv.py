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
import random
from math import sqrt

# - local imports -
from PyGenAlg.core.PYGA_Individual import PYGA_Individual

class PositionningIndiv(PYGA_Individual):
    
    __SPACE_MATRIX = None
    __OBJECT_TO_PLACE = None
    __OBJECT_TO_PLACE_COL = None
    
    @classmethod
    def INIT_PARAM(cls, spaceMatrix, objects, colors):
        cls.__SPACE_MATRIX = spaceMatrix
        cls.__OBJECT_TO_PLACE = objects
        cls.__OBJECT_TO_PLACE_COL = colors
    
    def __init__(self):
        PYGA_Individual.__init__(self)
        self.__positions = None
        self.__canTouch = True
    
    def getSpaceMatrix(self):
        return self.__SPACE_MATRIX
    
    def getAllObjectRect(self):
        allVerts = []
        for i, pos in enumerate(self.__positions):
            width = self.__OBJECT_TO_PLACE[i][0]
            high = self.__OBJECT_TO_PLACE[i][1]
            verts = [
                    (pos[0]-1, pos[1]-high), # left, bottom
                    (pos[0]-1, pos[1]), # left, top
                    (pos[0]+width-1, pos[1]), # right, top
                    (pos[0]+width-1, pos[1]-high), # right, bottom
                    (0., 0.), # ignored
                    ]
            allVerts.append([verts, self.__OBJECT_TO_PLACE_COL[i]])
        return allVerts
    
    @classmethod
    def generate(cls):
        newInd = cls()
        newInd.__positions = []
        for i in xrange(len(cls.__OBJECT_TO_PLACE)):
            newInd.__positions.append(newInd.__generateAnchor(i))
        return newInd
    
    def fitness(self, population):
        fitness = 0.0
        for i1 in xrange(len(self.__positions)):
            for i2 in xrange(len(self.__positions)):
                if i2 > i1:
                    fitness += self.__conflict(i1, i2)
        return fitness
    
    def printColisions(self):
        for ip1 in xrange(len(self.__positions)):
            for ip2 in xrange(len(self.__positions)):
                if ip2 > ip1:
                    nbConflict = self.__conflict(ip1, ip2)
                    print "Colision:", ip1, "-", ip2, "-->", nbConflict
    
    def __isOutOfSpace(self, index, anchor=None):
        if anchor is None:
            x_anchor = self.__positions[index][0]
            y_anchor = self.__positions[index][1]
        else:
            x_anchor = anchor[0]
            y_anchor = anchor[1]
        width = self.__OBJECT_TO_PLACE[index][0]
        high = self.__OBJECT_TO_PLACE[index][1]
        outside = False
        if x_anchor < 1 or y_anchor - high+1 < 1 or\
           x_anchor + width -1 > self.__SPACE_MATRIX[0] or\
           y_anchor > self.__SPACE_MATRIX[1]:
            outside = True
        return outside
    
    def __conflict(self, index1, index2):
        e1_x_anchor = self.__positions[index1][0]
        e1_y_anchor = self.__positions[index1][1]
        e2_x_anchor = self.__positions[index2][0]
        e2_y_anchor = self.__positions[index2][1]
        e1_width = self.__OBJECT_TO_PLACE[index1][0]
        e1_high = self.__OBJECT_TO_PLACE[index1][1]
        e2_width = self.__OBJECT_TO_PLACE[index2][0]
        e2_high = self.__OBJECT_TO_PLACE[index2][1]
        nbConflict = 0
        for x in xrange(e1_width):
            for y in xrange(e1_high):
                x_anchor = e1_x_anchor + x
                y_anchor = e1_y_anchor - y
                if self.__canTouch:
                    if x_anchor < e2_x_anchor + e2_width and\
                       x_anchor + 1 > e2_x_anchor and\
                       y_anchor > e2_y_anchor - e2_high and\
                       y_anchor - 1 < e2_y_anchor:
                        nbConflict += 1
                else:
                    if x_anchor <= e2_x_anchor + e2_width and\
                       x_anchor + 1 >= e2_x_anchor and\
                       y_anchor >= e2_y_anchor - e2_high and\
                       y_anchor - 1 <= e2_y_anchor:
                        nbConflict += 1
        return nbConflict
    
    def duplicate(self):
        newInd = self.__class__()
        newInd.__positions = []
        for pos in self.__positions:
            newInd.__positions.append((pos[0], pos[1]))
        return newInd
    
    def isBetter(self, otherIndiv, population):
        return self.getFitness() < otherIndiv.getFitness()
    
    @classmethod
    def crossover(cls, parent1, parent2):
        newInd1 = parent1.duplicate()
        newInd2 = parent2.duplicate()
        
        nbExchanged = random.randint(0, len(newInd1.__positions)-1)
        exchangedIndexes = random.sample(xrange(len(newInd1.__positions)), nbExchanged)
        
        for i in exchangedIndexes:
            newInd1.__positions[i] = (parent2.__positions[i][0], parent2.__positions[i][1])
            newInd2.__positions[i] = (parent1.__positions[i][0], parent1.__positions[i][1])

        return [newInd1, newInd2]
    
    def distance(self, otherInd, population):
        dist = 0.0
        for ip, pos in enumerate(self.__positions):
            d = sqrt((pos[0]-otherInd.__positions[ip][0])**2+(pos[1]-otherInd.__positions[ip][1])**2)
            dist += d
        return dist
    
    @classmethod
    def mutation(cls, indiv):
        newInd = indiv.duplicate()
        if random.random() < 0.5:
            nbMuted = random.randint(0, len(newInd.__positions)-1)
            mutedIndexes = []
            if random.random() < 0.5:
                for ip1 in xrange(len(newInd.__positions)):
                    for ip2 in xrange(len(newInd.__positions)):
                        if ip2 > ip1:
                            nbConflict = newInd.__conflict(ip1, ip2)
                            if nbConflict > 0:
                                if len(mutedIndexes) < nbMuted:
                                    if random.random() < 0.5:
                                        mutedIndexes.append(ip1)
                                    else:
                                        mutedIndexes.append(ip2)
            while len(mutedIndexes) < nbMuted:
                ind = random.randint(0, len(newInd.__positions)-1)
                if ind not in mutedIndexes:
                    mutedIndexes.append(ind)
            for i in mutedIndexes:
                newX = newInd.__positions[i][0]
                newY = newInd.__positions[i][1]
                r = random.random()
                if r <= 0.3:
                    newX, _ = newInd.__generateAnchor(i)
                elif r <= 0.6:
                    _, newY = newInd.__generateAnchor(i)
                else:
                    newX, newY = newInd.__generateAnchor(i)
                newInd.__positions[i] = (newX, newY)
        else:
            outSide = True
            while outSide:
                exchanged = random.sample(xrange(len(newInd.__positions)), 2)
                tmpPos = newInd.__positions[exchanged[0]]
                tmpPos2 = newInd.__positions[exchanged[1]]
                outSide = newInd.__isOutOfSpace(exchanged[0], (tmpPos2[0], tmpPos2[1])) or\
                          newInd.__isOutOfSpace(exchanged[1], (tmpPos[0], tmpPos[1]))
                if not outSide:
                    newInd.__positions[exchanged[0]] = (tmpPos2[0], tmpPos2[1])
                    newInd.__positions[exchanged[1]] = (tmpPos[0], tmpPos[1])
        return newInd
    
    def __str__(self):
        return str(self.getFitness()) + " - " + str(self.__positions) 
    
    def __isOnFreeCase(self, index, anchor):
        colide = False
        for ieq, eq in enumerate(self.__positions):
            if ieq != index:
                e_x_anchor = eq[0]
                e_y_anchor = eq[1]
                e_width = self.__OBJECT_TO_PLACE[ieq][0]
                e_high = self.__OBJECT_TO_PLACE[ieq][1]
                x_anchor = anchor[0]
                y_anchor = anchor[1]
                high = 1
                width = 1
                if self.__canTouch:
                    if e_x_anchor < x_anchor + width and\
                       e_x_anchor + e_width > x_anchor and\
                       e_y_anchor > y_anchor - high and\
                       e_y_anchor - e_high < y_anchor:
                        colide = True
        return not colide
    
    def __generateAnchor(self, index):
        anchor = (random.randint(1, self.__SPACE_MATRIX[0]),
                  random.randint(1, self.__SPACE_MATRIX[1]))
        i = 0
        nbTry = 100
        while i < nbTry and (self.__isOutOfSpace(index, anchor) or not self.__isOnFreeCase(index, anchor)):
            anchor = (random.randint(1, self.__SPACE_MATRIX[0]),
                      random.randint(1, self.__SPACE_MATRIX[1]))
            i += 1
        if i == 100:
            print "Could not find free anchor."
        return anchor
        