import numpy as np
import sys
import os
from modifiedImprovedGreedy import modifiedImprovedGreedy

np.set_printoptions(threshold=sys.maxsize) #setting for print full numpy matrix
'''
This main function execute the square cost function and product cost function respectively, using 0 and 1 to select
'''
def main(Matrix, Size, Greedy, CostFunction, inputNormType, inputPValue, times):
    matrix = np.loadtxt(Matrix, usecols=range(Size), dtype=int)
    print("The Load Block Cipher Data: ")
    print(matrix)
    filename = os.path.splitext(os.path.basename(Matrix))[0]
    for i in range(0, int(times)):
        modifiedImprovedGreedy(Greedy, matrix, filename, CostFunction, inputNormType, inputPValue, i)

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
