import numpy as np
import matplotlib.pyplot as plt
import random


def _generate_lognormal_distribution_samples(min, avg, max, size):
    mu = np.log((avg ** 2) / np.sqrt(avg ** 2 + (max - min) ** 2))
    sigma = np.sqrt(np.log(1 + ((max - min) ** 2) / (avg ** 2)))
    return np.random.lognormal(mu, sigma, size)


def _filter_samples_by_percentile(samples, prctile_min, prctile_max):
    percentile_5 = np.percentile(samples, prctile_min)
    percentile_95 = np.percentile(samples, prctile_max)
    filtered_samples = [x for x in samples if percentile_5 <= x <= percentile_95]
    return filtered_samples


def plot_lognormal_values_and_distribution(samples, x_limit):
    # Plot the histogram
    plt.hist(samples, bins='auto', edgecolor='black', density=True)
    plt.xlim(0, x_limit)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Histogram of Samples')

    # FIXME lognormal plot
    # Calculate the lognormal distribution PDF
    # x = np.linspace(0.001, x_limit_max, 10000)
    # mu = np.log(np.mean(samples))
    # sigma = np.log(np.std(samples))
    # pdf = lognorm.pdf(x, s=sigma, scale=np.exp(mu))
    # plt.plot(x, pdf, color='red', label='Lognormal PDF')
    # plt.legend()
    plt.show()


def print_general_statistics(samples, name):
    print(f"{'=' * 60}")
    print(name)
    print("len", len(samples))
    print("min", np.min(samples))
    print("mean", np.mean(samples))
    print("max", np.max(samples))
    print(f"{'=' * 60}")


def remove_extra_samples(samples, size):
    repetition = len(samples) - size
    for _ in range(repetition):
        samples.remove(samples[random.randint(0, len(samples) - 1)])
    return samples


def generate_samples(min, avg, max, size, prctile_min, prctile_max):
    samples = _generate_lognormal_distribution_samples(min, avg, max, int(size * 1.2))
    samples = _filter_samples_by_percentile(samples, prctile_min, prctile_max)
    return remove_extra_samples(samples, size)