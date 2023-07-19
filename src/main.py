from model import model
from gurobipy import GRB

OPTIMIZE_LOG_PATH = "../results/log.log"
RESULTS_OUTPUT_PATH = "../results/output.log"


def run_model_and_save_output():
    model.setParam(GRB.Param.LogFile, OPTIMIZE_LOG_PATH)
    model.optimize()


def save_variables_to_file():
    log_file = open(RESULTS_OUTPUT_PATH, "w")
    for var in model.getVars():
        if var.x != 0 or var.x != 0.0:
            s = str(var.VarName) + ": " + str(var.x) + '\n'
            log_file.write(s)
    log_file.close()


run_model_and_save_output()
save_variables_to_file()
