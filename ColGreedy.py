import operations
import cost_function
import copy
import sys
import writers
import selector
import generator
import numpy as np
import random
import configparser

def ColGreedy(mat, CostFunction, inputNormType, inputPValue, occur):
    '''
    Define variables
    '''
    depth = 0
    SIZE = len(mat)
    minm = sys.float_info.max
    minm_size = sys.float_info.max
    minm_cost = sys.float_info.max
    origin = copy.deepcopy(mat)
    inverse = operations.inv(mat)
    row_visi = [0]*SIZE
    col_visi = [0]*SIZE
    #Layer_r and Layer_c
    L_r = []
    L_c = []
    #Layers_r and Layers_c
    Ls_r = []
    Ls_c = []
    row_op = []
    col_op = []
    select_list = []
    one = False
    normType = ""
    pValue = 0
    config = configparser.ConfigParser()
    config.read('ColConfig.ini')
    LIMIT = int(config.get('DEPTH', 'colLimit'))

    if CostFunction == "norm":
        #normType = input("Please select a Type for norm cost function, e.g. L1, L2, Lp, Linf: ")
        normType = inputNormType
        if normType == "Lp":
            #pValue = input("Please decide the p value for Lp, e.g., 3, 4, ...: ")
            pValue = inputPValue
    else:
        normType = ""
        pValue = 0

    '''
    According to the paper the greedy algorithm will limited for double SIZE
    '''
    while not operations.is_permutation_matrix(mat):
        print("\n=== Starting new iteration ===")
        print("Current depth:", depth)
        print("Current Row visited list:", row_visi)
        print("Current Col visited list:", col_visi)
        select_list.clear()
        L_row = []
        L_col = []
        L_row_cst = []
        L_col_cst = []

        minm_cost = cost_function.selector("global", CostFunction, mat, inverse, normType, pValue)
        print("Current Minm Cost:", minm_cost)

        for i in range(0, SIZE):
            if row_visi[i] == 1:
                continue
            for j in range(0, SIZE):
                if row_visi[j] == 1 or j == i:
                    continue
                L_row.append((i, j))

        for i in range(0, SIZE):
            if col_visi[i] == 1:
                continue
            for j in range(0, SIZE):
                if col_visi[j] == 1 or j == i:
                    continue
                L_col.append((i, j))

        #if the matrix is not achieve can depth one property
        if not one:
            for op_col in L_col:
                tmp_mat = operations.col_i2j(mat, op_col[0], op_col[1])
                tmp_inv = operations.row_i2j(inverse, op_col[1], op_col[0])
                L_col_cst.append(cost_function.selector("Column", CostFunction, tmp_mat, tmp_inv, normType, pValue))
            
            for index, col_op_cst in enumerate(L_col_cst):
                if col_op_cst < minm_cost:
                    select_list.clear()
                    op = (L_col[index][0], L_col[index][1], 1)
                    select_list.append(op)
                    minm_cost = col_op_cst
 
        for op_row in L_row:
            tmp_mat = operations.row_i2j(mat, op_row[0], op_row[1])
            tmp_inv = operations.col_i2j(inverse, op_row[1], op_row[0])
            L_row_cst.append(cost_function.selector("Row", CostFunction, tmp_mat, tmp_inv, normType, pValue))

        for index, row_op_cst in enumerate(L_row_cst):
            if row_op_cst < minm_cost:
                select_list.clear()
                op = (L_row[index][0], L_row[index][1], 0)
                select_list.append(op)
                minm_cost = row_op_cst

        print("The select list and current minm cost: ", select_list, minm_cost)
                    
        if len(select_list) == 0:
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
            if operations.can_depth_one(mat):
                one = True
        else:
            rand = random.randint(0, len(select_list)-1)
            select_operator = select_list[rand]
            if select_operator[2] == 0:
                mat = operations.row_i2j(mat, select_operator[0], select_operator[1])
                inverse = operations.col_i2j(inverse, select_operator[1], select_operator[0])
                L_r.append((select_operator[0], select_operator[1], 0))
                row_op.append((select_operator[0], select_operator[1], 0))
                if sum(row_visi) == 0:
                    depth = depth+1
                row_visi[select_operator[0]] = 1
                row_visi[select_operator[1]] = 1
                print("Currently Row operations:", row_op)
            else:
                mat = operations.col_i2j(mat, select_operator[0], select_operator[1])
                inverse = operations.row_i2j(inverse, select_operator[1], select_operator[0])
                L_c.append((select_operator[0], select_operator[1], 1))
                op = (select_operator[0], select_operator[1], 1)
                col_op.append(op)
                if sum(col_visi) == 0:
                    depth = depth+1
                col_visi[select_operator[0]] = 1
                col_visi[select_operator[1]] = 1
                print("Currently Column oeprations:", col_op)
                

        if depth > LIMIT:
            print(f"Depth {depth} over minimum limit {LIMIT}, so break this iteration")
            return
        else:
            config['DEPTH'] = {'colLimit': depth}
            with open('config.ini', 'w') as configfile:
                config.write(configfile)

    '''
    check the last iteration
    '''
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

    '''
    check the matrix is different from origin matrix
    '''
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
    
    '''
    Verify the Layers is work
    '''
    correct = operations.Verify(origin, layers, seq, mat)

    if correct:
        with open(f"Col_{SIZE}-block_Layer_Results", "a") as f:
            for l in layers:
                for lay in l:
                    f.write("(%d %d %d)|" % (lay[0], lay[1], lay[2]))
                f.write("\n")
            if CostFunction == "norm":
                if inputNormType == "Lp":
                    f.write("CNOT: %d, depth: %d and cost function: %s with %s and p value: %s occur in %d\n" % (len(seq), len(layers), CostFunction, inputNormType, inputPValue, occur))
                else:
                    f.write("CNOT: %d, depth: %d and cost function: %s with %s occur in %d\n" % (len(seq), len(layers), CostFunction, inputNormType, occur))
            else:
                f.write("CNOT: %d, depth: %d and cost function: %s occur in %d\n" % (len(seq), len(layers), CostFunction, occur))
        f.close()

        #store the operations from sequence
        with open(f"Col_{SIZE}-block_Sequence_Results", "a") as f:
            for i in seq:
                f.write("%d, %d, %d\n" % (i[0], i[1], i[2]))
            f.write("CNOT: %d\n" % (len(seq)))
        f.close()

    print(str(SIZE) + "-block size for Square Cost that the depth is: ", minm, " and size is: ", size_minm)
    print(f"The select cost function used in {SIZE} matrix and cost function: {CostFunction}")
