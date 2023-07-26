import numpy as np
from src.dataset.generation.lognormal_distribution import generate_lognormal_distribution_samples


def average_summary_statistics(min_val, avg_val, max_val, size, name):
    num_runs = 5
    min_values = []
    mean_values = []
    max_values = []
    for _ in range(num_runs):
        lognormal_samples = generate_lognormal_distribution_samples(min_val, avg_val, max_val, size)
        min_values.append(np.min(lognormal_samples))
        mean_values.append(np.mean(lognormal_samples))
        max_values.append(np.max(lognormal_samples))
    average_min = np.mean(min_values)
    if average_min < 1e-1:
        average_min = 0.00
    average_mean = np.mean(mean_values)
    average_max = np.mean(max_values)
    print(f"{name} - Average Min: {average_min}")
    print(f"{name} - Average Mean: {average_mean}")
    print(f"{name} - Average Max: {average_max}")


average_summary_statistics(1.41, 3439.98, 280573.60, 570, "Demand [# part numbers/day]")
average_summary_statistics(0.00, 2.53, 69.70, 570, "Demand [m^3/day]")
average_summary_statistics(0.00, 357.74, 9994.02, 570, "Demand [kg/day]")
average_summary_statistics(0.00, 0.08, 1.27, 570, "Load carrier rental costs")
average_summary_statistics(0.00, 1.43, 133.33, 570, "Load carrier invest costs")
average_summary_statistics(6.00, 538.38, 2547.00, 570, "Distance of suppliers")
