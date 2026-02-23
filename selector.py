import operations
import cost_function
"""
def available_operator_selection(greedy_op, row_visited, col_visited, mat, inverse, minm_cost, op_list):
    L_r = []; L_c = []
    if greedy_op == "row":
        #generate candidate row operaton for layer according to empty temp row visited position
        for i in range(0, config.SIZE):
            for j in range(0, config.SIZE):
                if row_visited[i] == 0 and row_visited[j] == 0 and i != j:
                    L_r.append((i, j))
        #generate B_r using cnadidates
        for row_op in L_r:
            #execute the column operation from col_visi
            tmp_mat = operations.row_i2j(mat, row_op[0], row_op[1])
            tmp_inverse = operations.col_i2j(inverse, row_op[1], row_op[0]) #calculate the row operation on inverse
            tmp_cost = cost_function.H_sqr(tmp_mat, tmp_inverse)
            #only if cost less than current cost underlying square row cost function
            if tmp_cost < minm_cost:
                op_list.clear() #clear the select_list and push the available operator
                operator = (row_op[0], row_op[1], tmp_cost, 0) #in this choose is column operator so that record the 1
                op_list.append(operator) #append this operator to select_list as available operator
                minm_cost = tmp_cost #redueced success so that update the temp_row_minm_cost
                #update temp row visited positions i and j
                row_visited[row_op[0]] = 1
                row_visited[row_op[1]] = 1
        return op_list, minm_cost, row_visited
    elif greedy_op == "column":
        #generate candidate column operations for layer according to empty temp col visited position
        for k in range(0, config.SIZE):
            for l in range(0, config.SIZE):
                if col_visited[k] == 0 and col_visited[l] == 0 and k != l:
                    L_c.append((k, l))
        #generate B_c using candidates
        for col_op in L_c:
            tmp_mat = operations.col_i2j(mat, col_op[0], col_op[1]) #execute the col operation on normal matrix
            tmp_inverse = operations.row_i2j(inverse, col_op[1], col_op[0]) #execute the column operation on inverse matrix
            tmp_cost = cost_function.H_sqc(tmp_mat, tmp_inverse)
            #only if cost less than current cost underlying square col cost function
            if tmp_cost < minm_cost:
                op_list.clear() #clear the select list
                operator = (col_op[0], col_op[1], tmp_cost, 1) #the col  operation record the 0 according to the paper setting
                op_list.append(operator) #append to the select list
                minm_cost = tmp_cost #update the new cost
                #update tmep col visited positions i and j
                col_visited[col_op[0]] = 1
                col_visited[col_op[1]] = 1
        return op_list, minm_cost

def prod_available_operator_selection(col_visited, mat, inverse, minm_cost, select_list):
    prod_L_c = []
    #generate candidate column operations for layer according to empty temp col visited position
    for i in range(0, config.SIZE):
        for j in range(0, config.SIZE):
            if col_visited[i] == 0 and col_visited[j] == 0 and i != j:
                prod_L_c.append((i, j))
    for prod_col_op in prod_L_c:
        tmp_mat = operations.col_i2j(mat, prod_col_op[0], prod_col_op[1]) #execute the col operation on normal matrix
        tmp_inverse = operations.row_i2j(inverse, prod_col_op[1], prod_col_op[0]) #execute the column operation on inverse matrix
        tmp_cost = cost_function.H_prodc(tmp_mat, tmp_inverse)

        if tmp_cost < minm_cost:
            select_list.clear() #clear the select list
            operator = (prod_col_op[0], prod_col_op[1], tmp_cost, 1) #the col  operation record the 0 according to the paper setting
            select_list.append(operator) #append to the select list
            minm_cost = tmp_cost #update the new cost
            col_visited[prod_col_op[0]] = 1
            col_visited[prod_col_op[1]] = 1
    return select_list, minm_cost

def B_localminima_selection(B_r, B_c, select_list):
    B_r_minm_val = 0; B_c_minm_val = 0
    if len(B_r) > 0 and len(B_c) > 0:
        B_r_minm_val, B_r_minm_addr = operations.find_min_2d(B_r)
        B_c_minm_val, B_c_minm_addr = operations.find_min_2d(B_c)
        if B_r_minm_val < B_c_minm_val:
            select_list.append(B_r[B_r_minm_addr])
        elif B_r_minm_val == B_c_minm_val:
            select_list.append(B_c[B_c_minm_addr])
    elif len(B_r) > 0:
        B_r_minm_val, B_r_minm_addr = operations.find_min_2d(B_r)
        select_list.append(B_r[B_r_minm_addr])
    elif len(B_c) > 0:
        B_c_minm_val, B_c_minm_addr = operations.find_min_2d(B_c)
        select_list.append(B_c[B_c_minm_addr])
    return select_list
"""
