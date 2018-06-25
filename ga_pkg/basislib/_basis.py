import random
import numpy
from functools import reduce

__all__ = ["basis", "emo"]

class emo(object):
    idx2mode = dict([(0,'A'), (1,'S')])
    
    def __init__(self, _mode, _i, _j):
        self._mode = _mode
        self._i = _i
        self._j = _j
    
    def __repr__(self):
        return "emo({mode}, {i}, {j})".format(mode=self.mode, i=self.i, j=self.j)
    
    def __str__(self):
        return "{mode}({i:2},{j:2})".format(mode=self.mode, i=self.i, j=self.j)
    
    def __eq__(self, other):
        return isinstance(other,emo) and self.mode == other.mode and self.i == other.i and self.j == other.j
    
    @property
    def i(self):
        return self._i
    
    @property
    def j(self):
        return self._j
    
    @property
    def mode(self):
        return self._mode
    
    """
    @classmethod
    def get_randoms(cls, n, mu, sigma):
        data = []
        num_data = int(random.normalvariate(mu, sigma))
        if num_data < 20: num_data = 20
        
        for i in range(num_data):
            data.append(emo.get_random(n))
        return data
     """

class basis(object):
    def __init__(self, data):
        """
            :param: data is list of emo
        """
        assert isinstance(data, list)
        #assert data # data is not empty
        #assert isinstance(data[0], emo)
        
        self._data = data
    
    def __repr__(self):
        return "basis({data})".format(data=self.data)
    
    def __str__(self):
        return "{0}".format(", ".join([str(i) for i in self.data]))
    
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self,key):
        return self.data[key]
    
    @property
    def data(self):
        return self._data
    
    def to_mat(self, ndim):
        mat = numpy.eye(ndim, dtype=numpy.int32)
        for e in self.data:
            if e.mode == 'A':
                mat[e.j] ^= mat[e.i]
            else:
                mat[e.i], mat[e.j] = mat[e.j].copy(), mat[e.i].copy()
        
        return mat
    
    def to_inv_mat(self, ndim):
        mat = numpy.eye(ndim, dtype=numpy.int32)
        for e in self.data[::-1]:
            if e.mode == 'A':
                mat[e.j] ^= mat[e.i]
            else:
                mat[e.i], mat[e.j] = mat[e.j].copy(), mat[e.i].copy()
        
        return mat
    
    def change_basis(self, ind):
        for e in self.data:
            if e.mode == 'A':
                ind[e.j] ^= ind[e.i]
            else:
                ind[e.i], ind[e.j] = ind[e.j], ind[e.i]
        
        return
    
    def revert_basis(self, ind):
        for e in self.data[::-1]:
            if e.mode == 'A':
                ind[e.j] ^= ind[e.i]
            else:
                ind[e.i], ind[e.j] = ind[e.j], ind[e.i]
        
        return