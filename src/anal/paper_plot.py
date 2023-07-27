import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../results/obj_func_data_20230726160608.csv')


def plot_obj_value_for_suppliers():
    means = df.groupby("n_suppliers").obj_value.mean()
    stds = df.groupby("n_suppliers").obj_value.std()
    plt.plot(means, label="Mean", marker='o')
    plt.xlabel("Number of suppliers")
    plt.ylabel("Objective value")
    plt.legend()
    plt.xticks(means.index)
    plt.fill_between(means.index, means - stds, means + stds, alpha=0.2, label="Standard deviation")
    plt.show()


def plot_gap_for_suppliers():
    means = df.groupby("n_suppliers").obj_gap.mean()
    stds = df.groupby("n_suppliers").obj_gap.std()
    plt.plot(means, label="Mean", marker='o')
    plt.xlabel("Number of suppliers")
    plt.ylabel("Objective gap")
    plt.legend()
    plt.xticks(means.index)
    plt.fill_between(means.index, means - stds, means + stds, alpha=0.2, label="Standard deviation")
    plt.show()


def plot_execution_time_for_suppliers():
    means = df.groupby("n_suppliers").execution_time.mean()
    stds = df.groupby("n_suppliers").execution_time.std()
    plt.plot(means, label="Mean", marker='o')
    plt.xlabel("Number of suppliers")
    plt.ylabel("Execution time")
    plt.legend()
    plt.xticks(means.index)
    plt.fill_between(means.index, means - stds, means + stds, alpha=0.2, label="Standard deviation")
    plt.show()


def plot_pie_chart_of_transport_shares():  # FIXME does not work
    df_share_suppl_FTL = df.groupby("n_suppliers").share_suppl_FTL.mean()
    share_suppl_CES = df.groupby("n_suppliers").share_suppl_CES.mean()
    share_suppl_LTL = df.groupby("n_suppliers").share_suppl_LTL.mean()
    df1 = pd.concat([df_share_suppl_FTL.head(1), share_suppl_CES.head(1), share_suppl_LTL.head(1)]).to_frame()
    print(df1.values)


plot_obj_value_for_suppliers()
plot_gap_for_suppliers()
plot_execution_time_for_suppliers()
plot_pie_chart_of_transport_shares()
