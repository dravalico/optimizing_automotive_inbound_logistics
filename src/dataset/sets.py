part_numbers = 3927
# n_suppliers = 570
n_suppliers = 30
# LTL_zones = 34
LTL_zones = 10
n_transportation_modes = 3
horizon = 10  # days
n_possible_orders = 6
types_of_load_carrier_storage_area = 3
n_weight_classes_LTL = 10
n_weight_classes_CES = 10
n_orders_on_six_months = 11400
ULC = 28
SLC = 419

# Sets
L = range(n_suppliers)  # Set of all suppliers
Z = range(LTL_zones)  # Set all zones/transport service providers
M = range(n_transportation_modes)  # Set of all transportation modes, 0: FTL, 1: CES, 2: LTL
D = range(1, horizon + 1)  # Set of 10 working days in a two-week horizon plus initial condition
O = range(n_possible_orders)  # Set of the number of possible orders [1, 2, 4, 6, 8, 10]
H = range(types_of_load_carrier_storage_area)  # Set of all types of load carrier storage area
Q = range(n_weight_classes_LTL)  # Set of all weight classes in the freight cost matrix of less than truckload
K = range(n_weight_classes_CES)  # Set of all weight classes in the freight cost matrix of courier and express service
