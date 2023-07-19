from model import model
from gurobipy import GRB
import time


def save_variables_to_file():
    log_file = open("../results/output.log", "w")
    for var in model.getVars():
        if var.x != 0 or var.x != 0.0:
            s = str(var.VarName) + ": " + str(var.x) + '\n'
            log_file.write(s)
    log_file.close()
