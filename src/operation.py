"""
operation.py --- Operators for Genetic Algorithm; generate new offsprings
- tournament: selection operator, tournament selection
- mutation: mutation operator, exchanging indices from each partitions
- singleCrossover: crossover operator, single point crossover
- multiCrossover: crossover operator, multi-point (here 5) crossover
"""

import random as rd
import copy
import sys
from evaluation import fitness


# Selection operator: tournament selection
def tournament(pop, bestCut, worstCut, g, kInd):
    copiedPop = copy.deepcopy(pop)

    # tournament for parent 1
    candidates = rd.choices(copiedPop, k=kInd)
    bestFit = sys.maxsize
    bestIdx = 0

    for idx in range(len(candidates)):
        currentFit, _ = fitness(worstCut, bestCut, g, pop[idx])
        if bestFit < currentFit:
            bestFit = currentFit
            bestIdx = idx

    copiedPop.remove(copiedPop[bestIdx])
    parent1 = copiedPop[bestIdx]

    # tournament for parent 2
    candidates = rd.choices(copiedPop, k=kInd)
    bestFit = sys.maxsize
    bestIdx = 0

    for idx in range(len(candidates)):
        currentFit, _ = fitness(worstCut, bestCut, g, pop[idx])
        if bestFit < currentFit:
            bestFit = currentFit
            bestIdx = idx

    parent2 = copiedPop[bestIdx]

    return parent1, parent2


# Mutation
def mutation(ind):
    mutatedInd = copy.deepcopy(ind)

    part0 = [index for index in range(len(ind)) if mutatedInd[index] == 0]  # partition 0
    part1 = [index for index in range(len(ind)) if mutatedInd[index] == 1]  # partition 1

    mutIdx0 = rd.choice(part0)
    mutIdx1 = rd.choice(part1)

    # swap indices
    mutatedInd[mutIdx0], mutatedInd[mutIdx1] = mutatedInd[mutIdx1], mutatedInd[mutIdx0]

    return mutatedInd


# Single point crossover
def singleCrossover(parent1, parent2):
    pivot = rd.choice(range(len(parent1)))

    offspring1 = parent1[:pivot] + parent2[pivot:]
    offspring2 = parent2[:pivot] + parent1[pivot:]

    return offspring1, offspring2


# Multi-point crossover
def multiCrossover(parent1, parent2):
    pivot = []

    # cut-point: 5
    while len(pivot) <= 5:
        tmp = rd.choice(range(len(parent1)))
        if not tmp in pivot:
            pivot.append(tmp)
    
    # first crossover operator
    offspring1 = parent1[:pivot[0]] + parent2[pivot[0]:pivot[1]] + parent1[pivot[1]:pivot[2]] + parent2[pivot[2]:pivot[3]] + parent1[pivot[3]:pivot[4]] + parent2[pivot[4]:]

    # second crossover operator
    complementParent = [int(not(parent2[i])) for i in range(len(parent2))]
    offspring2 = parent1[:pivot[0]] + complementParent[pivot[0]:pivot[1]] + parent1[pivot[1]:pivot[2]] + complementParent[pivot[2]:pivot[3]] + parent1[pivot[3]:pivot[4]] + complementParent[pivot[4]:]

    return offspring1, offspring2