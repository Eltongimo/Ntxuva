import sys
from gpu_methods.optimized_methods import *

@njit()
def utilidade(ntxuva):
    return np.sum(ntxuva[0:2]) - np.sum(ntxuva[2:4])
