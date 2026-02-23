## Table of Contents
- [About](#About)
- [Installation](#Installation)
- [Usage](#Usage)
- [Result](#Result)

## About
In this project, we implement an approach that reduces the depth of quantum circuits, specifically focusing on the CNOT gate.
```bash
.
├── main.py
    ├── RowGreedy.py
    ├── ColGreedy.py
    ├── LocalMinimumGreedy.py
    ├── ParallelGreedy.py
        ├── config.py
        ├── Can_depth_one.py
        ├── cost_function.py
        ├── operations.py
        ├── writers.py
        └── verify.py
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
## Result
The algorithm generates the CNOT synthesis result record in files
