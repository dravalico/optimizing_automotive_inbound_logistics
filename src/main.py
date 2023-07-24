from gurobipy import GRB, quicksum
import dataset.sets
import model
import time
from datetime import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt
import importlib


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


BASE_PATH_OPTIMIZATION = "../results/"
if not os.path.isdir(BASE_PATH_OPTIMIZATION):
    os.mkdir(BASE_PATH_OPTIMIZATION)
BASE_PATH_MODEL = "../persistence/"
if not os.path.isdir(BASE_PATH_MODEL):
    os.mkdir(BASE_PATH_MODEL)
now = str(datetime.now().strftime("%Y%m%d%H%M%S"))
today_res_path = os.path.join(BASE_PATH_MODEL, "model_" + now)
if not os.path.isdir(today_res_path):
    os.mkdir(today_res_path)

sets = dataset.sets.get_instance()
CSV_PATH = os.path.join(BASE_PATH_OPTIMIZATION, "obj_func_data_" + now + ".csv")
num_iterations = 5
suppliers_options = [((v + 1) * 25) for v in range(3)]
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
                    print("Iteration", instance + 1, "for", supplier, "suppliers - Optimal objective value:",
                          optimal_value)
                    run_result["obj_value"] = model.model.objVal
                    run_result["obj_bound"] = model.model.ObjBound
                    run_result["obj_gap"] = model.model.MIPGap

                else:
                    print("Iteration", instance + 1, "for", supplier,
                          "suppliers - No solution found or optimization failed.")
                    run_result["error"] = "no solution found"
                model.model.write(os.path.join(today_res_path, str(instance) + ".lp"))  # FIXME naming cause overlap
                instance_results.append(run_result)
                importlib.reload(model)
            df = pd.DataFrame([instance_results])
            if os.path.isfile(CSV_PATH):
                df.to_csv(CSV_PATH, mode='a', header=False, index=False)
            else:
                df.to_csv(CSV_PATH, index=False)
print("Benchmark completed.")
