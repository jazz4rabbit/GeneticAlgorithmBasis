from ... import ga
from ... import basislib
from deap import base
from deap import creator
from deap import tools
import random
import numpy
import copy

import time

__all__ = ["from_setting"]

ndim_fit=5
str_FitnessMax = "FitnessMax_{0}dim".format(ndim_fit)
if not str_FitnessMax in vars(creator):
    creator.create(str_FitnessMax, base.Fitness, weights=(1.0,)*ndim_fit)
FitnessMax_Ndim = vars(creator)[str_FitnessMax]
creator.create("Individual_basis", basislib.basis, fitness=FitnessMax_Ndim)

def evalBasis(individual, target_model_, target_ngen):
    """
        individual : basis
        target_ga
    """
    fit = tuple()
    for i in range(10):
        target_model = copy.deepcopy(target_model_)

        target_model.toolbox.register("mate", individual.change_mate(target_model.toolbox.mate))
        target_model.toolbox.register("mutate", individual.change_mutate(target_model.toolbox.mutate))

        model, logbook = ga.run(target_model, ngen=target_ngen, verbose=False)

        fit += model.halloffame[0].fitness.values
        #individual.target_model = model
        #individual.logbook = logbook
        #print(model.halloffame[0])
    return tuple(sorted(fit,key=lambda x:-x)) #model.halloffame[0].fitness.values #model.toolbox.evaluate(model.halloffame[0])

def mutEmos(individual, ndim, indpb):
    data = []
    for i in range(len(individual)):
        num_rand = random.random()
        if num_rand < indpb:
            if num_rand < indpb / 3.0: # mutate
                data.append(basislib.random.randemo(ndim))
            elif num_rand < indpb * 2.0 / 3.0: # addition (left-side)
                data.append(basislib.random.randemo(ndim))
                data.append(individual[i])
            else: # deleation
                pass
        else:
            data.append(individual[i])

    if random.random() < indpb / 3.0: # last addition (right-side)
        data.append(basislib.random.randemo(ndim))

    return creator.Individual_basis(data),

def cxAlignOnePoint(ind1, ind2):
    # get edit-distance table
    row, column = len(ind1) + 1, len(ind2) + 1
    if (row > column):
        row, column = column, row
        ind1, ind2 = ind2, ind1
    M = numpy.zeros((row,column), dtype=numpy.int32)
    M[0] = numpy.arange(column)
    M[:,0] = numpy.arange(row)
    
    for i in range(1,row):
        for j in range(1,column):
            if ind1[i-1] == ind2[j-1]:
                M[i,j] = M[i-1,j-1]
            else:
                M[i,j] = min(M[i-1,j],M[i-1,j-1],M[i,j-1]) + 1
    
    i = -1; j= -1
    d1 = []
    d2 = []
    while i != -row and j != -column:
        if i == -row: # 가로축에 닿은 경우
            d1.insert(0,None)
            d2.insert(0,ind2[j])
            j -= 1
            continue
        if j == -column: # 세로축에 닿은 경우
            d1.insert(0,data1[i])
            d2.insert(0,None)
            continue

        case = numpy.argmin([M[i-1,j-1], M[i,j-1], M[i-1,j]])
        if case == 0: 
            #if M[i-1,j-1] == M[i,j]: #none case
            #else edition case
            d1.insert(0, ind1[i])
            d2.insert(0, ind2[j])
            i -= 1; j -= 1
        elif case == 1: # left
            d1.insert(0, None)
            d2.insert(0, ind2[j])
            j -= 1;
        else: # Insertion
            d1.insert(0,ind1[i])
            d2.insert(0,None)
            i -= 1;
    #print(d1)
    #print(d2)
  
    size = min(len(d1), len(d2))
    if size == 0:
        return creator.Individual_basis([]), creator.Individual_basis([])
    elif size == 1:
        return creator.Individual_basis([e for e in d1 if e!=None]), creator.Individual_basis([e for e in d2 if e!=None])
    
    cxpoint = random.randint(1, size - 1)
    d1[cxpoint:], d2[cxpoint:] = d2[cxpoint:], d1[cxpoint:]
    return creator.Individual_basis([e for e in d1 if e!=None]), creator.Individual_basis([e for e in d2 if e!=None])

def s(ind):
    return ind.fitness.values

def from_setting(n, target_model, target_ngen, cxpb=0.5, mutpb=0.2):
    """
        n : size of population
        ndim : size of individual
    """    
    target_model = copy.deepcopy(target_model)
    ndim = len(target_model.population[0])
    
    toolbox = base.Toolbox()
    # Attribute generator 
    toolbox.register("attr_emos", basislib.random.randemos, ndim)
    # Structure initializers
    toolbox.register("individual", tools.initIterate, creator.Individual_basis, 
        toolbox.attr_emos)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    toolbox.register("evaluate", evalBasis, target_model_=target_model, target_ngen=target_ngen)
    toolbox.register("mate", cxAlignOnePoint)
    toolbox.register("mutate", mutEmos, ndim=ndim, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    stats = tools.Statistics(s)
    stats.register("avg", numpy.mean, axis=0)
    stats.register("min", numpy.min, axis=0)
    stats.register("max", numpy.max, axis=0)
    stats.register("std", numpy.std, axis=0)

    population = toolbox.population(n)

    hof = tools.HallOfFame(maxsize=1)
    gen = 0
    model = ga.Model(population=population, toolbox=toolbox, cxpb=cxpb, mutpb=mutpb, stats=stats, halloffame=hof, gen=gen)
    return model