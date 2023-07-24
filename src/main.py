from gurobipy import GRB, quicksum
import dataset.sets
import model
import time
from datetime import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt
import importlib
import sys
from src.dataset.params import *


def save_variables_to_file():
    log_file = open("../results/output.log", "w")
    for var in model.model.getVars():
        if var.x != 0 or var.x != 0.0:
            s = str(var.VarName) + ": " + str(var.x) + '\n'
            log_file.write(s)
    log_file.close()


def plot_dataframe(df_to_plot):
    plt.figure(figsize=(10, 6))
    plt.scatter(df_to_plot["n_suppliers"], df_to_plot["execution_time"], marker='o')
    plt.xlabel("Suppliers")
    plt.ylabel("Execution Time")
    plt.show()


def calculate_transportation_cost_FTL(C_i_D, n_ij, n_ij_ec):
    return quicksum(C_i_D[i] * (n_ij[i, j] + n_ij_ec[i, j]) for i in L for j in D).getValue()


def calculate_transportation_cost_LTL(B_ib_p, w_bij, w_bij_ec):
    return quicksum(
        B_ib_p[b, i]["cost"] * (w_bij[b, i, j] + w_bij_ec[b, i, j]) for i in L for j in D for b in Q).getValue()


def calculate_transportation_cost_CES(B_k_pCES, delta_kij):
    return quicksum(B_k_pCES[k]["cost"] * delta_kij[k, i, j] for i in L for j in D for k in K).getValue()


def calculate_transportation_cost(C_i_D, n_ij, n_ij_ec, B_k_pCES, delta_kij, B_ib_p, w_bij, w_bij_ec):
    return calculate_transportation_cost_FTL(C_i_D, n_ij, n_ij_ec) + \
        calculate_transportation_cost_LTL(B_ib_p, w_bij, w_bij_ec) + \
        calculate_transportation_cost_CES(B_k_pCES, delta_kij)


def calculate_order_cost(A, p_ij_m):
    return A * quicksum(p_ij_m[i, j, m] for m in M for j in D for i in L).getValue()


def calculate_load_carrier_rental_cost(D, C_i_dR, u_io_R, beta_io):
    return len(D) * quicksum(C_i_dR[i] * u_io_R[i, o] * beta_io[i, o] for i in L for o in O).getValue()


def calculate_load_carrier_invest_cost(D, C_i_dI, u_io_I, beta_io):
    return len(D) * quicksum(C_i_dI[i] * u_io_I[i, o] * beta_io[i, o] for i in L for o in O).getValue()


def share_suppliers_FTL(v_i_m):
    count_FTL = 0
    for i in L:
        if v_i_m[i, 0].x == 1:
            count_FTL += 1
    return count_FTL / sets.n_suppliers * 100


def share_suppliers_LTL(v_i_m):
    count_LTL = 0
    for i in L:
        if v_i_m[i, 2].x == 1:
            count_LTL += 1
    return count_LTL / sets.n_suppliers * 100


def share_suppliers_CES(v_i_m):
    count_CES = 0
    for i in L:
        if v_i_m[i, 1].x == 1:
            count_CES += 1
    return count_CES / sets.n_suppliers * 100


BASE_PATH_OPTIMIZATION = "../results/"
if not os.path.isdir(BASE_PATH_OPTIMIZATION):
    os.mkdir(BASE_PATH_OPTIMIZATION)
BASE_PATH_MODEL = "../persistence/"
if not os.path.isdir(BASE_PATH_MODEL):
    os.mkdir(BASE_PATH_MODEL)
now = str(datetime.now().strftime("%Y%m%d%H%M%S"))
# today_res_path = os.path.join(BASE_PATH_MODEL, "model_" + now)
# if not os.path.isdir(today_res_path):
# os.mkdir(today_res_path)

sets = dataset.sets.get_instance()
CSV_PATH = os.path.join(BASE_PATH_OPTIMIZATION, "obj_func_data_" + now + ".csv")
num_iterations = 2
suppliers_options = [((v + 1) * 25) for v in range(6)]
LTL_zones_options = [10, 20, 34]
horizon_options = [10, 20]

for supplier in suppliers_options:
    sets.n_suppliers = supplier
    for zone in LTL_zones_options:
        sets.LTL_zones = zone
        for horizon in horizon_options:
            sets.horizon = horizon
            instance_results = []
            for instance in range(num_iterations):
                start_time = time.time()
                model.model.optimize()
                total_time = time.time() - start_time
                run_result = {
                    "start_time": datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f"),
                    "execution_time": total_time,
                    "part_numbers": sets.part_numbers,
                    "n_suppliers": sets.n_suppliers,
                    "LTL_zones": sets.LTL_zones,
                    "horizon": sets.horizon
                }
                if model.model.status in (GRB.OPTIMAL, GRB.SUBOPTIMAL):
                    optimal_value = model.model.objVal
                    print("Iteration", instance + 1, "for", supplier, "suppliers for", zone, "zones in", horizon,
                          "days - Optimal objective value:", optimal_value)
                    run_result["obj_value"] = model.model.objVal
                    run_result["obj_bound"] = model.model.ObjBound
                    run_result["obj_gap"] = model.model.MIPGap
                    run_result["trans_costs"] = calculate_transportation_cost(C_i_D, model.n_ij, model.n_ij_ec,
                                                                              B_k_pCES, model.delta_kij, B_ib_p,
                                                                              model.w_bij, model.w_bij_ec)
                    run_result["order_cost"] = calculate_order_cost(A, model.p_ij_m)
                    run_result["load_car_rent"] = calculate_load_carrier_rental_cost(D, C_i_dR, u_io_R, model.beta_io)
                    run_result["load_car_invest"] = calculate_load_carrier_invest_cost(D, C_i_dI, u_io_I, model.beta_io)
                    run_result["share_suppl_FTL"] = share_suppliers_FTL(model.v_i_m)
                    run_result["share_suppl_CES"] = share_suppliers_CES(model.v_i_m)
                    run_result["share_suppl_LTL"] = share_suppliers_LTL(model.v_i_m)
                else:
                    print("Iteration", instance + 1, "for", supplier, "suppliers for", zone, "zones in", horizon,
                          "days - No solution found or optimization failed.")
                    run_result["error"] = "no solution found"
                # model.model.write(os.path.join(today_res_path, str(instance) + ".lp"))  # FIXME naming cause overlap
                instance_results.append(run_result)
                if "src.dataset.params" in sys.modules:
                    del sys.modules["src.dataset.params"]
                from src.dataset.params import *

                importlib.reload(sys.modules["src.dataset.params"])
                importlib.reload(model)
            for e in instance_results:
                df = pd.DataFrame([e])
                if os.path.isfile(CSV_PATH):
                    df.to_csv(CSV_PATH, mode='a', header=False, index=False)
                else:
                    df.to_csv(CSV_PATH, index=False)
print("Benchmark completed.")
