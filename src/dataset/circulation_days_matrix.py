import numpy as np
import math


def generate_circulation_days_matrix(L, O):
    circulation_matrix = []
    for o in O:
        suppliers_circulation_list = []
        for _ in L:
            suppliers_circulation_list.append(np.random.randint(math.ceil(max(O) / o), max(O) + 1, dtype=int))
        print(suppliers_circulation_list)
        circulation_matrix.append(suppliers_circulation_list)
    return circulation_matrix
