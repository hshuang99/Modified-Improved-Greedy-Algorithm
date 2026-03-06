import operations
import cost_function
import sys
import random
import copy
from RowGreedy import rowGreedy
from ColGreedy import colGreedy
from row_or_Col_Greedy import row_or_Col
from ParallelGreedy import parallelGreedy
ALL_COST_MAT_NAME = {"sum": "1", "sq": "2", "cube": "3", "fourth": "4", "log": "-1"}
REVERSED = {v: k for k, v in ALL_COST_MAT_NAME.items()}
'''
This function will execute the four kind of greedy algorithm depends on type parameter
- Row
- Column
- Row_or_Column
- Parallel
'''
def modifiedImprovedGreedy(mat, matName, greedy, p_value, occur):
    # Define variables
    SIZE = len(mat); depth = 0
    minm = sys.float_info.max; minm_size = sys.float_info.max; minm_cost = sys.float_info.max
    origin = copy.deepcopy(mat); inverse = operations.inv(mat)
    row_visi = [0]*SIZE; col_visi = [0]*SIZE
    #Layer_r and Layer_c
    L_r = []; L_c = []
    #Layers_r and Layers_c
    Ls_r = []; Ls_c = []
    row_op = []; col_op = []
    L_row = []; L_col = []
    flag = False

    match greedy:
        case "Row":
            L_r, L_c, Ls_r, Ls_c, L_row, L_col, mat, row_op, col_op, row_visi, col_visi, depth, flag = rowGreedy(mat, inverse, L_r, L_c, Ls_r, Ls_c, L_row, L_col, row_visi, col_visi, row_op, col_op, p_value, flag, depth)
        case "Col":
            L_r, L_c, Ls_r, Ls_c, L_row, L_col, mat, row_op, col_op, row_visi, col_visi, depth, flag = colGreedy(mat, inverse, L_r, L_c, Ls_r, Ls_c, L_row, L_col, row_visi, col_visi, row_op, col_op, p_value, flag, depth)
        case "Row_or_Col":
            L_r, L_c, Ls_r, Ls_c, L_row, L_col, mat, row_op, col_op, row_visi, col_visi, depth, flag = row_or_Col(mat, inverse, L_r, L_c, Ls_r, Ls_c, L_row, L_col, row_visi, col_visi, row_op, col_op, p_value, flag, depth)
        case "Parallel":
            L_r, L_c, Ls_r, Ls_c, L_row, L_col, mat, row_op, col_op, row_visi, col_visi, depth, flag = parallelGreedy(mat, inverse, L_r, L_c, Ls_r, Ls_c, L_row, L_col, row_visi, col_visi, row_op, col_op, p_value, flag, depth)

    if flag:
        return

    #check the last iteration
    if len(L_r) > 0:
        Ls_r.append(L_r)
        L_r = []
        row_visi = [0]*SIZE
        L_row = []
    if len(L_c) > 0:
        Ls_c.append(L_c)
        L_c = []
        col_visi = [0]*SIZE
        L_col = []
    #check the matrix is different from origin matrix
    reduce = copy.deepcopy(origin)
    size = 0
    for r_op in row_op:
        reduce = operations.row_i2j(reduce, r_op[0], r_op[1])
        size += 1
    for c_op in col_op:
        reduce = operations.col_i2j(reduce, c_op[0], c_op[1])
        size += 1

    ok = True
    if ((reduce != mat).all()):
        ok = False
        
    if (depth > minm or (depth == minm and size >= minm_size) or not ok):
        return

    #update depth and amounts of CNOT
    minm = depth
    size_minm = size

    #create the permutation matrix
    per = [0]*SIZE
    for i in range(SIZE):
        for j in range(SIZE):
            if mat[i][j] == 1:
                per[i] = j

    #create the operation sequence
    seq = []
    for op_c in col_op:
        seq.append((op_c[0], op_c[1], 1))
    for op_r in reversed(row_op):
        seq.append((per[op_r[0]], per[op_r[1]], 0))

    
    #create layers for operations
    layers = []
    for lay_c in Ls_c:
        nl_c = []
        for l_c in lay_c:
            nl_c.append((l_c[0], l_c[1], 1))
        layers.append(nl_c)
    
    Ls_r.reverse()
    for lay_r in Ls_r:
        nl_r = []
        for l_r in lay_r:
            nl_r.append((per[l_r[0]], per[l_r[1]], 0))
        layers.append(nl_r)

    #Verify the Layers is work
    correct = operations.Verify(origin, layers, seq, mat)
    if correct:
        with open(f"{greedy}_{matName}-{SIZE}-block_{REVERSED[p_value]}_Layer_Results", "a") as f:
            for l in layers:
                for lay in l:
                    f.write("(%d %d %d)|" % (lay[0], lay[1], lay[2]))
                f.write("\n")
            f.write("CNOT: %d, depth: %d and cost function: %s occurs in %d\n" % (len(seq), len(layers), REVERSED[p_value], occur))
        f.close()
        
        #store the operations from sequence
        with open(f"{greedy}_{matName}-{SIZE}-block_{REVERSED[p_value]}_Sequence_Results", "a") as f:
            for i in seq:
                f.write("%d, %d, %d\n" % (i[0], i[1], i[2]))
            f.write("CNOT: %d\n" % (len(seq)))
        f.close()

    print(f"{SIZE}-block size that depth is: ", minm, " and size is: ", size_minm)
    print(f"The select cost function is {REVERSED[p_value]} and used in {matName} matrix")
