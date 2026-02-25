import operations
import cost_function

def available_row_operator_selection(L_row, mat, inverse, CostFunction, normType, pValue, minm_cost, op_list):
    L_row_cst = []
    for row_op in L_row:
        #execute the column operation from col_visi
        tmp_mat = operations.row_i2j(mat, row_op[0], row_op[1])
        tmp_inverse = operations.col_i2j(inverse, row_op[1], row_op[0]) #calculate the row operation on inverse
        L_row_cst.append(cost_function.selector("Row", CostFunction, tmp_mat, tmp_inverse, normType, pValue))

    for index, row_op_cst in enumerate(L_row_cst):
        if row_op_cst < minm_cost:
            op_list = []
            op_list.append((L_row[index][0], L_row[index][1], 0))
            minm_cost = row_op_cst
        elif row_op_cst == minm_cost:
            op_list.append((L_row[index][0], L_row[index][1], 0))
    return op_list, minm_cost
def available_col_operator_selection(L_col, mat, inverse, CostFunction, normType, pValue, minm_cost, op_list):
    L_col_cst = []
    for col_op in L_col:
        tmp_mat = operations.col_i2j(mat, col_op[0], col_op[1]) #execute the col operation on normal matrix
        tmp_inverse = operations.row_i2j(inverse, col_op[1], col_op[0]) #execute the column operation on inverse matrix
        L_col_cst.append(cost_function.selector("Column", CostFunction, tmp_mat, tmp_inverse, normType, pValue))

    #only if cost less than current cost underlying square col cost function
    for index, col_op_cst in enumerate(L_col_cst):
        if col_op_cst < minm_cost:
            op_list = [] #clear the select list
            op_list.append((L_col[index][0], L_col[index][1], 1))
            minm_cost = col_op_cst #update the new cost
        elif col_op_cst == minm_cost:
            op_list.append((L_col[index][0], L_col[index][1], 1))
    return op_list, minm_cost
