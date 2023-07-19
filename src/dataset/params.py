import numpy as np
from src.dataset.generation.freight_cost_matrix import generate_freight_cost_matrix_LTL, \
    generate_freight_cost_matrix_CES
from src.dataset.generation.circulation_days_matrix import generate_circulation_days_matrix
from src.dataset.generation.lognormal_distribution import generate_samples
from src.dataset.sets import *

# Dataset
number_of_SKU_ordered = [max(1, int(i)) for i in generate_samples(1, 6.89, 110, part_numbers, 1, 99)]
daily_demand_of_SKUs_of_suppliers = [int(i) + 1 for i in
                                     generate_samples(1.41, 3439.98, 280573, n_suppliers, 0.5, 99.5)]
daily_demand_volume = generate_samples(0.00, 2.53, 69.70, n_suppliers, 1, 99)
daily_demand_weight = generate_samples(0.00, 357.74, 9994.02, n_suppliers, 1, 99)
load_carrier_rental_costs = generate_samples(0.00, 0.08, 1.27, n_suppliers, 1, 99)
load_carrier_invest_costs = generate_samples(0.00, 1.43, 133.33, n_suppliers, 0.1, 99.9)
distance_of_suppliers = generate_samples(6.0, 538.38, 2547.00, n_suppliers, 4, 96)

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

r_iz = np.zeros((len(L), len(Z)), dtype=int) # Allocation of supplier L to zone Z (1 if true, 0 if false)
for i in range(len(L)):
    row = np.random.choice(len(Z))
    r_iz[i, row] = 1
print(r_iz)
print("====")

# Parameters for transportation process
g_ij = np.random.rand(len(L), len(D)) + 0.5  # Parameter reflecting the minimum order weight per supplier per day
f_i_wq = abs(0.1 * np.random.randn(len(L)) + 5)  # Parameter reflecting the relationship between w_bij, q_ij [kg/m^3]
omega_LTL = 0  # Minimal weight required by regional forwarder service provider for the delivered parts [kg] # FIXME
Q_min = 1  # Minimum order quantity for CES and FTL [kg]

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
freight_cost_matrix_LTL = generate_freight_cost_matrix_LTL(Q, Z, L)
print(freight_cost_matrix_LTL)
print("====")

B_dtype = np.dtype([
    ("lb", np.int32),
    ("ub", np.int32),
    ("cost", np.float64)
])
B_ib_p = np.zeros(shape=(len(Q), len(L)), dtype=B_dtype)  # Prices of the weight class b in Q for LTL for i in L [€/kg]
for b in Q:
    for i in L:
        B_ib_p[b, i] = np.array((100 * b, 100 * (b + 1), freight_cost_matrix_LTL[b, i]), dtype=B_dtype)

B_k_pCES = np.zeros(shape=len(K), dtype=B_dtype)  # Prices of the weight class k in K for CES [€/kg]
for k in K:
    B_k_pCES[k] = np.array((80 * k, 80 * (k + 1), freight_cost_matrix_CES[k]), dtype=B_dtype)
