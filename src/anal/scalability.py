import matplotlib.pyplot as plt
from paper_plot import load_data_and_filter_by_zones_horizon, FILE_PATH


def plot_execution_time_for_suppliers(df):
    means = df.groupby("n_suppliers").execution_time.mean()
    stds = df.groupby("n_suppliers").execution_time.std()
    plt.plot(means, label="Mean", marker='o')
    plt.xlabel("Number of suppliers")
    plt.ylabel("Execution time")
    plt.legend()
    plt.xticks(means.index)
    plt.fill_between(means.index, means - stds, means + stds, alpha=0.2, label="Standard deviation")
    plt.show()


df_full = load_data_and_filter_by_zones_horizon(FILE_PATH, 34, 10)
plot_execution_time_for_suppliers(df_full)
