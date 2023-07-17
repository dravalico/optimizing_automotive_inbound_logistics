import numpy as np


def _compressed_logistic_function(x, scale, shift, min_value, max_value):
    return (max_value - min_value) / (1 + np.exp(-scale * (x - shift))) + min_value


def generate_freight_cost_matrix_LTL(Q, Z, L):
    prices_per_zone = np.zeros([len(Q), len(Z)])
    suppliers_per_zone = len(L) // len(Z)
    suppliers_per_last_zone = len(L) - suppliers_per_zone * (len(Z) - 1)
    for i in Q:
        prices_per_zone[i, 0] = round(_compressed_logistic_function(i, -0.6, 4.5, 1, 10), 2)
    for i in range(1, len(Z)):
        prices_per_zone[:, i] = np.round(((np.random.rand(1) + 0.5) * prices_per_zone[:, 0]), 2)
    repeats = suppliers_per_zone * np.ones(len(Z) - 1, dtype=int)
    repeats = np.append(repeats, suppliers_per_last_zone)
    prices = np.repeat(prices_per_zone, repeats, axis=1)
    return prices


def generate_freight_cost_matrix_CES(K):
    prices = np.zeros(len(K) + 1)
    for i in range(len(K) + 1):
        prices[i] = round(_compressed_logistic_function(i, -0.6, 4.5, 1, 10), 2)
    return prices
