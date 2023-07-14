import gurobipy as gp
from gurobipy import quicksum
from src.notation.sets_and_params import *
from itertools import chain

model = gp.Model()

# Decision variables
# Indicating if supplier i ∈ L uses transportation mode m ∈ M
v_i_m = model.addVars([(i, m) for i in L for m in M], vtype=gp.GRB.BINARY, name="v_i_m")

# Indicating if supplier i ∈ L uses transportation mode m ∈ M on day j ∈ D
p_ij_m = model.addVars([(i, j, m) for i in L for j in D for m in M], vtype=gp.GRB.BINARY, name="p_ij_m")

# Indicating if delivery of supplier i ∈ L on day j ∈ D is above the daily demand
tau_ij = model.addVars([(i, j) for i in L for j in D], vtype=gp.GRB.BINARY, name="tau_ij")

# Indicating if a single delivery in the planning horizon is chosen for supplier i ∈ L
gamma_i = model.addVars([i for i in L], vtype=gp.GRB.BINARY, name="gamma_i")

# Percentage order quantity of the horizon demand for supplier i ∈ L using transportation mode m ∈ M on day j ∈ D
q_ij_m = model.addVars([(i, j, m) for i in L for j in D for m in M], lb=0, ub=1, vtype=gp.GRB.CONTINUOUS, name="q_ij_m")

# Percentage order quantity of the horizon demand for supplier i ∈ L using transportation mode m ∈ M on day j ∈ D
s_ij = model.addVars([(i, j) for i in L for j in chain(range(1), D)], lb=0, ub=gp.GRB.INFINITY, vtype=gp.GRB.CONTINUOUS,
                     name="s_ij")

# Indicating if order frequency o ∈ O is selected for supplier i ∈ L
beta_io = model.addVars([(o, i) for o in O for i in L], vtype=gp.GRB.BINARY, name="beta_io")

# Number of trucks of supplier i ∈ L on day j ∈ D for FTL / FTL empty load carrier return
n_ij = model.addVars([(i, j) for i in L for j in D], lb=0, ub=gp.GRB.INFINITY, vtype=gp.GRB.INTEGER, name="n_ij")

# Number of trucks of supplier i ∈ L on day j ∈ D for FTL / FTL empty load carrier return
n_ij_ec = model.addVars([(i, j) for i in L for j in D], lb=0, ub=gp.GRB.INFINITY, vtype=gp.GRB.INTEGER, name="n_ij_ec")

# Number of trucks for zone z ∈ Z on day j ∈ D for transport mode LTL
n_jz_LTL = model.addVars([(j, z) for j in D for z in Z], lb=0, ub=gp.GRB.INFINITY, vtype=gp.GRB.INTEGER,
                         name="n_jz_LTL")

# Weight of the order quantity for a weight range (B_b, B_b+1) from supplier, i ∈ L using LTL / LTL empty load carrier
# return on day j ∈ D
w_bij = model.addVars([(b, i, j) for b in Q for i in L for j in D], lb=0, ub=gp.GRB.INFINITY, vtype=gp.GRB.CONTINUOUS,
                      name="w_bij")

# Weight of the order quantity for a weight range (B_b, B_b+1) from supplier, i ∈ L using LTL / LTL empty load carrier
# return on day j ∈ D
w_bij_ec = model.addVars([(b, i, j) for b in Q for i in L for j in D], lb=0, ub=gp.GRB.INFINITY,
                         vtype=gp.GRB.CONTINUOUS, name="w_bij_ec")

# Weight of the order quantity for weight range (B_k−1_CES, B_k_CES) from supplier i ∈ L using CES on day j ∈ D
w_kij_CES = model.addVars([(k, i, j) for k in K for i in L for j in D], lb=0, ub=gp.GRB.INFINITY,
                          vtype=gp.GRB.CONTINUOUS, name="w_bij_CES")

# Weight of carriers to satisfy one days demand for supplier i ∈ L
omega_i_ec = model.addVars([i for i in L], lb=0, ub=gp.GRB.INFINITY, vtype=gp.GRB.CONTINUOUS)

# Indicator for weight range b ∈ Q selected for LTL/LTL empty load carrier returns from supplier i ∈ L on day j ∈ D
alpha_bij = model.addVars([(b, i, j) for b in Q for i in L for j in D], vtype=gp.GRB.BINARY, name="alpha_bij")

# Indicator for weight range b ∈ Q selected for LTL/LTL empty load carrier returns from supplier i ∈ L on day j ∈ D
alpha_bij_ec = model.addVars([(b, i, j) for b in Q for i in L for j in D], vtype=gp.GRB.BINARY, name="alpha_bij_ec")

# Indicator for weight range k ∈ K selected for CES from supplier i ∈ L on day j ∈ D
delta_kij = model.addVars([(k, i, j) for k in K for i in L for j in D], vtype=gp.GRB.BINARY, name="delta_kij")

# Objective function
# model.setObjective(
#     quicksum(C_i_D[i] * (n_ij[i, j] + n_ij_ec[i, j]) for i in L for j in D) +
#     quicksum(B_k_pCES[k] * delta_kij[k, i, j] for i in L for j in D for k in K) +
#     # FIXME IndexError: index 10 is out of bounds for axis 0 with size 10, line 71
#     quicksum(B_ib_p[i, b] * (w_bij[b, i, j] + w_bij_ec[b, i, j]) for i in L for j in D for b in Q) +
#     A * quicksum(p_ij_m[i, j, m] for i in L for j in D for m in M) +
#     len(D) * quicksum(  # FIXME TypeError: list indices must be integers or slices, not tuple, line 74
#         C_i_dR[i] * u_io_R[i, o] * beta_io[i, o] + C_i_dI[i] * u_io_I[i, o] * beta_io[i, o] for i in L for o in O),
#     gp.GRB.MINIMIZE
# )

# Constraints
for i in L:
    for k in D:  # TODO Check if sum to k or sum to (k+1)
        model.addConstr(quicksum(q_ij_m[i, j, m] + s_ij[i, 0] for m in M for j in range(1, k)) >= k / len(D),
                        name="2")

for i in L:
    model.addConstr(quicksum(q_ij_m[i, j, m] for m in M for j in D) == 1, name="3")

for i in L:
    for j in D:
        model.addConstr(quicksum(p_ij_m[i, j, m] for m in M) <= 1, name="4")

for i in L:
    for j in D:
        for m in M:
            model.addConstr(q_ij_m[i, j, m] <= p_ij_m[i, j, m], name="5")

for i in L:
    for j in D:
        for m in [0, 1]:
            model.addConstr(q_ij_m[i, j, m] >= Q_min / d_i[i] * p_ij_m[i, j, m], name="6")

for i in L:
    for j in D:
        model.addConstr(q_ij_m[i, j, 2] >= 1 / len(D) * p_ij_m[i, j, 2], name="7")

for i in L:
    model.addConstr(quicksum(v_i_m[i, m] for m in M) == 1, name="8")

for i in L:
    for j in D:
        for m in M:
            model.addConstr(p_ij_m[i, j, m] <= v_i_m[i, m], name="9")

for i in L:
    for j in range(len(D) // 2):
        for m in M:
            model.addConstr(p_ij_m[i, j, m] + gamma_i[i] >= p_ij_m[i, j + len(D) // 2, m], name="10")

for i in L:
    for j in range(1, (len(D) // 2) + 1):
        for m in M:
            model.addConstr(p_ij_m[i, j, m] <= p_ij_m[i, j + len(D) // 2, m] + gamma_i[i], name="11")

for i in L:
    model.addConstr(quicksum(p_ij_m[i, j, m] for j in D for m in M) <= 1 + len(D) * (1 - gamma_i[i]), name="12")

for i in L:
    model.addConstr(quicksum(q_ij_m[i, j, 2] for j in range(1, (len(D) // 2) + 1)) <=
                    quicksum(q_ij_m[i, j + len(D) // 2, 2] for j in range(1, (len(D) // 2) + 1)) + gamma_i[i],
                    name="13")

for j in D:
    model.addConstr(quicksum(n_ij[i, j] for i in L) + quicksum(n_jz_LTL[j, z] for z in Z) <= Cap_GI, name="14")

for j in D:
    model.addConstr(quicksum(p_ij_m[i, j, 1] for i in L) <= Cap_WK, name="15")

for i in L:
    for j in D[1:]:
        model.addConstr(s_ij[i, j - 1] + quicksum(q_ij_m[i, j, m] for m in M) - 1 / len(D) == s_ij[i, j], name="16")

for i in L:
    model.addConstr(s_ij[i, 0] + SS_i[i] + quicksum(q_ij_m[i, 1, m] for m in M) - 1 / len(D) == s_ij[i, 0], name="17")

for h in H:
    for j in D:
        model.addConstr(quicksum(f_hi_qp[h, i] * d_i[i] * s_ij[i, j] for i in L) <= Cap_h[h], name="18")

for i in L:
    for j in D:
        model.addConstr(quicksum(q_ij_m[i, j, m] for m in M) >= tau_ij[i, j] / len(D), name="19")

for i in L:
    model.addConstr(quicksum(tau_ij[i, j] for j in D) == quicksum(o * beta_io[i, o] for o in O), name="20")

for i in L:
    model.addConstr(quicksum(beta_io[i, o] for o in O) == 1, name="21")

for i in L:
    for j in D:
        model.addConstr(q_ij_m[i, j, 0] * d_i[i] <= Cap_L * n_ij[i, j], name="22")

for i in L:
    for j in D:
        model.addConstr(f_i_wq[i] * q_ij_m[i, j, 0] * d_i[i] <= Cap_WL * n_ij[i, j], name="23")

for i in L:
    for j in D:
        model.addConstr(f_i_SLC[i] * q_ij_m[i, j, 0] * d_i[i] <= Cap_L * n_ij_ec[i, j], name="24")

for i in L:
    for j in D:
        model.addConstr(f_i_SLC[i] * omega_i_ec[i] * q_ij_m[i, j, 0] <= Cap_WL * n_ij_ec[i, j], name="25")

for i in L:
    for j in D:
        model.addConstr(f_i_wq[i] * q_ij_m[i, j, 1] * d_i[i] <= Cap_K, name="26")

for i in L:
    for j in D:
        model.addConstr(f_i_wq[i] * q_ij_m[i, j, 2] * d_i[i] >= omega_LTL * g_ij[i, j - 1], name="27")

for j in D:
    for z in Z:
        model.addConstr(quicksum(r_iz[i, z] * q_ij_m[i, j, 0] * d_i[i] for i in L) <= Cap_L * n_jz_LTL[j, z], name="28")

for j in D:
    for z in Z:
        model.addConstr(
            quicksum(r_iz[i, z] * f_i_wq[i] * q_ij_m[i, j, 0] * d_i[i] for i in L) <= Cap_WL * n_jz_LTL[j, z],
            name="29")
