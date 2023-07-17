import numpy as np
from src.dataset.dataset import n_suppliers, LTL_zones, distance_of_suppliers, daily_demand_of_SKUs_of_suppliers, \
    load_carrier_invest_costs, load_carrier_rental_costs
from src.dataset.freight_cost_matrix import generate_freight_cost_matrix_LTL, generate_freight_cost_matrix_CES
from src.dataset.circulation_days_matrix import generate_circulation_days_matrix

# Sets
L = range(n_suppliers)  # Set of all suppliers
Z = range(LTL_zones)  # Set all zones/transport service providers
M = range(3)  # Set of all transportation modes, 0: FTL, 1: CES, 2: LTL
D = range(1, 11)  # Set of 10 working days in a two-week horizon plus initial condition
O = range(6)  # Set of the number of possible orders [1, 2, 4, 6, 8, 10]
H = range(3)  # Set of all types of load carrier storage area # TODO Update model with 4 storage areas
Q = range(10)  # Set of all weight classes in the freight cost matrix of less than truckload
K = range(10)  # Set of all weight classes in the freight cost matrix of courier and express service

# Parameters of suppliers
d_i = daily_demand_of_SKUs_of_suppliers  # Demand of supplier i in L per day [#/day]
r_iz = np.random.randint(2, size=(len(L), len(Z)))  # Allocation of supplier L to zone Z (1 if true, 0 if false)

# Parameters for transportation process
g_ij = np.random.rand(len(L), len(D)) + 0.5  # Parameter reflecting the minimum order weight per supplier per day
f_i_wq = 1 * np.random.randn(len(L)) + 50000  # Parameter reflecting the relationship between w_bij and q_ij [kg/m^3]
omega_LTL = 30  # Minimal weight required by regional forwarder service provider for the delivered parts [kg]
Q_min = 30  # Minimum order quantity for CES and FTL [kg]

# Parameters for goods-entry
Cap_GI = 85  # Capacity regarding goods [# trucks/day]
Cap_WK = 40  # Capacity regarding goods-entry for courier and express service [# trucks/day]
Cap_h = np.random.randint(low=1500000, high=3000000, size=len(H))  # Capacity in storage area h in H [storage places]
Cap_L = 80  # Volume capacity of a FTL truck [m^3]
Cap_WL = 22000  # Weight capacity of a FTL truck [kg]
Cap_K = 3500  # Weight capacity of a CES truck [kg]

# Parameters for the warehouse
SS_i = 200 * np.ones(len(L), dtype=int)  # Safety stock for supplier i in L [storage places]
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

freight_cost_matrix = generate_freight_cost_matrix_LTL(Q, Z, L)
my_dtype = np.dtype([
    ("lb", np.int32),
    ("ub", np.int32),
    ("cost", np.float64)
])
B_ib_p = np.zeros(shape=(len(Q), len(L)), dtype=my_dtype)  # Prices of the weight class b in Q for LTL for i in L [€/kg]
for b in Q:
    for i in L:
        B_ib_p[b, i] = np.array((100 * b, 100 * (b + 1), freight_cost_matrix[b, i]), dtype=my_dtype)

# Define a dictionary with the desired lb and ub for each variable
lb_dict = {
    (b, i, j): 100 * b
    for b in Q
    for i in L
    for j in D
}
ub_dict = {
    (b, i, j): 100 * (b + 1)
    for b in Q
    for i in L
    for j in D
}
