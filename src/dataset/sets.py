part_numbers = 3927
# n_suppliers = 570
n_suppliers = 30
n_orders_on_six_months = 11400
# LTL_zones = 34
LTL_zones = 10
ULC = 28
SLC = 419

# Sets
L = range(n_suppliers)  # Set of all suppliers
Z = range(LTL_zones)  # Set all zones/transport service providers
M = range(3)  # Set of all transportation modes, 0: FTL, 1: CES, 2: LTL
D = range(1, 11)  # Set of 10 working days in a two-week horizon plus initial condition
O = range(6)  # Set of the number of possible orders [1, 2, 4, 6, 8, 10]
H = range(3)  # Set of all types of load carrier storage area
Q = range(10)  # Set of all weight classes in the freight cost matrix of less than truckload
K = range(10)  # Set of all weight classes in the freight cost matrix of courier and express service
