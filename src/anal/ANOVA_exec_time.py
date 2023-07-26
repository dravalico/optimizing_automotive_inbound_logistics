import pandas as pd
from scipy.stats import f_oneway
import matplotlib.pyplot as plt

data = pd.read_csv('../../results/obj_func_data_20230724173836.csv')

# Perform one-way ANOVA for n_suppliers
groups_n_suppliers = [group_data['execution_time'] for _, group_data in data.groupby('n_suppliers')]
anova_n_suppliers = f_oneway(*groups_n_suppliers)
print("One-way ANOVA for n_suppliers:")
print("F-statistic:", anova_n_suppliers.statistic)
print("p-value:", anova_n_suppliers.pvalue)

# Perform one-way ANOVA for LTL_zones
groups_LTL_zones = [group_data['execution_time'] for _, group_data in data.groupby('LTL_zones')]
anova_LTL_zones = f_oneway(*groups_LTL_zones)
print("\nOne-way ANOVA for LTL_zones:")
print("F-statistic:", anova_LTL_zones.statistic)
print("p-value:", anova_LTL_zones.pvalue)

# Perform one-way ANOVA for horizon
groups_horizon = [group_data['execution_time'] for _, group_data in data.groupby('horizon')]
anova_horizon = f_oneway(*groups_horizon)
print("\nOne-way ANOVA for horizon:")
print("F-statistic:", anova_horizon.statistic)
print("p-value:", anova_horizon.pvalue)

n_suppliers = data['n_suppliers']
horizon = data['horizon']
execution_time = data['execution_time']
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_trisurf(n_suppliers, horizon, execution_time, cmap='viridis', edgecolor='none')
ax.set_xlabel('n_suppliers')
ax.set_ylabel('horizon')
ax.set_zlabel('execution_time')
plt.show()
