"""
evaluation.py --- calculate cut size and fitness
- calCut: Calculate the cut size of individual
- getCutsize: Get the best and worst cut size of population
- fitness: Calculate fitness using worst, best and current cut size.
"""

# Calculate the cut size of individual
def calCut(g, ind):
    part0 = [index for index in range(len(ind)) if ind[index] == 0]  # partition 0
    part1 = [index for index in range(len(ind)) if ind[index] == 1]  # partition 1

    g0 = g.subgraph(part0)
    g1 = g.subgraph(part1)

    cutSize = len(g.edges()) - (len(g0.edges()) + len(g1.edges()))
    
    return cutSize

# Get the best and worst cut size 
def getCutsize(pop, g):
    cuts = []

    for ind in pop:
        cutSize = calCut(g, ind)
        cuts.append(cutSize)

    bestCut = min(cuts)
    worstCut = max(cuts)

    return bestCut, worstCut


# Calculate fitness
def fitness(worstCut, bestCut, g, ind):
    curCut = calCut(g, ind) # current cut
    value = (worstCut - curCut) + (worstCut - bestCut) / 3  # fitness equation

    return value, curCut