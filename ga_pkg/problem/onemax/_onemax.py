from ... import ga
from deap import base
from deap import creator
from deap import tools
import random
import numpy

__all__ = ["from_setting"]

def evalOneMax(individual):
    return sum(individual),

def s(ind):
    return ind.fitness.values

def from_setting(n, IND_SIZE, cxpb=0.5, mutpb=0.2):
    """
        n        : size of population
        IND_SIZE : size of individual
    """
    toolbox = base.Toolbox()
    # Attribute generator 
    toolbox.register("attr_bool", random.randint, 0, 1)
    # Structure initializers
    toolbox.register("individual", tools.initRepeat, creator.Individual_1dim, 
        toolbox.attr_bool, IND_SIZE)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", evalOneMax)
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