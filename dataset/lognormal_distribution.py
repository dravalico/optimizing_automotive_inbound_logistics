import numpy as np
import matplotlib.pyplot as plt


def _generate_lognormal_distribution_samples(min, avg, max, size):
    mu = np.log((avg ** 2) / np.sqrt(avg ** 2 + (max - min) ** 2))
    sigma = np.sqrt(np.log(1 + ((max - min) ** 2) / (avg ** 2)))
    return np.random.lognormal(mu, sigma, size)


def _filter_samples_by_percentile(samples, prctile_min, prctile_max):
    print(f"\n{'=' * 60}")
    percentile_5 = np.percentile(samples, prctile_min)
    percentile_95 = np.percentile(samples, prctile_max)
    filtered_samples = [x for x in samples if percentile_5 <= x <= percentile_95]
    print(prctile_min, "-", prctile_max, "% percentile min", np.min(filtered_samples))
    print(prctile_min, "-", prctile_max, "% percentile mean", np.mean(filtered_samples))
    print(prctile_min, "-", prctile_max, "% percentile max", np.max(filtered_samples))
    print(f"{'=' * 60}")
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


def generate_samples(min, avg, max, size, prctile_min, prctile_max):
    samples = _generate_lognormal_distribution_samples(min, avg, max, size)
    return _filter_samples_by_percentile(samples, prctile_min, prctile_max)
