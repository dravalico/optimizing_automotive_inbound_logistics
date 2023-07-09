import gurobipy
from gurobipy import Model
import numpy

exam: Model = gurobipy.Model()
exam.modelSense = gurobipy.GRB.MINIMIZE

# Sets
L = range(570)  # Set of all suppliers
Z = range(34)  # Set all zones/transport service providers
M = range(3)  # Set of all transportation modes, 1: FTL, 2: CES, 3: LTL
D = range(10)  # Set of 10 working days in a two-week horizon
O: list[int] = [1, 2, 4, 6, 8, 10]  # Set of the number of possible orders
H = range(2)  # Set of all types of load carrier storage area
Q = range(10)  # Set of all weight classes in the freight cost matrix of less than truckload
K = range(10)  # Set of all weight classes in the freight cost matrix of courier and express service

# Parameters of suppliers
# TODO Generate d_i from skewed distribution
d_i = numpy.random.randn(1, len(L))  # Demand of supplier i in L per day [#/day]
r_iz = numpy.random.randint(2, size=(len(L), len(Z)))  # Allocation of supplier L to zone Z (1 if true, 0 if false)

# Parameters for transportation process
f_i_wq = numpy.random.randn(1, len(L))  # Parameter reflecting the relationship between w_ij and q_ij [kg/m^3]
omega_LTL = 30  # Minimal weight required by regional forwarder service provider for the delivered parts [kg]
Q_min = 30  # Minimum order quantity for CES and FTL [kg]

# Parameters for goods-entry
Cap_GI = 20  # Capacity regarding goods [# trucks/day]
Cap_WK = 40  # Capacity regarding goods-entry for courier and express service [# trucks/day]
Cap_h = numpy.random.randint(10000, 20000, len(H))  # Capacity in storage area h in H [storage places]
Cap_L = 80  # Volume capacity of a FTL truck [m^3]
Cap_WL = 22000  # Weight capacity of a FTL truck [kg]
Cap_K = 3500  # Weight capacity of a CES truck [kg]

# Parameters for the warehouse
SS_i = 200 * numpy.ones(len(L), dtype=int)  # Safety stock for supplier i in L [storage places]
f_hi_qp = (1 / 1.92) * numpy.ones((len(H), len(L)), dtype=int)  # Coefficient from volume to storage places

# Parameters for planning and cost calculation
C_i_D =  # Fix cost for direct transportation per truck for i in L [€]
B_ib_p =  # Prices of the weight class b in B for LTL for i in L [€/kg]
B_k_pCES =  # Prices of the weight class k in K for CES [€/kg]
f_i_SLC =  # Parameter indicating if supplier i in L needs any SLC for the shipment [€]
C_i_dR = 0.08  # Rental cost for load carriers for supplier i in L to satisfy one day's demand [€/day]
C_i_dI = 1.43  # Investment cost for load carriers supplier i in L to satisfy one day's demand [€/day]
u_io_R =  # Circulation days for universal load carriers i in L and O in O [days]
u_io_I =  # Circulation days for SLC, i in L and o in O [days]
A =  # Order cost per order
