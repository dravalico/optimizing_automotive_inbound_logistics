import pandas as pd

df = pd.read_csv('../../results/obj_func_data_20230726160608.csv')


def retrieve_performance_data_based_on_suppliers(n_suppliers_value, LTL_zones_value, horizon_value):
    filtered_data = df[
        (df['n_suppliers'] == n_suppliers_value) &
        (df['LTL_zones'] == LTL_zones_value) &
        (df['horizon'] == horizon_value)
        ]
    return filtered_data[['execution_time', 'obj_gap']]


suppliers = [25, 50, 75, 100]
for supplier in suppliers:
    data = retrieve_performance_data_based_on_suppliers(supplier, 34, 10)
    print(f"Mean runtime for {supplier} suppliers: {data['execution_time'].mean()}")
    print(f"Mean gap for {supplier} suppliers: {data['obj_gap'].mean()}")
    print(f"Optimal runs for {supplier} suppliers: {(data['obj_gap'] == 0.0).sum()}/{len(data['obj_gap'])}\n")
