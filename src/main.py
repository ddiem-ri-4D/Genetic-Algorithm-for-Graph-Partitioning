import networkx as nx
import random as rd
from functools import partial
import time
import sys
import copy
from utils import genPopulation, initGraph
from operation import multiCrossover, mutation, tournament, multiCrossover # , singleCrossover
from evaluation import getCutsize, fitness

# Parameters; global variables
POP_SIZE = 300
NUM_NODES = 100  # SHOULD BE AN EVEN NUMBER !!!
CONNECT_PROB = 0.1
MUT_PROB = 0.3
STOPPING_COUNT = 10
K_IND = int(POP_SIZE * 0.1)  # tournament size: K individual

# MAIN
def main():
    start_time = time.time()

    """
    Generate random graph
    1) initGraph(NUM_NODES, CONNECT_PROB)
    2) nx.gnp_random_graph from networkX library
    """
    g = initGraph(NUM_NODES, CONNECT_PROB)
    print(">>> Graph Info (Node, Edge) : ", len(g.nodes()), len(g.edges()))
    #g = nx.gnp_random_graph(NUM_NODES, 0.6)

    # draw current graph
    # nx.draw(g)

    # Generate population
    pop = genPopulation(NUM_NODES, POP_SIZE)

    # Variables to keep best values
    bestSoFar = sys.maxsize
    bestCutSize = sys.maxsize
    bestPartition = []
    
    bestCut, worstCut = getCutsize(pop, g)
    eval_with = partial(fitness, worstCut, bestCut, g)

    initialCut = bestCut

    sortedPop = copy.deepcopy(sorted(pop, key=eval_with, reverse=True))
    pop = copy.deepcopy(sortedPop)

    genCount = 1
    improveCount = 0

    # Genetic algorithm
    while improveCount < STOPPING_COUNT:
        print("==================================================")
        print("Generation : ", genCount)
        print("Elapsed Time : ", time.time() - start_time)
        print("Population Size : ", len(pop))

        genCount = genCount + 1

        # fitness (low is good)
        currentFit, currentCut = fitness(worstCut, bestCut, g, pop[0])

        # Update best-so-far
        if currentFit < bestSoFar:
            improveCount = 0
            bestSoFar = currentFit
            bestCutSize = currentCut
            bestPartition = pop[0]

            print("--------------------------------------------------")
            print("Best So Far (Fitness) : ", bestSoFar)
            print("Best Cut Size : ", bestCutSize)
            print("Best Partition : ", bestPartition)            

        # No improvement
        else:
            improveCount += 1

        nextPop = copy.deepcopy(pop)

        # Crossover
        for idx in range(int(POP_SIZE / 2)):
            parent1, parent2 = tournament(pop, bestCut, worstCut, g, K_IND)
            
            offspring1, offspring2 = multiCrossover(parent1, parent2)
            # offspring1, offspring2 = singleCrossover(parent1, parent2)

            if (offspring1 not in nextPop) and (offspring1.count(0) == (NUM_NODES/2)):
                nextPop.append(offspring1)
            if (offspring2 not in nextPop) and (offspring2.count(0) == (NUM_NODES/2)):
                nextPop.append(offspring2)


        # Mutation
        for idx in range(len(nextPop)):
            randomProb = rd.random()
            if randomProb < MUT_PROB:
                mutInd = mutation(nextPop[idx])
                if mutInd not in nextPop:
                    nextPop.append(mutInd)

        # Update eval_with
        bestCut, worstCut = getCutsize(pop, g)
        eval_with = partial(fitness, worstCut, bestCut, g)

        pop = copy.deepcopy(sorted(nextPop, key=eval_with, reverse=True))
        pop = pop[:POP_SIZE]

    # Print summary of GA
    print("----------SUMMARY----------")
    print("Total Elapsed Time : ", time.time() - start_time)
    print("Generation Count: ", genCount)
    print("Best Fitness : ", bestSoFar)
    print("Best Partition : ", bestPartition)
    print("---------------------------")
    print("Initial Cut Size : ", initialCut)
    print("Final (Best) Cut Size : ", bestCutSize)

if __name__ == "__main__":
    main()
