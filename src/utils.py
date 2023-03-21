"""
utils.py --- Generating initial data
- initGraph: generating initial target graph
- genIndividual: generating each individuals with numNode (=NUM_NODE in main.py)
- genPopulation: generating population with popSize (=POP_SIZE in main.py)
"""

import networkx as nx
import random as rd
from itertools import combinations
import numpy as np


# generate initial random graph (= target graph)
def initGraph(numNode, connectProb):
    nodes = set([n for n in range(numNode)])
    edges = set()
    for combination in combinations(nodes, 2):
        tmp = rd.random()
        if tmp < connectProb:
            edges.add(combination)

    g = nx.Graph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)

    return g


# make two partitions
def genIndividual(numNode):
    ind = []
    while not ind.count(0) == numNode / 2:
        ind = list(np.random.choice([0, 1], size=(numNode,), p=[.5, .5]))

    return ind

# generate population with popSize
def genPopulation(numNode, popSize):
    pop = []
    while len(pop) < popSize:
        ind = genIndividual(numNode)
        if ind not in pop:
            pop.append(ind)

    return pop

