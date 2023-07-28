import pandas as pd


def filter_dataframe_based_on(df, n_suppliers_value, LTL_zones_value, horizon_value):
    filtered_data = df[
        (df["n_suppliers"] == n_suppliers_value) &
        (df["LTL_zones"] == LTL_zones_value) &
        (df["horizon"] == horizon_value)
        ]
    return filtered_data


suppliers = [25, 50, 75, 100]

# Print results for models with cyclic constraints and valid inequalities
df_full = pd.read_csv("../../results/obj_func_data_20230726160608.csv")
for supplier in suppliers:
    data_full = filter_dataframe_based_on(df_full, supplier, 34, 10)[["execution_time", "obj_gap"]]
    print(f"Mean runtime for {supplier} suppliers: {data_full['execution_time'].mean()}")
    print(f"Mean gap for {supplier} suppliers: {data_full['obj_gap'].mean()}")
    print(f"Optimal runs for {supplier} suppliers: {(data_full['obj_gap'] == 0.0).sum()}/{len(data_full['obj_gap'])}\n")

# Print results for models without cyclic constraints and with valid inequalities
df_no_ci = pd.read_csv("../../results/obj_func_data_20230728095643_noCI.csv")
for supplier in suppliers:
    data_full = filter_dataframe_based_on(df_full, supplier, 34, 10)[["execution_time", "obj_value"]]
    data_no_ci = filter_dataframe_based_on(df_no_ci, supplier, 34, 10)[["execution_time", "obj_value"]]
    print(f"Mean runtime for {supplier} suppliers: {data_no_ci['execution_time'].mean()}")
    print(f"Delta obj for {supplier} suppliers: "
          f"{(data_no_ci['obj_value'].mean() - data_full['obj_value'].mean()) / data_full['obj_value'].mean() * 100}\n")
