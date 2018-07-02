import random
import numpy
import networkx as nx

from ... import ga
from deap import base
from deap import creator
from deap import tools
from collections import defaultdict

__all__ = ["from_setting"]

def evalGraphPartition(individual, g):
    if sum(individual) in [0, len(individual)]:
        return len(individual) ** 2,
    
    pos2nodes = defaultdict(list)
    for node in g.nodes:
        pos = individual[node]
        pos2nodes[pos].append(node)

    pos_min_len = numpy.argmin([len(pos2nodes[pos]) for pos in pos2nodes])
    nodes_one_side_pos = pos2nodes[pos_min_len]
    
    fit = 0
    for node in nodes_one_side_pos:
        for neighbor in g.neighbors(node):
            if neighbor not in nodes_one_side_pos:
                fit += 1

    return fit,

def get_graph(fname):
    g = nx.Graph()
    with open(fname) as f:
        for line in f:
            s_line = line.split()
            node = int(s_line[0]) - 1
            deg = int(s_line[2])
            outNodes = [int(outNode) - 1 for outNode in s_line[3:deg+3]]

            g.add_node(node)
            g.add_edges_from([(node, outNode) for outNode in outNodes])
    
    return g

def s(ind):
    return ind.fitness.values

def from_setting(n, fname_graph, cxpb=0.5, mutpb=0.2):
    """
        n        : size of population
        IND_SIZE : size of individual
    """
    g = get_graph(fname_graph)
    IND_SIZE = len(g.nodes)
    
    toolbox = base.Toolbox()
    # Attribute generator 
    toolbox.register("attr_bool", random.randint, 0, 1)
    # Structure initializers
    toolbox.register("individual", tools.initRepeat, creator.Individual_1dim_min, 
        toolbox.attr_bool, IND_SIZE)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", evalGraphPartition, g=g)
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    stats = tools.Statistics(s)
    stats.register("avg", numpy.mean)
    stats.register("min", numpy.min)
    stats.register("max", numpy.max)
    stats.register("std", numpy.std)

    population = toolbox.population(n)

    hof = tools.HallOfFame(maxsize=1)
    gen = 0
    model = ga.Model(population=population, toolbox=toolbox, cxpb=cxpb, mutpb=mutpb, stats=stats, halloffame=hof, gen=gen)
    return model