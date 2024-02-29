'''
from pysat.solvers import Glucose3

# Initialize SAT solver
solver = Glucose3()

# Define equal and XOR constraints
equal_constraints = [(1, 2), (3, 4)]  # Example: x1 = x2, x3 = x4
xor_constraints = [(1, 2), (3, 4)]    # Example: x1 XOR x2, x3 XOR x4

# Convert equal constraints to CNF
for x, y in equal_constraints:
    solver.add_clause([-x, y])  # (x -> y)
    solver.add_clause([x, -y])  # (y -> x)

# Convert XOR constraints to CNF
for x, y in xor_constraints:
    solver.add_clause([-x, -y, x + y])  # (x1 -> -x2) ∧ (x2 -> -x1) ∧ (x1 ∨ x2)

# Solve the CNF formula
if solver.solve():
    model = solver.get_model()
    print("Satisfiable! Model:", model)
else:
    print("Unsatisfiable!")
'''
from pysat.solvers import Minisat22
from itertools import combinations

def xor_to_cnf(xor_list):
    cnf = []
    for xor_clause in xor_list:
        for combination in combinations(xor_clause, 2):
            x, y = combination
            cnf.append([x, -y])
            cnf.append([-x, y])
    return cnf

def to_cnf(constraints):
    cnf = []
    for constraint in constraints:
        cnf.append(constraint)
    return cnf

def solve_cnf(cnf, additional_constraints=None):
    solver = Minisat22()
    solver.append_formula(cnf)
    if additional_constraints:
        solver.append_formula(additional_constraints)
    if solver.solve():
        model = solver.get_model()
        return model
    else:
        return None

# Example usage
xor_list = [('x', 'y', 'z', 'a', 'b', 'c')]
xor_cnf = xor_to_cnf(xor_list)
additional_constraints = [['x', '-y'], ['-x', 'y']]  # Example additional constraint x=y
additional_cnf = to_cnf(additional_constraints)
model = solve_cnf(xor_cnf, additional_cnf)
if model:
    print("Satisfiable! Model:", model)
else:
    print("Unsatisfiable!")