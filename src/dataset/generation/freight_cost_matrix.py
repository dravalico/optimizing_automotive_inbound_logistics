import numpy as np
import matplotlib.pyplot as plt


def _compressed_logistic_function(x, scale, shift, min_value, max_value):
    return (max_value - min_value) / (1 + np.exp(-scale * (x - shift))) + min_value


def _generate_freight_cost_matrix_LTL_per_zone(Q, Z):
    prices_per_zone = np.zeros([len(Q), len(Z)])
    for i in Q:
        prices_per_zone[i, 0] = round(_compressed_logistic_function(i, -0.6, 4.5, 1, 10), 2)
    for i in range(1, len(Z)):
        prices_per_zone[:, i] = np.round(((np.random.rand(1) + 0.5) * prices_per_zone[:, 0]), 2)
    return prices_per_zone


def generate_freight_cost_matrix_LTL(r_iz, Q, Z, L):
    prices_per_zone = _generate_freight_cost_matrix_LTL_per_zone(Q, Z)
    prices = np.zeros([len(Q), len(L)])
    for b in Q:
        for i in L:
            prices[b, i] = prices_per_zone[b, :] @ r_iz[i, :]
    return prices


def generate_freight_cost_matrix_CES(K):
    prices = np.zeros(len(K))
    for i in K:
        prices[i] = round(_compressed_logistic_function(i, -0.6, 4.5, 1, 10), 2)
    return prices


def plot_sigmoid_function():
    x = np.linspace(0, 10, 100)
    y = _compressed_logistic_function(x, -0.6, 4.5, 1, 10)
    plt.plot(x, y)
    plt.xlabel("Weight class")
    plt.ylabel("Price")
    integer_x_values = np.arange(10)
    integer_y_values = _compressed_logistic_function(integer_x_values, -0.6, 4.5, 1, 10)
    plt.scatter(integer_x_values, integer_y_values, color="red", label="Price-per-class")
    plt.legend()
    plt.show()


# plot_sigmoid_function()
