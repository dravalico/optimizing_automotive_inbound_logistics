import numpy
from src.dataset.dataset import n_suppliers, LTL_zones, distance_of_suppliers, daily_demand_of_SKUs_of_suppliers, \
    load_carrier_invest_costs, load_carrier_rental_costs

# Sets
L = range(n_suppliers)  # Set of all suppliers
Z = range(LTL_zones)  # Set all zones/transport service providers
M = range(3)  # Set of all transportation modes, 1: FTL, 2: CES, 3: LTL
D = range(10)  # Set of 10 working days in a two-week horizon
O = [1, 2, 4, 6, 8, 10]  # Set of the number of possible orders
H = range(2)  # Set of all types of load carrier storage area
Q = range(10)  # Set of all weight classes in the freight cost matrix of less than truckload
K = range(10)  # Set of all weight classes in the freight cost matrix of courier and express service

# Parameters of suppliers
d_i = daily_demand_of_SKUs_of_suppliers  # Demand of supplier i in L per day [#/day]
r_iz = numpy.random.randint(2, size=(len(L), len(Z)))  # Allocation of supplier L to zone Z (1 if true, 0 if false)

# Parameters for transportation process
f_i_wq = numpy.random.randn(1, len(L))  # Parameter reflecting the relationship between w_ij and q_ij [kg/m^3]
omega_LTL = 30  # Minimal weight required by regional forwarder service provider for the delivered parts [kg]
Q_min = 30  # Minimum order quantity for CES and FTL [kg]

# Parameters for goods-entry
Cap_GI = 85  # Capacity regarding goods [# trucks/day]
Cap_WK = 40  # Capacity regarding goods-entry for courier and express service [# trucks/day]
Cap_h = numpy.random.randint(10000, 20000, len(H))  # Capacity in storage area h in H [storage places]
Cap_L = 80  # Volume capacity of a FTL truck [m^3]
Cap_WL = 22000  # Weight capacity of a FTL truck [kg]
Cap_K = 3500  # Weight capacity of a CES truck [kg]

# Parameters for the warehouse
SS_i = 200 * numpy.ones(len(L), dtype=int)  # Safety stock for supplier i in L [storage places]
f_hi_qp = (1 / 1.92) * numpy.ones((len(H), len(L)), dtype=int)  # Coefficient from volume to storage places

# Parameters for planning and cost calculation
# TODO Implement piece-wise linear cost-per-km function
C_i_D = [(500 + 1.0 * val) for val in distance_of_suppliers]  # Fix cost for transportation per truck for i in L [€]
# B_ib_p =  # Prices of the weight class b in Q for LTL for i in L [€/kg]
# B_k_pCES =  # Prices of the weight class k in K for CES [€/kg]
f_i_SLC = numpy.random.randint(2, len(L))  # Parameter indicating if supplier i in L needs any SLC for the shipment
C_i_dR = load_carrier_rental_costs  # Rental cost for load carriers for supplier i in L to satisfy one day's demand [€/day]
C_i_dI = load_carrier_invest_costs  # Investment cost for load carriers supplier i in L to satisfy one day's demand [€/day]
# u_io_R =  # Circulation days for universal load carriers i in L and o in O [days]
# u_io_I =  # Circulation days for SLC, i in L and o in O [days]
A = 50  # Order cost per order [€]
