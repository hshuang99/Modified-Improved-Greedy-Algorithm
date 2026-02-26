import operations
import cost_function
import sys
import selector
import configparser

def colGreedy(mat, inverse, L_r, L_c, Ls_r, Ls_c, L_row, L_col, row_visi, col_visi, row_op, col_op, CostFunction, inputNormType, inputPValue, flag, depth):
    SIZE = len(mat)
    minm_cost = sys.float_info.max
    select_list = []
    one = False
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read('ColConfig.ini')
    LIMIT = int(config.get('DEPTH', 'colLimit'))

    while not operations.is_permutation_matrix(mat):
        print("\n=== Starting new iteration ===")
        print("Current depth:", depth)
        print("Current Row visited list:", row_visi)
        print("Current Col visited list:", col_visi)
        select_list = []
        L_row = []
        L_col = []
        L_row_cst = []
        L_col_cst = []

        minm_cost = cost_function.selector("global", CostFunction, mat, inverse, inputNormType, inputPValue)
        print("Current Minm Cost:", minm_cost)

        L_row = operations.L_collection(L_row, row_visi, SIZE)
        L_col = operations.L_collection(L_col, col_visi, SIZE)

        #if the matrix is not achieve can depth one property
        if not one:
            select_list, minm_cost = selector.available_col_operator_selection(L_col, L_col_cst, mat, inverse, CostFunction, inputNormType, inputPValue, minm_cost, select_list)
 
        select_list, minm_cost = selector.available_row_operator_selection(L_row, L_row_cst, mat, inverse, CostFunction, inputNormType, inputPValue, minm_cost, select_list)

        print("The select list and current minm cost: ", select_list, minm_cost)
                    
        select_list, L_r, L_c, Ls_r, Ls_c, L_row, L_col, mat, inverse, row_op, col_op, row_visi, col_visi, depth, one = operations.available_operator_execution(select_list, L_r, L_c, Ls_r, Ls_c, L_row, L_col, mat, inverse, row_op, col_op, row_visi, col_visi, depth, SIZE, one)  

        if depth > LIMIT:
            print(f"Depth {depth} over minimum limit {LIMIT}, so break this iteration")
            flag = True

    return L_r, L_c, Ls_r, Ls_c, L_row, L_col, mat, row_op, col_op, row_visi, col_visi, depth, flag
