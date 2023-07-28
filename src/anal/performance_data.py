import pandas as pd

df = pd.read_csv('../../results/obj_func_data_20230726160608.csv')


def filter_dataframe_based_on(df_data, n_suppliers_value, LTL_zones_value, horizon_value):
    filtered_data = df_data[
        (df_data['n_suppliers'] == n_suppliers_value) &
        (df_data['LTL_zones'] == LTL_zones_value) &
        (df_data['horizon'] == horizon_value)
        ]
    return filtered_data


suppliers = [25, 50, 75, 100]

for supplier in suppliers:
    data = filter_dataframe_based_on(df, supplier, 34, 10)[['execution_time', 'obj_gap']]
    print(f"Mean runtime for {supplier} suppliers: {data['execution_time'].mean()}")
    print(f"Mean gap for {supplier} suppliers: {data['obj_gap'].mean()}")
    print(f"Optimal runs for {supplier} suppliers: {(data['obj_gap'] == 0.0).sum()}/{len(data['obj_gap'])}\n")

df1 = pd.read_csv('../../results/obj_func_data_20230728091234_noCI.csv')
for supplier in suppliers:
    data = filter_dataframe_based_on(df, supplier, 34, 10)['obj_value']
    data_no_ci = filter_dataframe_based_on(df1, supplier, 34, 10)['obj_value']
    print(data.mean())
    print(data_no_ci.mean())
    print(f"Delta obj for {supplier} suppliers: {abs(data.mean() - data_no_ci.mean()) / data.mean() * 100}\n")
