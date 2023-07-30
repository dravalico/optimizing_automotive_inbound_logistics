import pandas as pd
import matplotlib.pyplot as plt

FILE_PATH = "../../results/collected_data.csv"


def load_data_and_filter_by_zones_horizon(file_path, LTL_zones, horizon):
    df = pd.read_csv(file_path)
    df = df[
        (df["LTL_zones"] == LTL_zones) &
        (df["horizon"] == horizon)
        ]
    return df


def plot_obj_value_for_suppliers(df):
    means = df.groupby("n_suppliers").obj_value.mean()
    stds = df.groupby("n_suppliers").obj_value.std()
    plt.plot(means, label="Mean", marker='o')
    plt.xlabel("Number of suppliers")
    plt.ylabel("Objective value")
    plt.legend()
    plt.xticks(means.index)
    plt.fill_between(means.index, means - stds, means + stds, alpha=0.2, label="Standard deviation")
    plt.show()


def plot_gap_for_suppliers(df):
    means = df.groupby("n_suppliers").obj_gap.mean()
    stds = df.groupby("n_suppliers").obj_gap.std()
    plt.plot(means, label="Mean", marker='o')
    plt.xlabel("Number of suppliers")
    plt.ylabel("Objective gap")
    plt.legend()
    plt.xticks(means.index)
    plt.fill_between(means.index, means - stds, means + stds, alpha=0.2, label="Standard deviation")
    plt.show()


def plot_pie_chart_of_transport_share(values):
    labels = ["FTL", "CES", "LTL"]
    colors = ["lightgreen", "lightcoral", "lightskyblue"]
    plt.figure(figsize=(8, 8))
    plt.pie(values, labels=labels, colors=colors, autopct="%1.1f%%", shadow=False, startangle=140)
    plt.axis("equal")
    plt.show()


def cost_suddivision_barplot(values):
    total = sum(values)
    values = [v / total * 100 for v in values]
    categories = ["Transportation", "Order", "Load carrier rental", "Load carrier invest"]
    positions = range(len(categories))
    bar_width = 0.4
    plt.bar(positions, values, bar_width)
    plt.xticks([p for p in positions], categories)
    plt.xlabel("Categories")
    plt.ylabel("Total costs (%)")
    plt.ylim(0, 80)
    for i, v in enumerate(values):
        plt.text(i, v + 1, f"{v:.1f}%", ha="center", va="bottom", fontweight="bold")
    plt.tight_layout()
    plt.show()


df_full = load_data_and_filter_by_zones_horizon(FILE_PATH, 34, 10)
df_full['obj_value'] = pd.to_numeric(df_full['obj_value'], errors='coerce')
df_full = df_full.dropna(subset=['obj_value'])
plot_obj_value_for_suppliers(df_full)
plot_gap_for_suppliers(df_full)

values_from_df = [
    df_full.groupby("n_suppliers").share_suppl_FTL.mean().mean(),
    df_full.groupby("n_suppliers").share_suppl_CES.mean().mean(),
    df_full.groupby("n_suppliers").share_suppl_LTL.mean().mean()
]
plot_pie_chart_of_transport_share(values_from_df)
values_on_paper = [2.28, 25.26, 72.46]
plot_pie_chart_of_transport_share(values_on_paper)

values_from_df = [
    df_full.groupby("n_suppliers").trans_costs.mean().mean(),
    df_full.groupby("n_suppliers").order_cost.mean().mean(),
    df_full.groupby("n_suppliers").load_car_rent.mean().mean(),
    df_full.groupby("n_suppliers").load_car_invest.mean().mean()
]
cost_suddivision_barplot(values_from_df)
values_on_paper = [71.61, 2.87, 2.91, 22.61]
cost_suddivision_barplot(values_on_paper)
