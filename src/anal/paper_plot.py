import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../results/obj_func_data_20230726160608.csv')
df = df[
    (df['LTL_zones'] == 34) &
    (df['horizon'] == 10)
    ]


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


def plot_pie_chart_of_transport_share():
    values = [
        df.groupby("n_suppliers").share_suppl_FTL.mean().mean(),
        df.groupby("n_suppliers").share_suppl_CES.mean().mean(),
        df.groupby("n_suppliers").share_suppl_LTL.mean().mean()
    ]
    labels = ["FTL", "CES", "LTL"]
    colors = ['lightgreen', 'lightcoral', 'lightskyblue']
    plt.figure(figsize=(8, 8))
    plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', shadow=False, startangle=140)
    plt.axis('equal')
    plt.show()


def plot_pie_chart_of_trasport_share_of_paper():
    labels = ["FTL", "CES", "LTL"]
    colors = ['lightgreen', 'lightcoral', 'lightskyblue']
    plt.figure(figsize=(8, 8))
    plt.pie([2.28, 25.26, 72.46], labels=labels, colors=colors, autopct='%1.1f%%', shadow=False, startangle=140)
    plt.axis('equal')
    plt.show()


def cost_suddivision():
    values = [
        df.groupby("n_suppliers").trans_costs.mean().mean(),
        df.groupby("n_suppliers").order_cost.mean().mean(),
        df.groupby("n_suppliers").load_car_rent.mean().mean(),
        df.groupby("n_suppliers").load_car_invest.mean().mean()
    ]
    total = sum(values)
    values_percent = [v / total * 100 for v in values]
    categories = ['Transportation', 'Order', 'Load carrier rental', 'Load carrier invest']
    positions = range(len(categories))
    bar_width = 0.4
    plt.bar(positions, values_percent, bar_width)
    plt.xticks([p for p in positions], categories)
    plt.xlabel('Categories')
    plt.ylabel('Total costs (%)')
    plt.ylim(0, 80)
    for i, v in enumerate(values_percent):
        plt.text(i, v + 1, f'{v:.1f}%', ha='center', va='bottom', fontweight='bold')
    plt.tight_layout()
    plt.show()


def cost_suddivision_of_paper():
    values = [71.61, 2.87, 2.91, 22.61]
    total = sum(values)
    values = [v / total * 100 for v in values]
    categories = ['Transportation', 'Order', 'Load carrier rental', 'Load carrier invest']
    positions = range(len(categories))
    bar_width = 0.4
    plt.bar(positions, values, bar_width)
    plt.xticks([p for p in positions], categories)
    plt.xlabel('Categories')
    plt.ylabel('Total costs (%)')
    plt.ylim(0, 80)
    for i, v in enumerate(values):
        plt.text(i, v + 1, f'{v:.1f}%', ha='center', va='bottom', fontweight='bold')
    plt.tight_layout()
    plt.show()


plot_obj_value_for_suppliers()
plot_gap_for_suppliers()
plot_execution_time_for_suppliers()
plot_pie_chart_of_transport_share()
plot_pie_chart_of_trasport_share_of_paper()
cost_suddivision()
cost_suddivision_of_paper()
