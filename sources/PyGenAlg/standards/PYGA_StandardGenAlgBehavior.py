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
# Start date: 20/07/2011
#
#-----------------------

# - build-in imports -
from PyGenAlg.core.PYGA_Exceptions import PYGA_BehaviorAddMethodError, PYGA_FitnessComputation
from PyGenAlg.core.PYGA_GenAlgBehavior import PYGA_GenAlgBehavior
import os
import random
import time

from sys import version_info
if version_info[0] >= 3:
    xrange = range

# - local imports -

class PYGA_StandardGenAlgBehavior(PYGA_GenAlgBehavior):
    
    standardsParamFileName = "standardParameters.xml"
    standardsParamsFile = os.path.join(os.path.dirname(os.path.abspath(__file__)), standardsParamFileName)
    PYGA_GenAlgBehavior.addParamFile(standardsParamsFile)
    
    def __init__(self, *args, **kwargs):
        PYGA_GenAlgBehavior.__init__(self, *args, **kwargs)
        
    # ======================
    # v Overloaded methods v
    # ======================

    def setParameter(self, paramName, value):
        PYGA_GenAlgBehavior.setParameters(self, **{paramName: value})

    def setParameters(self, **kwargs):
        PYGA_GenAlgBehavior.setParameters(self, **kwargs)
        self.__updateOptimizedParams()
        
    def __updateOptimizedParams(self):
        for param in self.getParam(self.SELF_OPTIMIZED_PARAMETERS_LABEL):
            paramLabel = self.getParamFromKeyword(param)
            paramNoneValue = eval("self."+paramLabel.upper()+"_NONE_VALUE")
            PYGA_GenAlgBehavior.setParameters(self, **{paramLabel:paramNoneValue})

    # ------------------------
    # Public - Init population
    def initPopulation(self, population, infoStr):
        popFile = self.getParam(self.POP_FILE_LABEL)
        popArg = self.getParam(self.INIT_POP_LABEL)
        if popFile != self.POP_FILE_NONE_VALUE:
            population.loadPopulation(popFile)
            infoStr2 = infoStr + ' Population loaded: ' + str(population.size()) + ' individuals.\n'
            self.printLog(infoStr2)
        elif popArg != self.INIT_POP_NONE_VALUE:
            population.parsePopulation(popArg)
            infoStr2 = infoStr + ' Population set: ' + str(population.size()) + ' individuals.\n'
            self.printLog(infoStr2)
        else:
            population.generateInitPop(self.getParam(self.POPULATION_SIZE_LABEL),
                                       self.getParam(self.DEL_DUPLICATED_INDIV_LABEL),
                                       self.getParam(self.MAX_PROCESS_LABEL), 
                                       infoStr)
            infoStr2 = infoStr + ' Population generated: ' + str(population.size()) + ' individuals.\n'
            self.printLog(infoStr2)
        if population.size() < self.getParam(self.POPULATION_SIZE_LABEL):
            infoStr2 = infoStr + ' Population loaded too small. Generating ' + str(self.getPopSize() - population.size()) + ' individuals.\n'
            self.printLog(infoStr2)
        while population.size() < self.getParam(self.POPULATION_SIZE_LABEL):
            population.addIndividual(self.getIndividualClass().generate())
        
    # ------------------------

    # ----------------------
    # Public - stop criteria
    def stopCriteria(self, population, iGeneration, startTime, infoStr):
        # May be changed in derived class
        # 1- Store the output
        stop = False
        percent = 0

        # 2- Check time criterion
        endTime = self.getParam(self.END_TIME_LABEL)
        if endTime != 0:
            timeDiff = time.time() - startTime
            percent = int(100 * timeDiff / endTime)
            if timeDiff >= endTime:
                stop = True

        # 3- Check number of generation
        nbGen = self.getParam(self.NB_GENERATIONS_LABEL)
        if nbGen != 0:
            genPercent = int(100 * iGeneration / nbGen)
            if genPercent > percent:
                percent = genPercent
            if iGeneration == nbGen:
                stop = True

        return percent, stop
    # ----------------------

    # ----------------------------
    # Public - start of generation
    def startOfGeneration(self, population, iGeneration, infoStr):
        pass # Do nothing, may be changed in derived class
    # ----------------------------

    # --------------------------
    # Public - end of generation
    def endOfGeneration(self, population, iGeneration, endOfRun, infoStr):
        pass # Do nothing, may be changed in derived class
    # --------------------------

    # ------------------
    # Public - Selection
    def selection(self, population, infoStr):
        # 1- Get the selection method to use
        selectionName = self.getParam(self.SELECTION_LABEL)
        selectionMethod = eval('self.' + self.SELECTION_DICT[selectionName])

        ps = population.size()
        # 2- Get the number of crossed individual of the end population
        crossRate = self.getParam(self.CROSSOVER_LABEL)
        nbCross = int(round(crossRate*ps/100.))
        # 3- Get the number of mutated individual of the end population
        muteRate = self.getParam(self.MUTATION_LABEL)
        nbMut = int(round(muteRate*ps/100.))
        # 4- Get the number of individuals to select
        nbToSelect = ps - nbCross - nbMut
        selectedPopulation = selectionMethod(population, nbToSelect)
        return selectedPopulation 
    # Public - End of Selection
    # ----------------------
        
    # ----------------------
    # Public - Reproduction
    def reproduction(self, population, selectedPopulation, infoStr):
        self.printLog('PYGA_StandaradGenAlgBehavior / reproduction - input\n', debug=True)
        ps = population.size()
        # 1- Get the population to consider (whole or selected only)
        if self.getParam(self.REPRODUCE_SELECTED_ONLY_LABEL):
            currentPop = selectedPopulation
        else:
            currentPop = population
        self.printLog('PYGA_StandaradGenAlgBehavior / reproduction - Population chosen\n', debug=True)
        # 2- Get the number of crossed/mutated individual in the end population
        crossRate = self.getParam(self.CROSSOVER_LABEL)
        nbCrossedInd = int(round(ps * crossRate / 100.))
        muteRate = self.getParam(self.MUTATION_LABEL)
        nbMutatedInd = int(round(ps * muteRate / 100.))
        # 3- Reproduction process...
        # Keep the entire population to check duplication
        newPop = selectedPopulation
        self.printLog('PYGA_StandaradGenAlgBehavior / reproduction - Crossing\n', debug=True)
        crossedPopulation = self.crossover(currentPop, nbCrossedInd, newPop, infoStr)
        newPop += crossedPopulation
        self.printLog('PYGA_StandaradGenAlgBehavior / reproduction - Muting\n', debug=True)
        mutatedPopulation = self.mutation(currentPop, nbMutatedInd, newPop, infoStr)
        reproducedPopulation = mutatedPopulation + crossedPopulation
        self.printLog('PYGA_StandaradGenAlgBehavior / reproduction - Reproduction done\n', debug=True)
        return reproducedPopulation
    # Public - End of Reproduction
    # ----------------------
        
    def biasCrossoverSelection(self, individuals, nbToSelect):
        # Default: random selection
        return random.sample(individuals, nbToSelect)
    
    def biasMutationSelection(self, individuals, nbToSelect):
        # Default: random selection
        return random.sample(individuals, nbToSelect)
        
    # ----------------------
    # Public - Crossover
    def crossover(self, population, nbCrossInd, newPop, infoStr):
        # 1- Create the new population
        # -- It will contain only all individuals generated by crossover
        crossedPopulation = self.createPopulation()
        crossOnce = self.getParam(self.CROSS_ONCE_LABEL)
        del_duplicated = self.getParam(self.DEL_DUPLICATED_INDIV_LABEL)
        # 2- Generate enough individuals
        while crossedPopulation.size() < nbCrossInd:
            duplicated = True
            nbTry = 0
            nbTryMax = self.getParam(self.DEL_DUPL_NB_TRY_LABEL)
            while duplicated and nbTry < nbTryMax:
                nbTry += 1
                # 2.1- Get the parents to cross
                parents = population.getRandomParents(self.biasCrossoverSelection,
                                                      useTwice=(not crossOnce))
                while not self.getIndividualClass().canBeCrossed(parents[0], parents[1]):
                    parents = population.getRandomParents(self.biasCrossoverSelection,
                                                          useTwice=(not crossOnce))
                # 2.2- Call cross method from individual class
                crossResult = self.getIndividualClass().crossover(parents[0], parents[1])
                if type(crossResult) != type([]):
                    newIndivs = [crossResult]
                else:
                    newIndivs = crossResult
                duplicated = False
                curIndivIndex = 0
                while not duplicated and curIndivIndex < len(newIndivs):
                    newIndiv = newIndivs[curIndivIndex]
                    if not del_duplicated:
                        crossedPopulation.addIndividual(newIndiv)
                    else:
                        i = 0
                        while not duplicated and i < newPop.size():
                            if newIndiv.isDuplication(newPop[i]):
                                duplicated = True
                            i += 1
                        if not duplicated:
                            i = 0
                            while not duplicated and i < crossedPopulation.size():
                                if newIndiv.isDuplication(crossedPopulation[i]):
                                    duplicated = True
                                i += 1
                        if not duplicated and crossedPopulation.size() < nbCrossInd:
                            crossedPopulation.addIndividual(newIndiv)
                    curIndivIndex += 1
            if duplicated and nbTry == nbTryMax:
                # Duplication cannot be avoided
                # Get the parents to cross
                parents = population.getRandomParents(self.biasCrossoverSelection,
                                                      useTwice=(not crossOnce))
                while not self.getIndividualClass().canBeCrossed(parents[0], parents[1]):
                    parents = population.getRandomParents(self.biasCrossoverSelection,
                                                          useTwice=(not crossOnce))
                # Call cross method from individual class
                crossResult = self.getIndividualClass().crossover(parents[0], parents[1])
                # Store the new individuals
                if type(crossResult) != type([]):
                    newIndivs = [crossResult]
                else:
                    newIndivs = crossResult
                for newIndiv in newIndivs:
                    crossedPopulation.addIndividual(newIndiv)
                infoStr2 = infoStr + " Crossover - Could not avoid duplication."
                self.printLog(infoStr2)
            self.printLog('PYGA_StandaradGenAlgBehavior / crossover - crossedPopulation.size() / nbCrossInd = ' + str(crossedPopulation.size()) + ' / ' + str(nbCrossInd) + '\n', debug=True)
        # Update crossed individual number if needed
        nbIndivMore = crossedPopulation.size() - nbCrossInd 
        if nbIndivMore > 0:
            crossedPopulation.removeRandomIndiv(nbIndivMore)
        return crossedPopulation
    # Public - End of Crossover
    # ----------------------

    # ----------------------
    # Public - Mutation
    def mutation(self, population, nbMutInd, newPop, infoStr):
        # 1- Create the new population
        # -- It will contain only all individuals generated by mutation
        mutatedPopulation = self.createPopulation()
        self.printLog('PYGA_StandaradGenAlgBehavior / mutation - Muted population created\n', debug=True)
        # 2- Generate enought individuals
        while mutatedPopulation.size() < nbMutInd:
            self.printLog('PYGA_StandaradGenAlgBehavior / mutation - Creating new individual\n', debug=True)
            # 2.1- Get the individual to mutate
            individual = population.getRandomIndividual(self.biasMutationSelection)
            while not self.getIndividualClass().canBeMuted(individual):
                self.printLog('PYGA_StandaradGenAlgBehavior / mutation - Indiv cannot be muted, choose another\n', debug=True)
                individual = population.getRandomIndividual(self.biasMutationSelection)
            # 2.2- Call mutation method from individual class
            duplicated = True
            nbTryMax = self.getParam(self.DEL_DUPL_NB_TRY_LABEL)
            nbTry = 0
            while duplicated and nbTry < nbTryMax:
                nbTry += 1
                newIndiv = self.getIndividualClass().mutation(individual)
                self.printLog('PYGA_StandaradGenAlgBehavior / mutation - Checking duplication\n', debug=True)
                duplicated = False
                if self.getParam(self.DEL_DUPLICATED_INDIV_LABEL):
                    for indiv in newPop:
                        if newIndiv.isDuplication(indiv):
                            duplicated = True
                            break 
                        if not duplicated:
                            for indiv in mutatedPopulation:
                                if newIndiv.isDuplication(indiv):
                                    duplicated = True
                                    break
            if duplicated and nbTry == nbTryMax:
                # Duplication cannot be avoided
                infoStr2 = infoStr + " Mutation - Could not avoid duplication."
                self.printLog(infoStr2)
            self.printLog('PYGA_StandaradGenAlgBehavior / mutation - Individual valid, add it to population\n', debug=True)
            mutatedPopulation.addIndividual(newIndiv)
        nbIndivMore = mutatedPopulation.size() - nbMutInd
        if nbIndivMore > 0:
            mutatedPopulation.removeRandomIndiv(nbIndivMore)
        return mutatedPopulation
    # Public - End of Mutation
    # ----------------------

    def selfOptimize(self, population, iGen, infoStr):
        for param in self.getParam(self.SELF_OPTIMIZED_PARAMETERS_LABEL):
            paramLabel = self.getParamFromKeyword(param)
            eval("self."+eval("self."+paramLabel.upper()+"_OPTIMIZE_METHOD"))(population, iGen, infoStr)
        
    def optimizeInflDist(self, population, iGen, infoStr):
        newInflDist = self.getParam(self.DIST_INFLUENCE_LABEL)
        if iGen == 0:
            # Try to have maximum diversity:
            searchSpaceSize, dim = self.getIndividualClass()().individualSearchSpaceInfo()
            maxClusterSize = searchSpaceSize / population.size()
            # This distance will cover maximum space search
            newInflDist = pow(maxClusterSize, 1.0/dim)
        else:
            clusters = population.getClusters(newInflDist)
            sm, sM = self.getParam(self.NB_CLUSTER_INFLUENCE_LABEL)
            if len(clusters) >= sm and len(clusters) <= sM:
                minDist = newInflDist
                indivPerCluster = []
                for cluster in clusters:
                    indivPerCluster.append(len(cluster))
                    for indiv1 in cluster:
                        for indiv2 in cluster:
                            if indiv1 is not indiv2 and indiv1.distance(indiv2, self) < minDist:
                                minDist = indiv1.distance(indiv2, self)
                reduceInflDist = True
                minInd = population.size() / sM
                minInd = minInd - minInd/10
                for nbInd in indivPerCluster:
                    if nbInd < minInd:
                        reduceInflDist = False
                if reduceInflDist:
                    newInflDist = minDist + (newInflDist - minDist)/2.0
        # TODO: Distance according to convergence
        infoStr2 = infoStr + ' Optimizing influence distance: ' + unicode(newInflDist) + "."
        self.printLog(infoStr2)
        PYGA_GenAlgBehavior.setParameters(self, **{"infl_dist":newInflDist})
        
    def optimizeCrossover(self, population, iGen, infoStr):
        authorizedDuplPercent = 20
        duplPercent = population.getDuplicationPercent()
        if duplPercent > authorizedDuplPercent:
            # Specific case: lot of duplicated individuals --> crossover = 0
            newCrossValue = 0
            infoStr2 = infoStr + ' Optimizing crossover rate: ' + unicode(newCrossValue) + " (Too many duplication: "+unicode(duplPercent)+"%)."
            self.printLog(infoStr2)
        else:
            clusters = population.getClusters(self.getParam(self.DIST_INFLUENCE_LABEL))
            # TODO: Param pour le nombre min de cross/mute ?
            # Consider stability point if nbClust == "number of cluster influence"
            sm, sM = self.getParam(self.NB_CLUSTER_INFLUENCE_LABEL)
            n = len(clusters)
            ps = population.size()
            maxRepro = self.getParam(self.MAX_REPRO_LABEL)
            cm = 10 # min crossover
            cM = maxRepro-cm # max crossover
            cS = int((cM + cm)/2) # Stability crossover
            newCrossValue = cS
            if n < sm:
                newCrossValue = ((cm-cS)*n+(cS-cm*sm))/(1-sm)
            elif n > sM:
                newCrossValue = ((cS-cM)*n+(cM*sM-ps*cS))/(sM-ps)
            # Old method with only min and max, no stability point
            #newCrossValue = len(clusters)*90/(population.size()-1) - 90/(population.size()-1)
            infoStr2 = infoStr + ' Optimizing crossover rate: ' + unicode(newCrossValue) + " ("+unicode(len(clusters))+" clusters)."
            self.printLog(infoStr2)
        PYGA_GenAlgBehavior.setParameters(self, **{"crossrate":newCrossValue})
        
    def optimizeMutation(self, population, iGen, infoStr):
        authorizedDuplPercent = 20
        duplPercent = population.getDuplicationPercent()
        if duplPercent > authorizedDuplPercent:
            newMuteValue = min(90, duplPercent*3)
            infoStr2 = infoStr + ' Optimizing mutation rate: ' + unicode(newMuteValue) + " (Too many duplication: "+unicode(duplPercent)+"%)."
            self.printLog(infoStr2)
        else:
            clusters = population.getClusters(self.getParam(self.DIST_INFLUENCE_LABEL))
            # newMuteValue = a*nbClust²+b*nbClust+c
            # If nbClust == 1 --> mute maximum to explore
            # Consider stability point if nbClust == "number of cluster influence"
            sm, sM = self.getParam(self.NB_CLUSTER_INFLUENCE_LABEL)
            n = len(clusters)
            ps = population.size()
            maxRepro = self.getParam(self.MAX_REPRO_LABEL)
            mm = 10 # min mutation
            mM = maxRepro-mm # max mutation
            mS = int((mM + mm)/2) # Stability crossover
            newMuteValue = mS
            if n < sm:
                newMuteValue = ((mM-mS)*n+(mS-mM*sm))/(1-sm)
            elif n > sM:
                newMuteValue = ((mS-mm)*n+(mm*sM-ps*mS))/(sM-ps)
            # Old method with only min and max, no stability point
            #newMuteValue = -len(clusters)*90/(population.size()-1) + 90*population.size()/(population.size()-1)
    #         if len(clusters) < self.getParam(self.NB_CLUSTER_INFLUENCE_LABEL):
    #             newMuteValue = 60
    #         else:
    #             newMuteValue = 20
            # TODO: Enhance depending on convergence
            infoStr2 = infoStr + ' Optimizing mutation rate: ' + unicode(newMuteValue) + " ("+unicode(len(clusters))+" clusters)."
            self.printLog(infoStr2)
        PYGA_GenAlgBehavior.setParameters(self, **{"mutaterate":newMuteValue})
        
    # ----------------------
    # Public - Optimise
    def optimise(self, population, infoStr):
        self.scaling(population, infoStr)
        self.sharing(population, infoStr)
    # ----------------------

    # ----------------------
    # Public - Sharing
    def sharing(self, population, infoStr):
        sharingName = self.getParam(self.SHARING_LABEL)
        sharingMethod = eval('self.' + self.SHARING_DICT[sharingName])
        shareRate = self.getParam(self.SHARING_RATE_LABEL)
        sharingMethod(population, shareRate)
    # ----------------------

    # ----------------------
    # Public - Scaling
    def scaling(self, population, infoStr):
        scalingName = self.getParam(self.SCALING_LABEL)
        scalingMethod = eval('self.' + self.SCALING_DICT[scalingName])
        scaleRate = self.getParam(self.SCALING_RATE_LABEL)
        scalingMethod(population, scaleRate)
    # ----------------------

    # ======================
    # ^ Overloaded methods ^
    # ======================
        
    @classmethod
    def ADD_METHOD(cls, **kwargs):
        paramWithMethods = []
        for param in cls.ALL_PARAMS:
            upParam = param.upper()
            if hasattr(cls, 'POSSIBLE_' + upParam + '_METHODS'):
                paramWithMethods.append(param)
        
        for key in kwargs.keys():
            if key not in paramWithMethods:
                raise PYGA_BehaviorAddMethodError('ERROR: add_method arguments must be in ' + str(paramWithMethods) + '.')
            if type(kwargs[key]) != type([]) or len(kwargs[key]) != 2:
                raise PYGA_BehaviorAddMethodError('ERROR: add_method arguments must be a list of [methodID, methodName].')

            methodID = kwargs[key][0].upper()
            methodName = kwargs[key][1]
            exec('cls.POSSIBLE_' + key.upper() + '_METHODS.append(\'' + methodID + '\')')
            exec('cls.' + key.upper() + '_DICT[\'' + methodID + '\'] = \'' + methodName + '\'')

    # ==============================
    # v Standard selection methods v
    # ==============================

    # ----------------------
    # Private - Get the highest fitness of the population
    def __getMaxFitness(self, population):
        #if self.__individualClass.MULTI_OBJ:
        #    raise PYGA_FitnessComputation, 'ERROR: Best fitness cannot be computed for multi-objectives individuals...'
        fitMax = None
        for indiv in population:
            if fitMax is None or fitMax < indiv.getFitness():
                fitMax = indiv.getFitness()
        return fitMax
    # Private - End of Get average fitness of the population
    # ----------------------

    # ----------------------
    # Public - "Best" selection
    def bestSelection(self, population, nbIndSelected, noDupl=None):
        # 1- Create the new population
        # -- It will contain only the selected individuals
        bestPop = self.createPopulation()
        if noDupl is None:
            noDupl = self.getParam(self.DEL_DUPLICATED_INDIV_LABEL)
        if nbIndSelected > 0:
            # 1.1- Go trough each individual of the population
            for individual in population:
                if bestPop.size() < nbIndSelected:
                    # 1.1.1.1- Fill the population until the number of 
                    # -------- individuals is reached
                    if noDupl:
                        for indiv in bestPop:
                            if not indiv.isDuplication(individual):
                                bestPop.addIndividual(individual)
                    else:
                        bestPop.addIndividual(individual)
                else:
                    # 1.1.2.1- Population is full
                    # -------- Get the worst individual of the population 
                    worstInd = None
                    for ind in bestPop:
                        if worstInd is None or \
                                self.getIndividualClass().isBetter(worstInd,
                                                                   ind,
                                                                   population):
                            worstInd = ind
                    # 1.1.2.2- Replace it if the current individual is better
                    if self.getIndividualClass().isBetter(individual,
                                                          worstInd,
                                                          population):
                        if noDupl:
                            for indiv in bestPop:
                                if not indiv.isDuplication(individual):
                                    bestPop.removeIndividual(worstInd)
                                    bestPop.addIndividual(individual)
                        else:
                            bestPop.removeIndividual(worstInd)
                            bestPop.addIndividual(individual)
        if bestPop.size() < nbIndSelected:
            # Duplication could not be avoided
            bestPop = self.bestSelection(population, nbIndSelected, False)
        return bestPop
    # Public - End of "Best" selection
    # ----------------------

    # ----------------------
    # Public - "Roulette Wheel" selection
    def rouletteWheelSelection(self, population, nbIndSelected):
        # 1- Create the new population
        # -- It will contain only the selected individuals
        selectedPop = self.createPopulation()
        if nbIndSelected > 0:
            # 1.1- Check the fitness function monotonic
            indiv1 = population[int(random.random() * population.size())]
            fit1 = indiv1.getOptimisedFitness()
            indiv2 = None
            fit2 = fit1
            # Get 2 individuals with different fitness to compare them
            while fit2 == fit1:
                indiv2 = population[random.randint(0, population.size()-1)]
                fit2 = indiv2.getOptimisedFitness()
            fitFunc = 1
            # "isBetter" is given by the Individual creator 
            # so it will give us the order of the individuals
            if indiv1.isBetter(indiv2, population):
                if fit1 < fit2:
                    fitFunc = -1
            else:
                if fit1 > fit2:
                    fitFunc = -1
            # Store the max fitness in case of decreasing function
            maxFit = self.__getMaxFitness(population)
            # 1.2- Get the sum of all fitnesses
            fitSum = 0.0
            for indiv in population:
                indivFit = indiv.getOptimisedFitness()
                # 1.2.1- Consider the fitness function monotony
                # If fitness function is decreasing, the proba to be selected must
                # be inverted (take "(maxFit - fit) / sum" instead of "fit / sum")
                if fitFunc == -1:
                    indivFit = maxFit - indivFit
                fitSum += indivFit
            # 1.3- Compute all propability of each individual
            proba = []
            prevProba = 0.0
            for ip, indiv in enumerate(population):
                indivFit = indiv.getOptimisedFitness()
                # 1.3.1- Consider the fitness function monotony
                if fitFunc == -1:
                    indivFit = maxFit - indivFit
                # 1.3.2- Get the proba of the individual to be choosen 
                # (between 0.0 and 1.0)
                nextProba = prevProba + indivFit / fitSum
                # 1.3.3- Simulate the wheel with a range for each individual
                proba.append([prevProba, nextProba, ip])
                prevProba = nextProba
            # 1.4- Fill the new population
            while selectedPop.size() < nbIndSelected:
                # 1.4.1- Pick a random number between 0.0 and 1.0
                pickedProba = random.random()
                # 1.4.2- Find the corresponding proba in the wheel
                selectedProba = None
                for prob in proba:
                    if pickedProba >= prob[0] and pickedProba < prob[1]:
                        selectedProba = prob
                # 1.4.3- Manage a selected individual
                if selectedProba is not None:
                    # 1.4.3.1- Add the choosen on the new population 
                    selectedPop.addIndividual(population[selectedProba[2]])
                    # 1.4.3.2- Remove it from the eligible list
                    proba.remove(selectedProba)
        return selectedPop
    # Public - End of "Roulette Wheel" selection
    # ----------------------

    # ----------------------
    # Public - "Ranking" selection
    def rankingSelection(self, population, nbIndSelected):
        # 1- Create the new population
        # -- It will contain only the selected individuals
        selectedPop = self.createPopulation()
        if nbIndSelected > 0:
            # 1.1- Sort the population
            sortedPop = []
            for ip, indiv in enumerate(population):
                i = 0
                while i < len(sortedPop) and\
                      indiv.isBetter(sortedPop[i][0], population):
                    i += 1
                sortedPop.insert(i, [indiv, ip])
            # 1.2- Get the sum of all rank (so sum of population size)
            rankSum = sum(xrange(population.size()+1))
            # 1.3- Compute all propability of each individual
            proba = []
            prevProba = 0.0
            for rank, [indiv, ip] in enumerate(sortedPop):
                rank = rank+1
                # 1.3.2- Get the proba of the individual to be choosen 
                # (between 0.0 and 1.0)
                nextProba = prevProba + float(rank) / rankSum
                # 1.3.3- Simulate the wheel with a range for each individual
                proba.append([prevProba, nextProba, ip])
                prevProba = nextProba
            # 1.4- Fill the new population
            while selectedPop.size() < nbIndSelected:
                # 1.4.1- Pick a random number between 0.0 and 1.0
                pickedProba = random.random()
                # 1.4.2- Find the corresponding proba in the wheel
                selectedProba = None
                for prob in proba:
                    if pickedProba >= prob[0] and pickedProba < prob[1]:
                        selectedProba = prob
                # 1.4.3- Manage a selected individual
                if selectedProba is not None:
                    # 1.4.3.1- Add the choosen on the new population 
                    selectedPop.addIndividual(population[selectedProba[2]])
                    # 1.4.3.2- Remove it from the eligible list
                    proba.remove(selectedProba)
        return selectedPop
    # Public - End of "Ranking" selection
    # ----------------------    

    # ==============================
    # ^ Standard selection methods ^
    # ==============================

    # ============================
    # v Standard scaling methods v
    # ============================

    # ----------------------
    # Private - Get average fitness of the population
    def __getAverageFitness(self, population):
        if self.getIndividualClass().MULTI_OBJ:
            raise PYGA_FitnessComputation('ERROR: Average fitness cannot be computed for multi-objectives individuals...')
        fitSum = 0.0
        for indiv in population:
            fitSum += indiv.getFitness()
        return fitSum / population.size()
    # Private - End of Get average fitness of the population
    # ----------------------    

    # ----------------------
    # Public - Linear scaling
    def linearScaling(self, population, scaleRate):
        # Population will be scaled lineraely
        # That means a function such as "ax+b" will be applied on each fitness
        #             f' = af+b
        #
        # a and b must be determined so that the average remains unchanged.
        #     - scaleRate = 0 --> full random exploration (each fitness is the average)
        #     - scaleRate < 1 --> low selection pressure
        #     - scaleRate = 1 --> no selection pressure
        #     - scaleRate > 1 --> strong selection pressure
        if scaleRate != 1.0:
            # 1- Get some usefull variables...
            favg = self.__getAverageFitness(population)
            # 2 - Determine a and b
            a = scaleRate
            b = favg * (1.0 - scaleRate)
            # 3 - Apply the function on each individual
            for indiv in population:
                indiv.setOptimizedFitness(a * indiv.getFitness() + b)
    # Public - End of Linear scaling
    # ----------------------

    # ----------------------
    # Public - Exponential scaling
    def exponentialScaling(self, population, scaleRate):
        # Population will be scaled exponentialy
        # That means a function such as "x^k" will be applied on each fitness
        #             f' = f^scaleRate
        #     - scaleRate = 0 --> full random exploration (each fitness is 1)
        #     - scaleRate < 1 --> low selection pressure
        #     - scaleRate = 1 --> no selection pressure
        #     - scaleRate > 1 --> strong selection pressure
        if scaleRate != 1.0:
            for indiv in population:
                indiv.setOptimizedFitness(indiv.getFitness()**scaleRate)
    # Public - End of Exponential scaling
    # ----------------------

    # ============================
    # ^ Standard scaling methods ^
    # ============================


    # ============================
    # v Standard sharing methods v
    # ============================

    # ----------------------
    # Public - Basic sharing
    def basicSharing(self, population, shareRate):
        # Don't compute sharing if not used (may take time...)
        if shareRate != 0.0:
            # Compute for each individual
            indivNewFit = []
            for indiv in population:
                indivNewFit.append(indiv.getOptimisedFitness())
                # Get the density of the population near the individual
                density = 0.0
                for indiv2 in population:
                    if indiv2 != indiv:
                        # Get the distance with all other individuals
                        dist = indiv.distance(indiv2, population)
                        # If indiv2 is near indiv: consider its influence
                        if dist <= self.getParam(self.DIST_INFLUENCE_LABEL):
                            influence = 1 - (dist / self.getParam(self.DIST_INFLUENCE_LABEL))**shareRate
                        else:
                            influence = 0
                        # density is the sum of each influence
                        density = density + influence
                # Compute the shared fitness
                if density != 0.0:
                    indivNewFit[-1] = indiv.getOptimisedFitness()/density
            # Apply the shared fitness on each individual
            for ip, indiv in enumerate(population):
                indiv.setOptimizedFitness(indivNewFit[ip])
    # Public - End of Basic sharing
    # ----------------------


    # ----------------------
    # Public - Clustered sharing
    def clusteredSharing(self, population, shareRate):
        pass
    # Public - End of Clustered sharing
    # ----------------------

    # ============================
    # ^ Standard sharing methods ^
    # ============================
