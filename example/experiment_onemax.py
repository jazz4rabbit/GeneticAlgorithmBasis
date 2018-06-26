import sys
import random
import numpy
import copy
import pickle
import collections
from ga_pkg import ga
from ga_pkg import problem

Fname = collections.namedtuple('Fname', ['origin', 'log'])
Param = collections.namedtuple('Param', ['IND_SIZE','n','fname'])

def to_csv(fname, logbook, mode='w', exist_header=False):
    with open(fname, mode) as f:
        if exist_header:
            f.write(logbook.stream + '\n')
        else:
            lines = logbook.stream.splitlines()[2:]
            f.write('\n'.join(lines) + '\n')
    return

def get_param(IND_SIZE):
    n = IND_SIZE * 4
    fname_origin = \
            "./onemax/pkl/init_n_{n}_INDSIZE_{IND_SIZE}.pkl".format(n=n,IND_SIZE=IND_SIZE)
    fname_log = "./onemax/logbook/n_{n}_INDSIZE_{IND_SIZE}".format(
                    n=n,IND_SIZE=IND_SIZE
                ) + "_{i}.log"
    fname = Fname(origin=fname_origin, log=fname_log)

    return Param(IND_SIZE=IND_SIZE, n=n, fname=fname)

if __name__ == "__main__":
    if len(sys.argv) != 2 or not sys.argv[1].isdecimal():
        print("usage: {0} <IND_SIZE>".format(sys.argv[0]))
        sys.exit()

    param = get_param(int(sys.argv[1])) # input IND_SIZE
    
    model_origin = problem.onemax.from_setting(param.n, param.IND_SIZE)
    ga.to_pkl(model_origin, param.fname.origin)

    for i in range(100):
        random.seed(i)

        model = copy.deepcopy(model_origin)
        model, logbook = ga.run_target(
                model, ngen=100, fit_val_target=(param.IND_SIZE,), nloop=100
        )
        to_csv(param.fname.log.format(i=i), logbook, exist_header=True)

        # calculate information
        total_time = sum(logbook.select('time'))

        maxidx = numpy.argmax(logbook.select('max'))
        maxval = logbook.select('max')[maxidx]
        gen = maxidx if maxval == param.IND_SIZE else None
        
        print("idx: {0}, best_fit: {1}, gen: {2}, time: {3}".format(
                i, model.halloffame[0].fitness.values, gen, total_time)
        )
