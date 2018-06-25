import random 
import collections
import pickle
import copy
from . import _algorithms as algorithms

__all__ = ["Model", "to_pkl", "from_pkl", "run", "run_target"]

Model = collections.namedtuple("Model", ["population", "toolbox", "cxpb", "mutpb", "stats", "halloffame", "gen"])

def to_pkl(model, fname, logbook=None, with_rndstate=False):
    """
        save model using pickle
    """
    with open(fname, "wb") as cp_file:
        data = {"model":model, "logbook":logbook}
        if with_rndstate:
            data["rndstate"] = random.getstate()
        pickle.dump(data, cp_file)

def from_pkl(fname):
    """
        load model using pickle
    """
    with open(fname, "rb") as cp_file:
        data = pickle.load(cp_file)
    
    rndstate = data.get("rndstate",None)
    if rndstate is not None:
        random.setstate(rndstate)
        
    return data["model"], data["logbook"]

def run(model, ngen, verbose=__debug__):
    model_dict_copy = copy.deepcopy(model)._asdict()
    #pop, log = algorithms.eaSimple(**model_copy._asdict(), ngen=ngen, verbose=verbose)
    pop, log = algorithms.eaSimple(**model_dict_copy, ngen=ngen, verbose=verbose)
    model_dict_copy['gen'] += ngen
    return Model(**model_dict_copy), log

def run_target(model, ngen, fit_val_target, nloop=10, verbose=__debug__):
    fit_target = (type(model.population[0].fitness))(fit_val_target)
    
    model, logbook_out = run(model, ngen, verbose)
    
    for _ in range(nloop - 1):
        if fit_target <= model.halloffame[0].fitness:
            break
        model, logbook = run(model, ngen, verbose)
        any(map(logbook_out.append,logbook[1:])) # append logbook
    return model, logbook_out