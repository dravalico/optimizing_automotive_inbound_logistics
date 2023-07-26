import numpy as np
from src.dataset.generation.freight_cost_matrix import generate_freight_cost_matrix_LTL, \
    generate_freight_cost_matrix_CES
from src.dataset.generation.circulation_days_matrix import generate_circulation_days_matrix
from src.dataset.generation.lognormal_distribution import generate_samples
import src.dataset.sets

sets = src.dataset.sets.get_instance()

# Sets
L = range(sets.n_suppliers)  # Set of all suppliers
Z = range(sets.LTL_zones)  # Set all zones/transport service providers
M = range(sets.n_transportation_modes)  # Set of all transportation modes, 0: FTL, 1: CES, 2: LTL
D = range(1, sets.horizon + 1)  # Set of 10 working days in a two-week horizon plus initial condition
O = range(sets.n_possible_orders)  # Set of the number of possible orders [1, 2, 4, 6, 8, 10]
H = range(sets.types_of_load_carrier_storage_area)  # Set of all types of load carrier storage area
Q = range(sets.n_weight_classes_LTL)  # Set of all weight classes in the freight cost matrix of less than truckload
K = range(
    sets.n_weight_classes_CES)  # Set of all weight classes in the freight cost matrix of courier and express service

# Dataset
number_of_SKU_ordered = [max(1, int(i)) for i in generate_samples(1, 6.89, 110, sets.part_numbers)]
daily_demand_of_SKUs_of_suppliers = [int(i) + 1 for i in generate_samples(1.41, 3439.98, 280573.60, sets.n_suppliers)]
daily_demand_volume = generate_samples(0.00, 2.53, 69.70, sets.n_suppliers)
daily_demand_weight = generate_samples(0.00, 357.74, 9994.02, sets.n_suppliers)
load_carrier_rental_costs = generate_samples(0.00, 0.08, 1.27, sets.n_suppliers)
load_carrier_invest_costs = generate_samples(0.00, 1.43, 133.33, sets.n_suppliers)
distance_of_suppliers = generate_samples(6.0, 538.38, 2547.00, sets.n_suppliers)

# Parameters of suppliers
demand = daily_demand_of_SKUs_of_suppliers  # Demand of supplier i in L per day [#/day]
d_i_dtype = np.dtype([
    ("demand", np.int32),
    ("total_weight", np.float64),
    ("total_volume", np.float64)
])
d_i = np.zeros(len(L), dtype=d_i_dtype)
for i in L:
    d_i[i] = np.array((demand[i], demand[i] * (np.mean(daily_demand_weight) / np.mean(demand)),
                       demand[i] * (np.mean(daily_demand_volume) / np.mean(demand))), dtype=d_i_dtype)

r_iz = np.zeros((len(L), len(Z)), dtype=int)  # Allocation of supplier L to zone Z (1 if true, 0 if false)
for i in range(len(L)):
    row = np.random.choice(len(Z))
    r_iz[i, row] = 1

# Parameters for transportation process
g_ij = np.random.rand(len(L), len(D)) + 0.5  # Parameter reflecting the minimum order weight per supplier per day
f_i_wq = abs(0.1 * np.random.randn(len(L)) + 5)  # Parameter reflecting the relationship between w_bij, q_ij [kg/m^3]
omega_LTL = 0  # Minimal weight required by regional forwarder service provider for the delivered parts [kg] # FIXME
Q_min = 150  # Minimum order quantity for CES and FTL [kg]

# Parameters for goods-entry
Cap_GI = 30  # Capacity regarding goods [# trucks/day]
Cap_WK = 40  # Capacity regarding goods-entry for courier and express service [# trucks/day]
Cap_h = 25000 * np.ones(len(H), dtype=int)  # Capacity in storage area h in H [storage places]
Cap_L = 80  # Volume capacity of a FTL truck [m^3]
Cap_WL = 22000  # Weight capacity of a FTL truck [kg]
Cap_K = 3500  # Weight capacity of a CES truck [kg]

# Parameters for the warehouse
SS_i = 0.2 * np.ones(len(L), dtype=int)  # Safety stock for supplier i in L [storage places]
f_hi_qp = (1 / 1.92) * np.ones((len(L), len(H)))  # Coefficient from volume to storage places

# Parameters for planning and cost calculation
# TODO Implement piece-wise linear cost-per-km function
C_i_D = [(500 + 1.0 * v) for v in distance_of_suppliers]  # Fix cost for transportation per truck for i in L [€]
f_i_SLC = np.random.randint(2, size=len(L))  # Parameter indicating if supplier i in L needs any SLC for the shipment
C_i_dR = load_carrier_rental_costs  # Rental cost for load carriers for supplier i in L to satisfy day demand [€/day]
C_i_dI = load_carrier_invest_costs  # Investment cost for load carriers supplier i in L to satisfy day demand [€/day]
u_io_R = generate_circulation_days_matrix(L, O)  # Circulation days for universal load carriers i in L and o in O [days]
u_io_I = generate_circulation_days_matrix(L, O)  # Circulation days for SLC, i in L and o in O [days]
A = 50  # Order cost per order [€]

freight_cost_matrix_CES = generate_freight_cost_matrix_CES(K)
freight_cost_matrix_LTL = generate_freight_cost_matrix_LTL(r_iz, Q, Z, L)

B_dtype = np.dtype([
    ("lb", np.int32),
    ("ub", np.int32),
    ("cost", np.float64)
])
Q_interval = 5
B_ib_p = np.zeros(shape=(len(Q), len(L)), dtype=B_dtype)  # Prices of the weight class b in Q for LTL for i in L [€/kg]
for b in Q:
    for i in L:
        B_ib_p[b, i] = np.array((Q_interval * b, Q_interval * (b + 1), freight_cost_matrix_LTL[b, i]), dtype=B_dtype)

K_interval = 5
B_k_pCES = np.zeros(shape=len(K), dtype=B_dtype)  # Prices of the weight class k in K for CES [€/kg]
for k in K:
    B_k_pCES[k] = np.array((K_interval * k, K_interval * (k + 1), freight_cost_matrix_CES[k]), dtype=B_dtype)
