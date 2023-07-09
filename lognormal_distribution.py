import numpy as np
import matplotlib.pyplot as plt


def generate_lognormal_distribution_samples(min, avg, max, size):
    mu = np.log((avg ** 2) / np.sqrt(avg ** 2 + (max - min) ** 2))
    sigma = np.sqrt(np.log(1 + ((max - min) ** 2) / (avg ** 2)))
    return np.random.lognormal(mu, sigma, size)


def plot_lognormal_values_and_distribution(samples, x_limit_max):
    # Plot the histogram
    plt.hist(samples, bins='auto', edgecolor='black', density=True)
    plt.xlim(0, x_limit_max)
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


samples = generate_lognormal_distribution_samples(6.0, 538.38, 2547.00, 570)
print("Mean:", np.mean(samples))

percentile_5 = np.percentile(samples, 5)
percentile_95 = np.percentile(samples, 95)
filtered_samples = [x for x in samples if percentile_5 <= x <= percentile_95]
print("3-97% percentile min:", np.min(filtered_samples))
print("3-97% percentile mean:", np.mean(filtered_samples))
print("3-97% percentile max:", np.max(filtered_samples))
plot_lognormal_values_and_distribution(samples, 2547.00)
