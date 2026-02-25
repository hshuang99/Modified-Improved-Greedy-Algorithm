## Table of Contents
- [About](#About)
- [Installation](#Installation)
- [Usage](#Usage)
- [Result](#Result)

## About
In this project, we implement an approach that reduces the depth of quantum circuits, specifically focusing on the CNOT gate.
```bash
.
├── Matrix
├── main.py
    ├── RowGreedy.py
        ├── RowConfig.ini
    ├── ColGreedy.py
        ├── ColConfig.ini
    ├── LocalMinimumGreedy.py
        ├── LocalMinimaConfig.ini
    ├── ParallelGreedy.py
        ├── ParallelConfig.ini
    ├── cost_function.py
    ├── operations.py
    └── selector.py
```

## Installation
To execute this repo, please create a virtual environment
```
python3 -m venv venv
source venv/bin/activate
```
Then install the modules used in the algorithm
```
pip install numpy
pip install random
pip install copy
```
## Usage
The command executes this Greedy algorithm
```
python3 main.py <Matrix> <Size> <Greedy Selection> <Cost Function> <Input Norm Type> <Input Norm P Value> <Times>
```
- Matrix: The matrix what we testing
- Size: The size of the matrix you need to assign. Some matrices have the same structure but different sizes, such as 32×32 and 16×16 versions.
- Greedy Selection: The greedy algorithm you want to execute. We provide four types of algorithms: Row, Column, Local Minima, and Parallel.
- Cost Function: The cost function used to calculate the operation cost. You can choose from sum, origin, square, log, and norm. The norm options include L1, L2, Lp (e.g., 3, 4, ...), and Linf.
- Input Norm Type: If you choose the L-norm cost function, you need to specify the norm type. If you select another type of cost function, enter an empty string ("") for this parameter.
- Input Norm P Value: If you choose the Lp norm cost function, you must provide a number greater than 2 (e.g., 3, 4, ...). If you do not choose the Lp norm function, enter 0.
- Times: The number of iterations you want to run.
## Result
The algorithm generates the CNOT synthesis result record in files, for example, we will make two results
### Layer Results
This result presents the available operators for each layer and records the number of CNOT gates and the circuit depth of the quantum circuit.
```
(7 15 1)|(6 22 1)|(14 30 1)|(23 31 1)|(28 12 1)|(13 29 1)|(20 4 1)|(21 5 1)|(27 3 1)|(26 10 1)|(2 18 1)|(24 8 1)|(11 19 1)|(25 1 1)|(9 17 1)|(16 0 1)|
(31 15 1)|(5 29 1)|(27 11 1)|(21 13 1)|(19 3 1)|(17 1 1)|(0 7 1)|(25 9 1)|(18 2 1)|(22 14 1)|(20 28 1)|(12 23 1)|(16 24 1)|
(7 23 1)|(10 9 1)|(15 22 1)|(1 8 1)|(29 28 1)|(30 5 1)|(26 25 1)|(3 27 1)|(11 31 1)|(0 16 1)|(18 17 1)|(4 20 1)|(6 14 1)|
(4 23 1)|(22 5 1)|(18 9 1)|(12 11 1)|(19 7 1)|(15 30 1)|(8 31 1)|(3 10 1)|(1 25 1)|(29 21 1)|
(4 11 1)|(5 28 1)|(17 7 1)|(22 14 1)|(30 6 1)|(1 16 1)|(3 23 1)|(9 31 1)|
(29 4 1)|(9 7 1)|(22 13 1)|(8 23 1)|
(14 23 0)|(19 4 0)|(26 11 0)|(7 28 0)|(6 22 0)|
(6 23 0)|(17 3 0)|(31 4 0)|(28 15 0)|(7 24 0)|(21 22 0)|(26 19 0)|(16 8 0)|(25 2 0)|(20 12 0)|
(27 28 0)|(21 14 0)|(6 31 0)|(16 17 0)|(26 10 0)|(2 19 0)|(20 13 0)|(25 11 0)|(24 9 0)|(18 3 0)|(0 1 0)|(12 29 0)|(5 15 0)|
(5 21 0)|(15 31 0)|(11 27 0)|(23 7 0)|(1 17 0)|(29 13 0)|(9 25 0)|(3 19 0)|(28 20 0)|(24 16 0)|(2 10 0)|(14 6 0)|(26 18 0)|
(29 5 0)|(13 21 0)|(30 14 0)|(22 6 0)|(8 24 0)|(3 27 0)|(4 20 0)|(15 7 0)|(17 9 0)|(1 25 0)|(19 11 0)|(31 23 0)|(12 28 0)|(10 26 0)|(18 2 0)|(0 16 0)|
CNOT: 121, depth: 11 and cost function: origin occur in 2
```
### Sequence Results
Another result presents the synthesized operations of this quantum circuit. This makes it convenient to verify correctness, as we can execute each operator on a matrix to check whether it produces a permutation matrix.
```
7, 15, 1
6, 22, 1
14, 30, 1
23, 31, 1
28, 12, 1
13, 29, 1
20, 4, 1
21, 5, 1
27, 3, 1
26, 10, 1
2, 18, 1
24, 8, 1
11, 19, 1
25, 1, 1
9, 17, 1
16, 0, 1
31, 15, 1
5, 29, 1
27, 11, 1
21, 13, 1
19, 3, 1
17, 1, 1
0, 7, 1
25, 9, 1
18, 2, 1
22, 14, 1
20, 28, 1
12, 23, 1
16, 24, 1
7, 23, 1
10, 9, 1
15, 22, 1
1, 8, 1
29, 28, 1
30, 5, 1
26, 25, 1
3, 27, 1
11, 31, 1
0, 16, 1
18, 17, 1
4, 20, 1
6, 14, 1
4, 23, 1
22, 5, 1
18, 9, 1
12, 11, 1
19, 7, 1
15, 30, 1
8, 31, 1
3, 10, 1
1, 25, 1
29, 21, 1
4, 11, 1
5, 28, 1
17, 7, 1
22, 14, 1
30, 6, 1
1, 16, 1
3, 23, 1
9, 31, 1
29, 4, 1
9, 7, 1
22, 13, 1
8, 23, 1
6, 22, 0
7, 28, 0
26, 11, 0
19, 4, 0
14, 23, 0
20, 12, 0
25, 2, 0
16, 8, 0
26, 19, 0
21, 22, 0
7, 24, 0
28, 15, 0
31, 4, 0
17, 3, 0
6, 23, 0
5, 15, 0
12, 29, 0
0, 1, 0
18, 3, 0
24, 9, 0
25, 11, 0
20, 13, 0
2, 19, 0
26, 10, 0
16, 17, 0
6, 31, 0
21, 14, 0
27, 28, 0
26, 18, 0
14, 6, 0
2, 10, 0
24, 16, 0
28, 20, 0
3, 19, 0
9, 25, 0
29, 13, 0
1, 17, 0
23, 7, 0
11, 27, 0
15, 31, 0
5, 21, 0
0, 16, 0
18, 2, 0
10, 26, 0
12, 28, 0
31, 23, 0
19, 11, 0
1, 25, 0
17, 9, 0
15, 7, 0
4, 20, 0
3, 27, 0
8, 24, 0
22, 6, 0
30, 14, 0
13, 21, 0
29, 5, 0
CNOT: 121
```