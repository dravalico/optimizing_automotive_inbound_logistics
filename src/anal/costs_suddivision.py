import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('../../results/obj_func_data_20230726160608.csv')
grouped_data = df.groupby('n_suppliers').agg({
    'trans_costs': 'mean',
    'order_cost': 'mean',
    'load_car_rent': 'mean',
    'load_car_invest': 'mean'
}).reset_index()

categories = ['trans_costs', 'order_cost', 'load_car_rent', 'load_car_invest']
positions = range(len(grouped_data))
bar_width = 0.2
for i, category in enumerate(categories):
    plt.bar([p + i*bar_width for p in positions], grouped_data[category], bar_width, label=category)
plt.xticks([p + 1.5*bar_width for p in positions], grouped_data['n_suppliers'])
plt.xlabel('Suppliers')
plt.ylabel('Mean Values')
plt.title('Mean Values of Categories per Supplier')
plt.legend(title='Categories')
plt.tight_layout()
plt.show()
