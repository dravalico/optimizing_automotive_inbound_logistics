import numpy as np
from scipy.optimize import minimize


def generate_lognormal_distribution_samples(min_val, avg_val, max_val, size):
    epsilon = 0.00001

    def objective(params):
        mu, sigma = params
        return (np.log(min_val + epsilon) - mu) ** 2 + (np.log(max_val) - mu) ** 2 + \
            (np.exp(mu + 0.5 * sigma ** 2) - avg_val) ** 2

    x0 = [np.log(min_val + epsilon), 1.0]
    bounds = ((None, None), (0.01, None))
    result = minimize(objective, x0, bounds=bounds)
    mu_opt, sigma_opt = result.x
    samples = np.random.lognormal(mean=mu_opt, sigma=sigma_opt, size=size)
    samples = np.clip(samples, min_val, max_val)
    return samples


def generate_samples(min_val, avg_val, max_val, size):
    num_runs = 5
    lognormal_distributions = []
    for _ in range(num_runs):
        lognormal_samples = generate_lognormal_distribution_samples(min_val, avg_val, max_val, size)
        lognormal_distributions.append(lognormal_samples)
    average_lognormal = np.mean(lognormal_distributions, axis=0)
    return average_lognormal


def print_general_statistics(samples, name):
    print(f"{'=' * 60}")
    print(name)
    print("len", len(samples))
    print("min", np.min(samples))
    print("mean", np.mean(samples))
    print("max", np.max(samples))
    print(f"{'=' * 60}")
