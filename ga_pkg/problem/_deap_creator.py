from .. import basislib
from deap import base
from deap import creator
from deap import tools
import array

# for onemax
creator.create("FitnessMax_1dim", base.Fitness, weights=(1.0,))
#creator.create("onemax_Individual", numpy.ndarray, fitness=creator.onemax_FitnessMax)
creator.create("Individual_1dim", array.array, typecode='b', fitness=creator.FitnessMax_1dim)