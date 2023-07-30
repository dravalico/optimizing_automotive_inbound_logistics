import pandas as pd


def filter_dataframe_based_on(df, n_suppliers_value, LTL_zones_value, horizon_value):
    df['obj_value'] = pd.to_numeric(df['obj_value'], errors='coerce')
    df = df.dropna(subset=['obj_value'])
    filtered_data = df[
        (df["n_suppliers"] == n_suppliers_value) &
        (df["LTL_zones"] == LTL_zones_value) &
        (df["horizon"] == horizon_value)
        ]
    return filtered_data


suppliers = [25, 50, 75, 100]

# Print results for models with valid inequalities
df_full = pd.read_csv("../../results/collected_data.csv")
for supplier in suppliers:
    data_full = filter_dataframe_based_on(df_full, supplier, 34, 10)[["execution_time", "obj_gap"]]
    print(f"Mean runtime for {supplier} suppliers: {data_full['execution_time'].mean()}")
    print(f"Mean gap for {supplier} suppliers: {data_full['obj_gap'].mean()}")
    print(f"Optimal runs for {supplier} suppliers: {(data_full['obj_gap'] == 0.0).sum()}/{len(data_full['obj_gap'])}\n")

# Print results for models without valid inequalities
df_no_vi = pd.read_csv("../../results/collected_data_noVI.csv")
for supplier in suppliers:
    data_no_ci = filter_dataframe_based_on(df_no_vi, supplier, 34, 10)[["execution_time", "obj_gap"]]
    print(f"Mean runtime for {supplier} suppliers: {data_no_ci['execution_time'].mean()}")
    print(f"Gap for {supplier} suppliers: {data_no_ci['obj_gap'].mean()}\n")
