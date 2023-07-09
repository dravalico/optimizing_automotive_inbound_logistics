from entity.Order import Order
from entity.Part import Part
from lognormal_distribution import generate_samples, print_general_statistics

part_numbers = 3927
n_suppliers = 570
n_orders_on_six_months = 11400
LTL_zones = 34
ULC = 28
SLC = 419

distance_of_suppliers = generate_samples(6.0, 538.38, 2547.00, n_suppliers, 5, 95)
print_general_statistics(distance_of_suppliers, "Distance of suppliers")

load_carrier_invest_costs = generate_samples(0.00, 1.43, 133.33, n_orders_on_six_months, 0.01, 99.9)
print_general_statistics(load_carrier_invest_costs, "Load carrier invest costs")

load_carrier_rental_costs = generate_samples(0.00, 0.08, 1.27, n_orders_on_six_months, 1, 99)
print_general_statistics(load_carrier_rental_costs, "Load carrier rental costs")

number_of_SKU_ordered = [max(1, int(i)) for i in generate_samples(1, 6.89, 110, part_numbers, 1, 99)]
print_general_statistics(number_of_SKU_ordered, "Part numbers [#]")

part1 = Part(1, 10, 2)
part2 = Part(2, 20, 4)
order = Order([part1, part2])
print(order.total_volume)
print(order.total_weight)