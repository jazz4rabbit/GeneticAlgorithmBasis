import random
import numpy
import itertools
from ... import ga
from deap import base
from deap import creator
from deap import tools

__all__ = ["from_setting"]

if __debug__:
    __all__ += ["gen_Tables"]

def nk_brute_force(model):
    N = len(model.population[0])
    
    best = None; fit_best = 0.0
    worst = None; fit_worst = 1.0
    for i in itertools.product(*([range(2)] * N)):
        fit_cur = model.toolbox.evaluate(i)[0]
        if fit_best < fit_cur:
            fit_best = fit_cur
            best = i

        if fit_worst > fit_cur:
            fit_worst = fit_cur
            worst = i
    
    return best, worst

def gen_Tables(n,k):
    # locusTable, scoreTable
    
    # Part of scoreTable
    scoreTable = numpy.random.rand(n,2**(k+1))
    
    # Part of locusTable 
    locusTable = numpy.zeros((n,k+1),dtype=numpy.int32)

    for i in range(n):
        temp = list(range(0,i)) + list(range(i+1,n))
        random.shuffle(temp)
        locusTable[i,1:] = temp[:k]
    locusTable[:,0] = numpy.arange(n)
    
    return scoreTable, locusTable

def eval_nk_landscape(ind, scoreTable, locusTable):
    n = len(ind)
    fitness = 0
    for i in range(n):
        locus_i = numpy.array([ind[i] for i in locusTable[i]])
        col = locus_i.dot(1 << numpy.arange(locus_i.size)[::-1])
        fitness += scoreTable[i,col]
    
    return (fitness / n,)

def s(ind):
    return ind.fitness.values

def from_setting(n, IND_SIZE, K, cxpb=0.5, mutpb=0.2):
    """
        n        : size of population
        IND_SIZE : size of individual
    """
    N = IND_SIZE
    
    toolbox = base.Toolbox()
    # Attribute generator 
    toolbox.register("attr_bool", random.randint, 0, 1)
    # Structure initializers
    toolbox.register("individual", tools.initRepeat, creator.Individual_1dim, 
        toolbox.attr_bool, IND_SIZE)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    scoreTable, locusTable = gen_Tables(N, K)
    toolbox.register("evaluate", eval_nk_landscape, scoreTable=scoreTable, locusTable=locusTable)
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