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


num_iterations = 10
start_time = time.time()

for i in range(num_iterations):
    model.optimize()
    if model.status == GRB.OPTIMAL:
        optimal_value = model.objVal
        print("Iteration", i + 1, "- Optimal objective value:", optimal_value)
    else:
        print("Iteration", i + 1, "- No solution found or optimization failed.")

end_time = time.time()
total_time = end_time - start_time

print("Benchmark completed.")
print("Total time:", total_time, "seconds")
print("Average time per iteration:", total_time / num_iterations, "seconds")
