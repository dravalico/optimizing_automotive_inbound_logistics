import gurobipy
from src.notation.sets_and_params import *

exam = gurobipy.Model()
exam.modelSense = gurobipy.GRB.MINIMIZE

# Decision variables
v_i_m = exam.addVar([(i, m) for i in L for m in M], vtype=gurobipy.GRB.BINARY)
p_ij_m = exam.addVar([(i, m, j) for i in L for m in M for j in D], vtype=gurobipy.GRB.BINARY)
tau_ij = exam.addVar([(i, j) for i in L for j in D], vtype=gurobipy.GRB.BINARY)
gamma_i = exam.addVar([i for i in L], vtype=gurobipy.GRB.BINARY)
q_ij_m = exam.addVar([], vtype=gurobipy.GRB.INFINITY)  # TODO
s_ij = exam.addVar([], vtype=gurobipy.GRB.INFINITY)  # TODO
beta_io = exam.addVar([(o, i) for o in O for i in L], vtype=gurobipy.GRB.BINARY)
n_ij = exam.addVar([(i, j) for i in L for j in D], vtype=gurobipy.GRB.INTEGER)
n_ij_ec = exam.addVar([(i, j) for i in L for j in D], vtype=gurobipy.GRB.INTEGER)
n_jz_LTL = exam.addVar([(z, j) for z in Z for j in D], vtype=gurobipy.GRB.INTEGER)
w_bij = exam.addVar([], vtype=gurobipy.GRB.INFINITY)  # TODO
w_bij_ec = exam.addVar([], vtype=gurobipy.GRB.INFINITY)  # TODO
w_kij_CES = exam.addVar([], vtype=gurobipy.GRB.INFINITY)  # TODO
w_i_ec = exam.addVar([], vtype=gurobipy.GRB.INFINITY)  # TODO
alpha_bij = exam.addVar([], vtype=gurobipy.GRB.INFINITY)  # TODO
alpha_bij_ec = exam.addVar([(b, i, j) for b in Q for i in L for j in D], vtype=gurobipy.GRB.INTEGER)
sigma_kij = exam.addVar([(k, i, j) for k in K for i in L for j in D], vtype=gurobipy.GRB.INTEGER)
