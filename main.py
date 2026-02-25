import numpy as np
import sys
from modifiedImprovedGreedy import modifiedImprovedGreedy
from RowGreedy import rowGreedy
from ColGreedy import colGreedy
from LocalMinimumGreedy import localMinimumGreedy
from ParallelGreedy import parallelGreedy

np.set_printoptions(threshold=sys.maxsize) #setting for print full numpy matrix
'''
This main function execute the square cost function and product cost function respectively, using 0 and 1 to select
'''
def main(Matrix, Size, Greedy, CostFunction, inputNormType, inputPValue, times):
    matrix = np.loadtxt(Matrix, usecols=range(Size), dtype=int)
    print("The Load Block Cipher Data: ")
    print(matrix)
    for i in range(0, int(times)):
        match Greedy:
            case "Row":
                rowGreedy(matrix, CostFunction, inputNormType, inputPValue, i)
            case "Col":
                colGreedy(matrix, CostFunction, inputNormType, inputPValue, i)
            case "LocalMinima":
                localMinimumGreedy(matrix, CostFunction, inputNormType, inputPValue, i)
            case "Parallel":
                parallelGreedy(matrix, CostFunction, inputNormType, inputPValue, i)

if __name__ == "__main__":
    if len(sys.argv) != 8:
        print(f"Usage: python3 {sys.argv[0]} <matrix> <size> <greedy selection> <cost function> <input norm type> <input p value> <times>")
        sys.exit(1)

    Matrix = sys.argv[1]
    Size = int(sys.argv[2])
    Greedy = sys.argv[3]
    CostFunction = sys.argv[4]
    inputNormType = sys.argv[5]
    inputPValue = sys.argv[6]
    times = sys.argv[7]
    main(Matrix, Size, Greedy, CostFunction, inputNormType, inputPValue, times)
