import numpy as np
import math

# ===============================================
# 1. Schaeffer and Perkowski: A Cost Minimization Approach to Synthesis of Linear Reversible Circuits
# ===============================================
def cost_origin(mat, inverse):
    identity = np.identity(len(mat))
    return float(np.sum(np.logical_xor(mat, identity).astype(int) + np.logical_xor(inverse, identity).astype(int)))

# ===============================================
# 2. Heuristic Function
# ===============================================
## Brugière: Gaussian elimination versus greedy methods for the synthesis of linear reversible circuits
def cost_sum(mat):
    ret = 0.0
    SIZE = len(mat)
    for i in range(SIZE):
        for j in range(SIZE):
            ret += mat[i][j]
    return ret

## Brugière: Gaussian elimination versus greedy methods for the synthesis of linear reversible circuits
def cost_prod(mat):
	row_counts = np.sum(mat, axis=1)
	non_zero_counts = row_counts[row_counts > 0]
	#return the calculated product row's Hamming weight
	return np.sum(np.log2(non_zero_counts))

## Shi and Feng: Quantum Circuits of AES with a Low-depth Linear Layer and a New Structure
def cost_sq(mat):
    ret = 0.0
    SIZE = len(mat)
    for i in range(0, SIZE): #row
        hammingWeight = 0.0
        for j in range(0, SIZE): #column
            if mat[i][j]: #non-zero entry
                hammingWeight +=  mat[i][j]
        ret += hammingWeight ** 2
    #return the calculated square row's Hamming weight
    return ret

def cost_cubic(mat):
    ret = 0.0
    SIZE = len(mat)
    for i in range(0, SIZE): #row
        hammingWeight = 0.0
        for j in range(0, SIZE): #column
            if mat[i][j]: #non-zero entry
                hammingWeight +=  mat[i][j]
        ret += hammingWeight ** 3
    #return the calculated square row's Hamming weight
    return ret

def cost_fourth(mat):
    ret = 0.0
    SIZE = len(mat)
    for i in range(0, SIZE): #row
        hammingWeight = 0.0
        for j in range(0, SIZE): #column
            if mat[i][j]: #non-zero entry
                hammingWeight +=  mat[i][j]
        ret += hammingWeight ** 4
    #return the calculated square row's Hamming weight
    return ret

def H_sum(mat, inverse):
    return cost_sum(mat) + cost_sum(inverse)

def H_sqr(mat, inverse):
    return cost_sq(mat)+cost_sq(np.transpose(inverse))

def H_cubr(mat, inverse):
    return cost_cubic(mat)+cost_cubic(np.transpose(inverse))

def H_four(mat, inverse):
    return cost_fourth(mat)+cost_fourth(np.transpose(inverse))

def H_sqc(mat, inverse):
    return cost_sq(np.transpose(mat)) + cost_sq(inverse)

def H_cubc(mat, inverse):
    return cost_cubic(np.transpose(mat)) + cost_cubic(inverse)

def H_fouc(mat, inverse):
    return cost_fourth(np.transpose(mat)) + cost_fourth(inverse)

def H_logr(mat, inverse):
    return cost_prod(mat) + cost_prod(np.transpose(inverse))

def H_logc(mat, inverse):
    return cost_prod(np.transpose(mat))+cost_prod(inverse)

def H_sq_maximum(mat, inverse):
    return max(H_sqr(mat, inverse), H_sqc(mat, inverse))

def H_cube_maximum(mat, inverse):
    return max(H_cubr(mat, inverse), H_cubc(mat, inverse))

def H_fourth_maximum(mat, inverse):
    return max(H_four(mat, inverse), H_fouc(mat, inverse))

def H_log_maximum(mat, inverse):
    return max(H_logr(mat, inverse), H_logc(mat, inverse))

# ===================================================
# 3. L-Norm Cost Function
# ===================================================
def L_Norm(mat, inverse, normType, pValue): #Decide operator cost
    norm_cost = 0.0
    H_r = cost_sum(mat) + cost_sum(np.transpose(inverse)) # X
    H_c = cost_sum(np.transpose(mat)) + cost_sum(inverse) # Y
    if normType == "L1": # Manhattan norm cost function
        norm_cost = H_r + H_c
    elif normType == "L2": # Euclidean norm cost function
        norm_cost = math.sqrt((H_r ** 2) + (H_c ** 2))
    elif normType == "Lp": # Generalized norm cost function, p = 3, 4, ....
        norm_cost = ((H_r ** int(pValue)) + (H_c ** int(pValue))) ** (1/int(pValue))
    elif normType == "Linf": # Maximum norm cost function
        norm_cost = max(H_r, H_c) #paper's method
    return norm_cost

"""
Selector for combine different kind of maximum cost function and operator cost function
"""
def selector(opType, CostFunction, mat, inv, normType, pValue):
    tmp_cost = 0.0
    if opType == "Row":
        match CostFunction:
            case "sum":
                tmp_cost = H_sum(mat, inv)
            case "origin":
                tmp_cost = cost_origin(mat, inv)
            case "square":
                tmp_cost = H_sqr(mat, inv)
            case "cube":
                tmp_cost = H_cubr(mat, inv)
            case "fourth":
                tmp_cost = H_four(mat, inv)
            case "log":
                tmp_cost = H_logr(mat, inv)
            case "norm":
                tmp_cost = L_Norm(mat, inv, normType, pValue)
    elif opType == "Column":
        match CostFunction:
            case "sum":
                tmp_cost = H_sum(mat, inv)
            case "origin":
                tmp_cost = cost_origin(mat, inv)
            case "square":
                tmp_cost = H_sqc(mat, inv)
            case "cube":
                tmp_cost = H_cubc(mat, inv)
            case "fourth":
                tmp_cost = H_fouc(mat, inv)
            case "log":
                tmp_cost = H_logc(mat, inv)
            case "norm":
                tmp_cost = L_Norm(mat, inv, normType, pValue)
    elif opType == "global":
        match CostFunction:
            case "sum":
                tmp_cost = H_sum(mat, inv)
            case "origin":
                tmp_cost = cost_origin(mat, inv)
            case "square":
                tmp_cost = H_sq_maximum(mat, inv)
            case "cube":
                tmp_cost = H_cube_maximum(mat, inv)
            case "fourth":
                tmp_cost = H_fourth_maximum(mat, inv)
            case "log":
                tmp_cost = H_log_maximum(mat, inv)
            case "norm":
                tmp_cost = L_Norm(mat, inv, normType, pValue)
    else:
        print("Error operation type")
    return tmp_cost
