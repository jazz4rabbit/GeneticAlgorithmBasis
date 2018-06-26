import sys
import random
import numpy
import copy
import collections
import os
from ga_pkg import ga
from ga_pkg import problem
from ga_pkg import basislib
from deap import creator

Fname = collections.namedtuple('Fname', ['ori','tar', 'log_ori', 'log_tar'])
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
    target = "v_onemax"
    n = IND_SIZE * 4
    
    fname_ori = \
        "./good_basis/pkl/init_n_{n}_INDSIZE_{IND_SIZE}.pkl".format(n=n,IND_SIZE=IND_SIZE)
    fname_tar = "./{target}/pkl/init_n_{n}_INDSIZE_{IND_SIZE}.pkl".format(
        target=target,n=n,IND_SIZE=IND_SIZE
    )
    fname_log_ori = "./good_basis/logbook/n_{n}_INDSIZE_{IND_SIZE}".format(n=n,IND_SIZE=IND_SIZE)
    fname_log_tar = "./good_basis/logbook/{target}_n_{n}_INDSIZE_{IND_SIZE}".format(
        target=target,n=n,IND_SIZE=IND_SIZE
    ) + "_{i}.log"
    fname = Fname(ori=fname_ori, tar=fname_tar, log_ori=fname_log_ori, log_tar=fname_log_tar)

    return Param(IND_SIZE=IND_SIZE, n=n, fname=fname)


if __name__ == "__main__":
    if len(sys.argv) != 2 or not sys.argv[1].isdecimal():
        print("usage: {0} <IND_SIZE>".format(sys.argv[0]))
        sys.exit()

    param = get_param(int(sys.argv[1])) # input IND_SIZE
    
    if not os.path.exists(param.fname.tar):
        print("requirment: python -O experiment_v_onemax <IND_SIZE>")
        sys.exit()
    
    model_tar, _ = ga.from_pkl(param.fname.tar)
    model_ori = problem.good_basis.from_setting(param.n, model_tar, param.IND_SIZE)

    model_ori, logbook = ga.run(model_ori, param.IND_SIZE*4)
    ga.to_pkl(model_ori, param.fname.ori)
    to_csv(param.fname.log_ori, logbook, exist_header=True)
    
    ind = model_ori.halloffame[0]
    
    """ only load
    model_tar, _ = ga.from_pkl(param.fname.tar)
    model_ori, _ = ga.from_pkl(param.fname.ori)
    ind = model_ori.halloffame[0]
    """

    for i in range(100):
        random.seed(i)
        
        model = ind.change_basis(model_tar)
        model, logbook = ga.run_target(
            model, ngen=100, fit_val_target=(param.IND_SIZE,), nloop=100
        )
        to_csv(param.fname.log_tar.format(i=i), logbook, exist_header=True)
        
        # calculate information
        total_time = sum(logbook.select('time'))

        maxidx = numpy.argmax(logbook.select('max'))
        maxval = logbook.select('max')[maxidx]
        gen = maxidx if maxval == param.IND_SIZE else None
        
        print("idx: {0}, best_fit: {1}, gen: {2}, time: {3}".format(
                i, model.halloffame[0].fitness.values, gen, total_time)
        )