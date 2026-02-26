import operations
import cost_function
import sys
import selector
import configparser

def parallelGreedy(mat, inverse, L_r, L_c, Ls_r, Ls_c, L_row, L_col, row_visi, col_visi, row_op, col_op, CostFunction, inputNormType, inputPValue, flag, depth):
    SIZE = len(mat)
    minm_cost = sys.float_info.max  # Initialize with current cost
    select_list = []
    B_row = []
    B_col = []
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read('ParallelConfig.ini')
    LIMIT = int(config.get('DEPTH', 'parallelLimit'))
    one = False

    best_row_cst = sys.float_info.max
    best_col_cst = sys.float_info.max

    stuck_counter = 0
    max_stuck_iterations = 3

    #go through the matrix and execute the row operations
    #outter while check matrix whether permutation
    while not operations.is_permutation_matrix(mat):
        print("\n=== Starting new iteration ===")
        print("Current depth:", depth)
        print("Current cost:", minm_cost)
        print("Row visited:", row_visi)
        print("Col visited:", col_visi)
        L_row = []
        L_col = []

        select_list = []
        L_row_cst = []
        L_col_cst = []


        B_row = []
        B_col = []
        
        minm_cost = cost_function.selector("global", CostFunction, mat, inverse, inputNormType, inputPValue)
        print("Current cost:", minm_cost)

        L_row = operations.L_collection(L_row, row_visi, SIZE)
        L_col = operations.L_collection(L_col, col_visi, SIZE)

        if not one:
            B_row, best_row_cst, minm_cost = selector.modified_available_row_operator_selection(L_row, L_row_cst, mat, inverse, CostFunction, inputNormType, inputPValue, minm_cost, best_row_cst, B_row)

        B_col, best_col_cst, minm_cost = selector.modified_available_col_operator_selection(L_col, L_col_cst, mat, inverse, CostFunction, inputNormType, inputPValue, minm_cost, best_col_cst, B_col)

        print("The B_row and best_row_cst:", B_row, best_row_cst)
        print("The B_col and best_col_cst:", B_col, best_col_cst)
        print("The length of B_row:", len(B_row))
        print("The length of B_col:", len(B_col))

        is_stuck = len(B_row) == 0 and len(B_col) == 0

        if is_stuck:
            stuck_counter += 1
            print(f"WARNING: Local minima detected! Stuck counter: {stuck_counter}/{max_stuck_iterations}")
        else:
            stuck_counter = 0

        if stuck_counter >= max_stuck_iterations or (is_stuck and sum(row_visi) == 0 and sum(col_visi) == 0):
            print("=== ESCAPING LOCAL MINIMA ===")

            escapeCandidates = []

            escapeCandidates = selector.avoid_localMinima_available_row_operator_selection(L_row, mat, inverse, CostFunction, inputNormType, inputPValue, escapeCandidates)

            escapeCandidates = selector.avoid_localMinima_available_col_operator_selection(L_col, mat, inverse, CostFunction, inputNormType, inputPValue, escapeCandidates)

            if len(escapeCandidates) > 0:
                escapeCandidates.sort(key=lambda x: x[0])
                best_escape = escapeCandidates[0]

                print(f"Escaping with operations: ({best_escape[1]}, {best_escape[2]}, {best_escape[3]})")
                print(f"Accepting cost increase from {minm_cost} to {best_escape[0]}")

                select_list = [(best_escape[1], best_escape[2], best_escape[3])]
                minm_cost = best_escape[0]
                stuck_counter = 0
        else:
            select_list = B_row + B_col


            if best_row_cst < best_col_cst:
                minm_cost = best_row_cst
            elif best_row_cst > best_col_cst:
                minm_cost = best_col_cst
            else:
                minm_cost = best_col_cst

        print("The current select_list and minm cost: ", select_list, minm_cost)
         
        select_list, L_r, L_c, Ls_r, Ls_c, L_row, L_col, mat, inverse, row_op, col_op, row_visi, col_visi, depth, one = operations.available_operator_execution(select_list, L_r, L_c, Ls_r, Ls_c, L_row, L_col, mat, inverse, row_op, col_op, row_visi, col_visi, depth, SIZE, one)

        if depth > LIMIT:
            print(f"Depth {depth} over minimum limit {LIMIT}, so break this iteration")
            flag = True
        else:
            config['DEPTH'] = {'parallelLimit': depth}
            with open('ParallelConfig.ini', 'w') as configfile:
                config.write(configfile)

    return L_r, L_c, Ls_r, Ls_c, L_row, L_col, mat, row_op, col_op, row_visi, col_visi, depth, flag
