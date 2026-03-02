import numpy as np
import sys
import os
from modifiedImprovedGreedy import modifiedImprovedGreedy
import threading
import itertools

ALL_GREEDY = ["Row", "Col", "LocalMinima", "Parallel"]
ALL_COST_FUNCTIONS = ["sum", "origin", "square", "cube", "fourth", "log", "norm"]
ALL_NORM_TYPES = ["L1", "L2", "Lp", "Linf"]
ALL_P_VALUES = ["3", "4"]

np.set_printoptions(threshold=sys.maxsize) #setting for print full numpy matrix
"""
The main function can specify the Greedy algorithm and Cost Function for single Matrix in times
"""
def main(Matrix, Greedy, CostFunction, inputNormType, inputPValue, times):
    matrix = np.loadtxt(Matrix, dtype=int)
    print(f"Loaded matrix shape: {matrix.shape}")  # debug to confirm
    print("The Load Block Cipher Data: ")
    print(matrix)
    filename = os.path.splitext(os.path.basename(Matrix))[0]
    for i in range(0, int(times)):
        modifiedImprovedGreedy(Greedy, matrix, filename, CostFunction, inputNormType, inputPValue, i)

"""
Spawn one thread per combination of (Greedy x CostFunction x NormType x PValue).
"""
def run_all_combinations(Matrix, times, greedy_list=ALL_GREEDY,
                                        cost_list=ALL_COST_FUNCTIONS,
                                        norm_list=ALL_NORM_TYPES,
                                        p_list=ALL_P_VALUES):
    combinations = []
    for greedy, cost in itertools.product(greedy_list, cost_list):
        if cost == "norm":
            # "norm" cost: iterate all norm types
            for norm in ALL_NORM_TYPES:
                if norm == "Lp":
                    # "Lp" norm: also iterate all p values
                    for p in ALL_P_VALUES:
                        combinations.append((greedy, cost, norm, p))
                else:
                    # other norms: p is irrelevant, fix to "0"
                    combinations.append((greedy, cost, norm, 0))
        else:
            # non-"norm" cost: norm and p are irrelevant, fix both
            combinations.append((greedy, cost, "", 0))

    print(f"[INFO] Running {len(combinations)} combinations in parallel...")
    threads = []
    for greedy, cost, norm, p in combinations:
        t = threading.Thread(
                target = main,
                args = (Matrix, greedy, cost, norm, p, times),
                name=f"{greedy}-{cost}-{norm}-{p}"
                )
        threads.append(t)

    for t in threads:
        t.start()
        print(f"[START] Thread: {t.name}")

    for t in threads:
        t.join()
        print(f"[DONE]  Thread: {t.name}")

    print("[INFO] All combinations completed.")

if __name__ == "__main__":
    if len(sys.argv) == 7:
        Matrix = sys.argv[1]
        Greedy = sys.argv[2]
        CostFunction = sys.argv[3]
        inputNormType = sys.argv[4]
        inputPValue = sys.argv[5]
        times = sys.argv[6]
        main(Matrix, Greedy, CostFunction, inputNormType, inputPValue, times)
    elif len(sys.argv) == 4 and sys.argv[2] == "all":
        Matrix = sys.argv[1]
        times = sys.argv[3]
        run_all_combinations(Matrix, times)
    else:
        print(f"Usage:")
        print(f"  Specific : python3 {sys.argv[0]} <matrix> <greedy> <cost_fn> <norm_type> <p_value> <times>")
        print(f"  All combos: python3 {sys.argv[0]} <matrix> all <times>")
        sys.exit(1)
