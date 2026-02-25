import numpy as np
import operations
import cost_function
import sys
import random
import copy
from RowGreedy import rowGreedy

'''
This function will execute the four kind of greedy algorithm depends on type parameter
- Row/Column
- Column/Row
- LocalMinima
- Parallel
'''
def modifiedImprovedGreedy(greedyType, mat, matName, CostFunction, inputNormType, inputPValue, occur):
    # Define variables
    SIZE = len(mat); depth = 0
    minm = sys.float_info.max; minm_size = sys.float_info.max; minm_cost = sys.float_info.max
    origin = copy.deepcopy(mat); inverse = operations.inv(mat)
    row_visi = [0]*SIZE; col_visi = [0]*SIZE
    #Layer_r and Layer_c
    L_r = []; L_c = []
    #Layers_r and Layers_c
    Ls_r = []; Ls_c = []
    L_row = []; L_col = []
    row_op = []; col_op = []
    flag = False

    match greedyType:
        case "Row":
            L_r, L_c, Ls_r, Ls_c, row_visi, col_visi, L_row, L_col, row_op, col_op, depth, flag = rowGreedy(mat, inverse, SIZE, CostFunction, inputNormType, inputPValue, flag)

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

    '''
    update depth and amounts of CNOT
    '''
    minm = depth
    size_minm = size

    '''
    create the permutation matrix
    '''
    per = [0]*SIZE
    for i in range(SIZE):
        for j in range(SIZE):
            if mat[i][j] == 1:
                per[i] = j

    '''            
    create the operation sequence
    '''
    seq = []
    for op_c in col_op:
        seq.append((op_c[0], op_c[1], 1))
    for op_r in reversed(row_op):
        seq.append((per[op_r[0]], per[op_r[1]], 0))

    '''
    create layers for operations
    '''
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
        with open(f"{greedyType}_{SIZE}-block-{CostFunction}_Layer_Results", "a") as f:
            for l in layers:
                for lay in l:
                    f.write("(%d %d %d)|" % (lay[0], lay[1], lay[2]))
                f.write("\n")
            if CostFunction == "norm":
                if inputNormType == "Lp":
                    f.write("CNOT: %d, depth: %d and cost function: %s with %s and p value: %s occurs in %d\n" % (len(seq), len(layers), CostFunction, inputNormType, inputPValue, occur))
                else:
                    f.write("CNOT: %d, depth: %d and cost function: %s with %s occurs in %d\n" % (len(seq), len(layers), CostFunction, inputNormType, occur))
            else:
                f.write("CNOT: %d, depth: %d and cost function: %s occurs in %d\n" % (len(seq), len(layers), CostFunction, occur))
        f.close()
        
        #store the operations from sequence
        with open(f"{greedyType}_{SIZE}-block-{CostFunction}_Sequence_Results", "a") as f:
            for i in seq:
                f.write("%d, %d, %d\n" % (i[0], i[1], i[2]))
            f.write("CNOT: %d\n" % (len(seq)))
        f.close()

    print(f"{SIZE}-block size that depth is: ", minm, " and size is: ", size_minm)
    print(f"The select cost function is {CostFunction} and used in {matName} matrix")
