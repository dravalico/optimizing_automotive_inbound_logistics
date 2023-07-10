from src.dataset.lognormal_distribution import generate_samples, print_general_statistics

part_numbers = 3927
n_suppliers = 570
n_orders_on_six_months = 11400
LTL_zones = 34
ULC = 28
SLC = 419

number_of_SKU_ordered = [max(1, int(i)) for i in generate_samples(1, 6.89, 110, part_numbers, 1, 99)]
print_general_statistics(number_of_SKU_ordered, "Part numbers [#]")

daily_demand_of_SKUs_of_suppliers = generate_samples(1.41, 3439.98, 280573, n_orders_on_six_months, 0.5, 99.5)
print_general_statistics(daily_demand_of_SKUs_of_suppliers, "Daily demand of SKUs of suppliers [# SKUs/day]")

load_carrier_rental_costs = generate_samples(0.00, 0.08, 1.27, n_suppliers, 1, 99)
print_general_statistics(load_carrier_rental_costs, "Load carrier rental costs")

load_carrier_invest_costs = generate_samples(0.00, 1.43, 133.33, n_suppliers, 0.1, 99.9)
print_general_statistics(load_carrier_invest_costs, "Load carrier invest costs")

distance_of_suppliers = generate_samples(6.0, 538.38, 2547.00, n_suppliers, 4, 96)
print_general_statistics(distance_of_suppliers, "Distance of suppliers")
