from src.notation.sets_and_params import L, Q, K
import numpy as np
import random
import matplotlib.pyplot as plt


def _compressed_logistic_function(x, scale, shift, min_value, max_value):
    return (max_value - min_value) / (1 + np.exp(-scale * (x - shift))) + min_value


def zero_order_hold(t, dt, y, a, b):
    dt = dt  # Time step
    t = t  # Time points
    x = a * (t - b)  # Scaled and shifted input
    y_continuous = y  # Continuous sigmoid function
    return np.round(y_continuous)  # Zero-order hold


# def zero_order_hold(signal, sampling_rate, output_rate):
#     input_length = len(signal)
#     output_length = int(input_length * (output_rate / sampling_rate))
#     output = np.zeros(output_length)
#     for i in range(output_length):
#         input_index = int(i * (sampling_rate / output_rate))
#         output[i] = signal[input_index]
#     return output


def generate_freight_cost_matrix_LTL():
    zones_prices = [[] for _ in Q]
    elements_per_list = max(L) // max(Q)
    is_list_full = max(L) % max(Q)
    current_list_index = 0
    for i in L:
        zones_prices[current_list_index].append(i)
        if len(zones_prices[current_list_index]) >= elements_per_list + (1 if is_list_full > 0 else 0):
            current_list_index += 1
            is_list_full -= 1
    costs_constants_per_zone = []
    for i in Q:
        costs_constants_per_zone[i] = round(random.uniform(0, 1), 2)
    return zones_prices


def generate_freight_cost_matrix_CES():
    prices = []
    for i in K:
        pass
    return prices


# Example input signal
scale = -0.6
shift = 4.5
x = np.arange(1, 10.01, 0.001)
signal = _compressed_logistic_function(x, scale, shift, 1, 10)
signal_zoh = zero_order_hold(x, 0.001, signal, scale, shift)

# Plot the original and zero-order hold signals
plt.figure(figsize=(10, 4))
plt.plot(x, signal, label='Original Signal')
plt.plot(x, signal_zoh, 'r-', label='Zero-Order Hold')
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.legend()
plt.show()
