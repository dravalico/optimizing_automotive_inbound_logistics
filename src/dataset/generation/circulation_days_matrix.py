import numpy as np
import math


def generate_circulation_days_matrix(L, O):
    circulation_matrix = np.zeros([len(L), len(O)])
    n_orders = [1, 2, 4, 6, 8, 10]
    for i in L:
        for o in O:
            circulation_matrix[i, o] = np.random.randint(0, math.ceil(max(n_orders) / n_orders[o]), dtype=int)
    return circulation_matrix
