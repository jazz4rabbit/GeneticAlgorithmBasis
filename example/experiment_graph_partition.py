import sys
import random
import numpy
import copy
import pickle
import collections
import re
import os
from ga_pkg import ga
from ga_pkg import problem

Fname = collections.namedtuple('Fname', ['origin','log','graph'])
Param = collections.namedtuple('Param', ['IND_SIZE','n','fname'])

def to_csv(fname, logbook, mode='w', exist_header=False):
    with open(fname, mode) as f:
        if exist_header:
            f.write(logbook.stream + '\n')
        else:
            lines = logbook.stream.splitlines()[2:]
            f.write('\n'.join(lines) + '\n')
    return

def get_param(fname_graph):
    """
        :n: is size of population
        :IND_SIZE: n (nk-landscape)
        :k: k (nk-landscape)
    """
    if re.match(r'^.+/\w+?\d+\..*', fname_graph):
        IND_SIZE = int(re.sub(r'^.+/\w+?(\d+)\..*', r'\1', fname_graph))
    elif re.match(r'^.+/\w+\.\d+\.?.*', fname_graph):
        IND_SIZE = int(re.sub(r'^.+/\w+\.(\d+)\.?.*', r'\1', fname_graph))
    
    n = IND_SIZE * 4
    fname_origin \
    = "./graph_partition/pkl/init_{graph_name}.pkl".format(
        graph_name=os.path.basename(fname_graph)
    )
    fname_log = "./graph_partition/logbook/{graph_name}".format(
        graph_name=os.path.basename(fname_graph)
    ) + "_{i}.log"
    fname = Fname(origin=fname_origin, log=fname_log, graph=fname_graph)

    return Param(IND_SIZE=IND_SIZE, n=n, fname=fname)

if __name__ == "__main__":
    if len(sys.argv) != 2 or not os.path.exists(sys.argv[1]):
        print("usage: {0} <fname_graph>".format(sys.argv[0]))
        sys.exit()

    param = get_param(sys.argv[1]) # input IND_SIZE, k
    
    model_origin = problem.graph_partition.from_setting(param.n, param.fname.graph)
    ga.to_pkl(model_origin, param.fname.origin)

    for i in range(100):
        random.seed(i)

        model = copy.deepcopy(model_origin)
        model, logbook = ga.run(model, ngen=1000)
        to_csv(param.fname.log.format(i=i), logbook, exist_header=True)

        # calculate information
        total_time = sum(logbook.select('time'))

        minidx = numpy.argmax(logbook.select('min'))
        minval = logbook.select('min')[minidx]
        
        print("idx: {0}, best_fit: {1}, time: {2}".format(
                i, model.halloffame[0].fitness.values, total_time)
        )
