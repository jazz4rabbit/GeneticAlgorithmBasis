import sys
import random
import numpy
import copy
import pickle
import collections
from ga_pkg import ga
from ga_pkg import problem

Fname = collections.namedtuple('Fname', ['origin','log'])
Param = collections.namedtuple('Param', ['IND_SIZE','n','k','fname'])

def to_csv(fname, logbook, mode='w', exist_header=False):
    with open(fname, mode) as f:
        if exist_header:
            f.write(logbook.stream + '\n')
        else:
            lines = logbook.stream.splitlines()[2:]
            f.write('\n'.join(lines) + '\n')
    return

def get_param(IND_SIZE, k):
    """
        :n: is size of population
        :IND_SIZE: n (nk-landscape)
        :k: k (nk-landscape)
    """
    n = IND_SIZE * 4
    fname_origin \
    = "./nk_landscape/pkl/init_n_{n}_INDSIZE_{IND_SIZE}_k_{k}.pkl".format(
        n=n,IND_SIZE=IND_SIZE,k=k
    )
    fname_log = "./nk_landscape/logbook/n_{n}_INDSIZE_{IND_SIZE}_k_{k}".format(
        n=n,IND_SIZE=IND_SIZE,k=k
    ) + "_{i}.log"
    fname = Fname(origin=fname_origin, log=fname_log)

    return Param(IND_SIZE=IND_SIZE, n=n, k=k, fname=fname)

if __name__ == "__main__":
    if len(sys.argv) != 3 or not sys.argv[1].isdecimal() or not sys.argv[2].isdecimal():
        print("usage: {0} <IND_SIZE> <k>".format(sys.argv[0]))
        sys.exit()

    param = get_param(int(sys.argv[1]), int(sys.argv[2])) # input IND_SIZE, k
    
    model_origin = problem.nk_landscape.from_setting(param.n, param.IND_SIZE, param.k)
    ga.to_pkl(model_origin, param.fname.origin)

    for i in range(100):
        random.seed(i)

        model = copy.deepcopy(model_origin)
        model, logbook = ga.run(model, ngen=3000)
        to_csv(param.fname.log.format(i=i), logbook, exist_header=True)

        # calculate information
        total_time = sum(logbook.select('time'))

        maxidx = numpy.argmax(logbook.select('max'))
        maxval = logbook.select('max')[maxidx]
        
        print("idx: {0}, best_fit: {1}, time: {2}".format(
                i, model.halloffame[0].fitness.values, total_time)
        )
