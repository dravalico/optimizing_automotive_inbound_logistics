import gurobipy as gp
from src.notation.sets_and_params import *

exam = gp.Model()
exam.modelSense = gp.GRB.MINIMIZE

# Decision variables
# Indicating if supplier i in L
v_i_m = exam.addVar(vtype=gp.GRB.BINARY, name="v_i_m",
                    column=[(i, m) for i in L for m in M])
p_ij_m = exam.addVar(vtype=gp.GRB.BINARY, name="p_ij_m",
                     column=[(i, m, j) for i in L for m in M for j in D])
tau_ij = exam.addVar(vtype=gp.GRB.BINARY, name="tau_ij",
                     column=[(i, j) for i in L for j in D])
gamma_i = exam.addVar(vtype=gp.GRB.BINARY, name="gamma_i",
                      column=[i for i in L])
q_ij_m = exam.addVar(lb=0, ub=1, vtype=gp.GRB.CONTINUOUS, name="q_ij_m",
                     column=[(i, m, j) for i in L for m in M for j in D])
s_ij = exam.addVar(lb=0, ub=gp.GRB.INFINITY, vtype=gp.GRB.CONTINUOUS, name="s_ij",
                   column=[(i, j) for i in L for j in [0, D]])
beta_io = exam.addVar(vtype=gp.GRB.BINARY, name="beta_io",
                      column=[(o, i) for o in O for i in L])
n_ij = exam.addVar(lb=0, ub=gp.GRB.INFINITY, vtype=gp.GRB.INTEGER, name="n_ij",
                   column=[(i, j) for i in L for j in D])
n_ij_ec = exam.addVar(lb=0, ub=gp.GRB.INFINITY, vtype=gp.GRB.INTEGER, name="n_ij_ec",
                      column=[(i, j) for i in L for j in D])
n_jz_LTL = exam.addVar(lb=0, ub=gp.GRB.INFINITY, vtype=gp.GRB.INTEGER, name="n_jz_LTL",
                       column=[(z, j) for z in Z for j in D])
w_bij = exam.addVar(lb=0, ub=gp.GRB.INFINITY, vtype=gp.GRB.CONTINUOUS, name="w_bij",
                    column=[(b, i, j) for b in Q for i in L for j in D])
w_bij_ec = exam.addVar(lb=0, ub=gp.GRB.INFINITY, vtype=gp.GRB.CONTINUOUS, name="w_bij_ec",
                       column=[(b, i, j) for b in Q for i in L for j in D])
w_kij_CES = exam.addVar(lb=0, ub=gp.GRB.INFINITY, vtype=gp.GRB.CONTINUOUS, name="w_bij_CES",
                        column=[(k, i, j) for k in K for i in L for j in D])
omega_i_ec = exam.addVar([], vtype=gp.GRB.INFINITY)  # TODO
alpha_bij = exam.addVar(vtype=gp.GRB.BINARY, name="alpha_bij",
                        column=[(b, i, j) for b in Q for i in L for j in D])
alpha_bij_ec = exam.addVar(vtype=gp.GRB.BINARY, name="alpha_bij_ec",
                           column=[(b, i, j) for b in Q for i in L for j in D])
delta_kij = exam.addVar(vtype=gp.GRB.BINARY, name="delta_kij",
                        column=[(k, i, j) for k in K for i in L for j in D])
