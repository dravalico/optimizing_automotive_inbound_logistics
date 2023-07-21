from gurobipy import GRB
import model
import time
from datetime import datetime
import os
from dataset.sets import *
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


BASE_PATH_OPTMIZATION = "../results/"
if not os.path.isdir(BASE_PATH_OPTMIZATION):
    os.mkdir(BASE_PATH_OPTMIZATION)
BASE_PATH_MODEL = "../persistence/"
if not os.path.isdir(BASE_PATH_MODEL):
    os.mkdir(BASE_PATH_MODEL)
today_res_path = os.path.join(BASE_PATH_MODEL, str(datetime.now().strftime("%Y-%m-%d_%H:%M:%S")))
if not os.path.isdir(today_res_path):
    os.mkdir(today_res_path)

num_iterations = 10
df = pd.DataFrame()
model.model.Params.OutputFlag = 0

for i in range(num_iterations):
    start_time = time.time()
    model.model.optimize()
    total_time = time.time() - start_time
    run_result = {
        "start_time": datetime.now().strftime("%Y-%m-%d_%H:%M:%S.%f"),
        "execution_time": total_time,
        "part_numbers": part_numbers,
        "n_suppliers": n_suppliers,
        "LTL_zones": LTL_zones,
        "horizon": horizon
    }
    if model.model.status == GRB.OPTIMAL:
        optimal_value = model.model.objVal
        print("Iteration", i + 1, "- Optimal objective value:", optimal_value)
        run_result["obj_value"] = model.model.objVal
        run_result["obj_bound"] = model.model.ObjBound
        run_result["obj_gap"] = model.model.MIPGap
    else:
        print("Iteration", i + 1, "- No solution found or optimization failed.")
        run_result["error"] = "no solution found"
    df = pd.concat([df, pd.DataFrame([run_result])], ignore_index=True)
    model.model.write(os.path.join(today_res_path, str(i) + ".lp"))
    importlib.reload(model)

CSV_PATH = os.path.join(BASE_PATH_OPTMIZATION, "obj_func_data.csv")
if os.path.isfile(CSV_PATH):
    df.to_csv(CSV_PATH, mode='a', header=False, index=False)
else:
    df.to_csv(CSV_PATH, index=False)

print("Benchmark completed.")
plot_dataframe(pd.read_csv(CSV_PATH))
