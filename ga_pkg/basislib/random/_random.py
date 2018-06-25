import random
from ... import basislib

__all__ = ["randemo", "randemos", "randbasis"]

def randemo(ndim):
    mode = basislib.emo.idx2mode[random.randint(0,1)]
    i = random.randint(0,ndim-1)
    j = random.randint(0,ndim-2)
    if j >= i:
        j+=1
    elif mode == 'S': # always i < j
        i, j = j, i
    
    return basislib.emo(mode, i, j)

def num_of_list(ndim):
    num = int(random.normalvariate(ndim*3, ndim))
    return num if num > 0 else 2

def randemos(ndim):
    num = num_of_list(ndim)
    return list(randemo(ndim) for _ in range(num))

def randbasis(ndim):
    return basislib.basis(randemos(ndim))