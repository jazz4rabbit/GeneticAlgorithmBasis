import numpy
import copy

from .. import onemax

__all__ = ["from_setting", "from_model_onemax"]

def evalVariantOneMax(individual, mat_basis):
    ind_basis_change = type(individual)(mat_basis @ individual % 2)
    return sum(ind_basis_change),

def from_setting(n, IND_SIZE, BASIS, cxpb=0.5, mutpb=0.2):
    model = onemax.from_setting(n, IND_SIZE, cxpb, mutpb)
    mat_basis = BASIS.to_mat(IND_SIZE)
    model.toolbox.register("evaluate", evalVariantOneMax, mat_basis=mat_basis)
    return model

def from_model_onemax(model_onemax, BASIS, cxpb=0.5, mutpb=0.2):
    model = copy.deepcopy(model_onemax)
    IND_SIZE = len(model_onemax.population[0])
    type_ind = type(model_onemax.population[0])
    inv_mat_basis = BASIS.to_inv_mat(IND_SIZE)
    
    # change basis with inverse
    for i,ind in enumerate(model.population):
        model.population[i] = type_ind(inv_mat_basis @ ind % 2)
    
    mat_basis = BASIS.to_mat(IND_SIZE)
    model.toolbox.register("evaluate", evalVariantOneMax, mat_basis=mat_basis)
    return model