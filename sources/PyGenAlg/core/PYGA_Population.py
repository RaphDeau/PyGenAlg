# -*- mode: python; py-indent-offset: 4; tab-width: 4; coding: iso-8859-1 -*-

#######################################################################
# Author: Deau Raphaël
#
# Copyright 2011 - 2016
# License: Creative Commons Attribution Non-commercial 4.0
# Full text: https://creativecommons.org/licenses/by-nc/4.0/legalcode
#
#######################################################################

#-----------------------
#
# Start date: 18/07/2011
#
#-----------------------

# - Build-in imports -
import os, random

from multiprocessing import Pipe

from PyGenAlg.core.PYGA_Exceptions import PYGA_PopulationError

class PYGA_Population:
   
    # ==================
    # v Public methods v
    # ==================

    # ----------------------
    # Public - Constructor
    def __init__(self, IndividualClass, behaviorInstance, debugMode, outputPrint):
        self.__individuals = []
        self.__uncatchedIndividuals = []
        self.__debugMode = debugMode
        self._outputPrint = outputPrint
        
        self.__behaviorInstance = behaviorInstance
        
        self.__individualClass = IndividualClass
    # Public - End of Constructor
    # ----------------------

    # ----------------------
    # Private - Generate initial population
    def __generateInitPop(self, nbIndividuals, noDuplication=False, infoStr=''):
        self.__individuals = []
        self.__uncatchedIndividuals = []
        while len(self.__individuals) < nbIndividuals:
            newInd = self.__individualClass.generate()
            add= True
            if noDuplication:
                i = 0
                while add and i < len(self.__individuals):
                    indiv = self.__individuals[i]
                    if newInd.isDuplication(indiv):
                        add=False
                    i += 1
            if add:
                self.__uncatchedIndividuals.append(newInd)
                self.__individuals.append(newInd)
                infoStr2 = infoStr + ' Initialisation: ' + str(len(self.__individuals)) + '/'+str(nbIndividuals)+' generated.'
                self._outputPrint.write(infoStr2)
                self._outputPrint.flush()
    # Private - End of Generate initial population
    # ----------------------


    # ----------------------
    # Public - Generate initial population
    def generateInitPop(self, nbIndividuals, noDuplication=False, 
                        maxProcess=1, infoStr=''):
        #TODO: multiprocess
        self.__generateInitPop(nbIndividuals, noDuplication, infoStr)
    # Public - End of Generate initial population
    # ----------------------

    # ----------------------
    # Public - Add individual
    def addIndividual(self, individual):
        self.__individuals.append(individual)
        self.__uncatchedIndividuals.append(individual)
    # ----------------------

    # ----------------------
    # Public - Remove individual
    def removeIndividual(self, individual):
        iInd = -1
        # Look for the individual. 
        # WARNING: "self.__individuals.index(individual)" not working.
        for i, indiv in enumerate(self.__individuals):
            if indiv is individual:
                iInd = i
        if iInd == -1:
            raise PYGA_PopulationError, 'ERROR: cannot remove individual from the population (individual not found).'
        self.__individuals.pop(iInd)
        try:
            iInd = self.__uncatchedIndividuals.index(individual)
            self.__uncatchedIndividuals.pop(iInd)
        except:
            pass
    # Public - End of Remove individual
    # ----------------------

    # ----------------------
    # Public - Size
    def size(self):
        return len(self.__individuals)
    # ----------------------

    # ----------------------
    # Public - Save population
    def savePopulation(self, fileName):
        # 1- Check fileName
        if type(fileName) != type(''):
            error = 'ERROR: population save file must be a string.\n'
            raise PYGA_PopulationError, error
        # 2- Write number of individuals
        fid = open(fileName, 'w')
        fid.write(str(len(self.__individuals)) + '\n')
        # 3- Write each individual
        for indiv in self.__individuals:
            indiv.saveIndividual(fid)
        fid.close()
    # ----------------------

    # ----------------------
    # Public - Load population
    def loadPopulation(self, fileName):
        # 1- Check fileName
        if fileName is None or not os.path.isfile(fileName):
            error = 'ERROR: population file '+str(fileName)+' is not an existing file.\n'
            raise PYGA_PopulationError, error
        # 2- Empty current population
        while len(self.__individuals) > 0:
            self.remove(self.__individuals[0])
        # 3- Read number of individuals
        fid = open(fileName, 'r')
        nbInd = eval(fid.readline())
        # 4- Write each individual
        for _ in xrange(nbInd):
            indiv = self.__individualClass.loadIndividual(fid)
            self.addIndividual(indiv)
        fid.close()
    # ----------------------
    
    def parsePopulation(self, population):
        # TODO: Check pop size
        for indiv in population:
            indiv, setFitness = self.__individualClass.parseIndividual(indiv)
            self.addIndividual(indiv)
            if setFitness:
                indiv.computeObjectives(self)
    
    # ----------------------
    # Public - Duplicate
    def duplicate(self):
        newPop = self.__class__(self.__individualClass, self.__behaviorInstance, self.__debugMode, self._outputPrint)
        newPop.__individuals = list(self.__individuals)
        newPop.__uncatchedIndividuals = list(self.__individuals)
        return newPop
    # ----------------------

    # ----------------------
    # Public - Merge
    def merge(self, population, duplicate=False):
        for individual in population:
            self.__individuals.append(individual)
            self.__uncatchedIndividuals.append(individual)
    # ----------------------

    def getDuplicationPercent(self):
        nbDupl = 0
        i1 = 0
        nbIndiv = len(self.__individuals)
        while i1 < nbIndiv:
            dupl = False
            indiv1 = self.__individuals[i1]
            i2 = i1+1
            while not dupl and i2 < nbIndiv:
                indiv2 = self.__individuals[i2]
                if indiv1.isDuplication(indiv2):
                    nbDupl += 1
                    dupl = True
                i2 += 1
            i1 += 1
        duplPercent = nbDupl*100/nbIndiv
        return duplPercent

    def getClusters(self, inflDist):
        clusters = [[self.__individuals[0]]]
        clusteredIndiv = [0]
        indivToTreat = [self.__individuals[0]]
        # Do it until all individual have been classified
        while len(clusteredIndiv) < len(self.__individuals):
            # Treat each point of the neighborhood to get chains of indiv
            while len(indivToTreat) > 0:
                currentTreatedIndiv = indivToTreat.pop(0)
                for i, indiv in enumerate(self.__individuals):
                    if i not in clusteredIndiv:
                        if currentTreatedIndiv.distance(indiv, self) <= inflDist:
                            clusters[-1].append(indiv)
                            clusteredIndiv.append(i)
                            indivToTreat.append(indiv)
            # One cluster has been found, if some individual have not been treated
            # get one random and find another chain starting from it
            if len(clusteredIndiv) < len(self.__individuals):
                clusters.append([])
                seedIndiv = 0
                while seedIndiv < len(self.__individuals) and seedIndiv in clusteredIndiv:
                    seedIndiv += 1
                clusters[-1].append(self.__individuals[seedIndiv])
                clusteredIndiv.append(seedIndiv)
                indivToTreat = [self.__individuals[seedIndiv]]
        return clusters
    
    def removeRandomIndiv(self, nbIndiv):
        indivs = random.sample(self.__individuals, nbIndiv)
        for indiv in indivs:
            self.removeIndividual(indiv)
            
    # ----------------------
    # Public - Get random parents
    def getRandomParents(self, biasSelectionMethod, useTwice=True):
        # 1- Check size of the population (need at least 2 individuals to cross...)
        if len(self.__individuals) < 2:
            error = 'At least TWO parents are needed to proceed to crossover.\n'
            error += 'Please change crossover/mutation rates or population size.'
            raise PYGA_PopulationError, 'ERROR: ' + error

        # 2- Get the right list to find parents
        indList = self.__individuals
        parent1 = None
        if not useTwice:
            # Get parents in "uncatched" list
            if len(self.__uncatchedIndividuals) > 1:
                indList = self.__uncatchedIndividuals
            elif len(self.__uncatchedIndividuals) == 1:
                # If only one parent uncatched, take it and pick another randomly
                parent1 = self.__uncatchedIndividuals[0]
        
        # 3- Get random parents
        if parent1 is None:
            [parent1, parent2] = biasSelectionMethod(indList,2)            
        else:
            # Pick second parent randomly
            parent2 = parent1
            while parent2 == parent1:
                parent2 = biasSelectionMethod(indList, 1)[0]
        
        # 4- Update the list of catched parents
        try:
            iInd = self.__uncatchedIndividuals.index(parent1)
            self.__uncatchedIndividuals.pop(iInd)
        except:
            pass
        try:
            iInd = self.__uncatchedIndividuals.index(parent2)
            self.__uncatchedIndividuals.pop(iInd)
        except:
            pass

        # 5- If all individuals have been chosen at least one time, reset uncatched list
        if len(self.__uncatchedIndividuals) == 0:
            self.__uncatchedIndividuals = list(self.__individuals)

        return (parent1, parent2)
    # Public - End of Get random parents
    # ----------------------

    # ----------------------
    # Public - Get random individual
    def getRandomIndividual(self, biasSelectionMethod):
        return biasSelectionMethod(self.__individuals, 1)[0]
    # ----------------------

    # ----------------------
    # Public - Get best individual
    def getBestIndividual(self, nbBest=1):
        if nbBest <= 0:
            nbBest = 1
        bestInd = None
        if nbBest == 1:
            if self.__individualClass.MULTI_OBJ:
                bestInd = self.__individualClass.getBestIndividuals(self)
            else:
                for individual in self.__individuals:
                    if bestInd is None or self.__individualClass.isBetter(individual, 
                                                                          bestInd,
                                                                          self):
                        bestInd = individual
        else:
            if self.__individualClass.MULTI_OBJ:
                print("More than 1 best individual not supported for now.")
                bestInd = self.__individualClass.getBestIndividuals(self)
            else:
                sortedPop = []
                for indiv in self:
                    added = False
                    for i, curInd in enumerate(sortedPop):
                        if indiv.isBetter(curInd, self) and not added:
                            sortedPop.insert(i, indiv)
                            added = True
                    if not added:
                        sortedPop.append(indiv)
                bestInd = sortedPop[:nbBest]
        return bestInd
    
    # Public - End of Get best individual
    # ----------------------
    
    # ----------------------
    # Public - Compute the objective of all individuals
    def computeObjectives(self, infoStr):
        nbIndivToComp = 0
        for indiv in self.__individuals:
            if indiv.needCompute():
                nbIndivToComp += 1
        # 1- Non parallel computing
        if self.__behaviorInstance.getParam(self.__behaviorInstance.MAX_PROCESS_LABEL) == 1:
            nbIndivEvaluated = 0
            for indiv in self.__individuals:
                infoStr2 = infoStr + ' Evaluated individuals: ' + str(nbIndivEvaluated) + '/' + str(nbIndivToComp)
                self._outputPrint.write(infoStr2)
                self._outputPrint.flush()
                if indiv.computeObjectives(self):
                    nbIndivEvaluated += 1
                infoStr2 = infoStr + ' Evaluated individuals: ' + str(nbIndivEvaluated) + '/' + str(nbIndivToComp)
                self._outputPrint.write(infoStr2)
                self._outputPrint.flush()
        # 2- Parallel computing
        else:
            # 2.1- Store process list and pipes
            processList = []
            parentPipe = []
            # 2.2- Get max simultaneous process
            max_proc = self.__behaviorInstance.getParam(self.__behaviorInstance.MAX_PROCESS_LABEL)
            # 2.3- Treat each individual
            nbIndivLaunched = 0
            nbIndivDone = 0
            for indivID, indiv in enumerate(self.__individuals):
                # 2.3.1- Create a specific pipe for this individual
                pipe_parent, pipe_child = Pipe(False)
                parentPipe.append(pipe_parent)
                # 2.3.2- If simultaneous process are limited and reached, wait...
                while max_proc != 0 and len(processList) == max_proc:
                    i = 0
                    while i < len(processList):
                        if not self.__checkProcessEnd(i, parentPipe, processList):
                            i += 1
                        else:
                            nbIndivDone += 1
                # 2.3.3- A new computation can be launched simultaneously with others
                if indiv.computeObjectives(self, processList, pipe_child, indivID):
                    nbIndivLaunched += 1
                infoStr2 = infoStr + ' Evaluating individuals: ' + str(nbIndivLaunched) + '/' + str(nbIndivToComp) + ' launched, '
                infoStr3 = infoStr2 + str(nbIndivDone) + ' Done.    '
                self._outputPrint.write(infoStr3)
                self._outputPrint.flush()
                
            # 2.4- Wait for computing obectives
            i = 0
            infoStr3 = infoStr2 + str(nbIndivDone) + ' Done.     '
            self._outputPrint.write(infoStr3)
            self._outputPrint.flush()
            while len(processList) > 0:
                if not self.__checkProcessEnd(i, parentPipe, processList):
                    i += 1
                else:
                    nbIndivDone += 1
                    infoStr3 = infoStr2 + str(nbIndivDone) + ' Done.    '
                    self._outputPrint.write(infoStr3)
                    self._outputPrint.flush()
                if i != 0:
                    i = i%(len(processList))

        # 3- For multi obj, call fitness function (obj have been computed)
        if self.__individualClass.MULTI_OBJ:
            self.__individualClass.computeMultiObjFitness(self)
    # Public - End of Get bet individual
    # ----------------------

    # ==================
    # ^ Public methods ^
    # ==================

    # =====================
    # v Specifics methods v
    # =====================

    def __checkProcessEnd(self, processNum, parentPipe, processList):
        terminated = False
        # poll() check if any data is available in the pipe
        if parentPipe[processNum].poll():
            # Get the new individual (with computed objectives)
            try:
                [indiv, indivId] = parentPipe[processNum].recv()
                self.__individuals[indivId] = indiv
            except:
                pass
            # Close pipe and process
            parentPipe[processNum].close()
            parentPipe.pop(processNum)
            proc = processList[processNum]
            proc.join()
            processList.pop(processNum)
            terminated = True

        return terminated
    # =====================
    # ^ Specifics methods ^
    # =====================


    # =========================
    # v Operators overloading v
    # =========================

    # ----------------------
    # Operator "del"
    def __del__(self):
        for ind in self.__individuals:
            del ind
        self.__uncatchedIndividuals = []
        self.__individualClass = None
    # ----------------------

    # ----------------------
    # Operator "+"
    def __add__(self, population):
        newPop = self.duplicate()
        newPop.merge(population)
        return newPop
    # ----------------------

    # ----------------------
    # Operator "in"
    def __contains__(self, key):
        return key in self.__individuals
    # ----------------------

    # ----------------------
    # Operator "for .. in .."
    def __iter__(self):
        return self.__individuals.__iter__()
    # ----------------------

    # ----------------------
    # Operator "[]"
    def __getitem__(self, i):
        return self.__individuals[i]
    # ----------------------
    

    # ----------------------
    # Operator "str"
    def __str__(self):
        s = ''
        for individual in self.__individuals:
            si = str(individual)
            if si != '':
                s += si + '\n'
        return s
    # ----------------------

    # =========================
    # ^ Operators overloading ^
    # =========================
