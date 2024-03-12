from SAT_constraints import funtional_contraints
from SAT_constraints import fault_constraints
from SAT_constraints import additional_constraints
from Read_Circuits import read_gates
from pysat.formula import CNF
from pysat.solvers import Minisat22

def main(): 
    gate_idx = 0
    xor_fault_idx = 0
    
    # Calling the function to read gates number
    gates_number, control_target_dont, line_number, constant = read_gates(file_path)
    print(control_target_dont)
    equal_constraints, xor_constraints = funtional_contraints(gates_number, control_target_dont, line_number)
    xor_constraints_faulty, fault_active_constraints_control, fault_active_constraints_faulty = fault_constraints(control_target_dont, xor_constraints)
    addition_constraints = additional_constraints(constant, line_number)
    
    if equal_constraints:
        label_equal_constraints = label_to_int(equal_constraints)
        equal_constraints_cnf = equation_cnf(label_equal_constraints)
        print("The CNF constraints of equality is: ",equal_constraints_cnf.clauses, end="\n\n")
    if addition_constraints:
        label_addition_constraints = label_to_int(addition_constraints)
        addition_constraints_cnf = equation_01_cnf(label_addition_constraints)
        print("The CNF constraints of equality is: ",addition_constraints_cnf.clauses, end="\n\n")
    if xor_constraints:
        label_xor_constraints = label_to_int(xor_constraints)
        xor_constraints_cnf = xor_to_cnf(label_xor_constraints)
        print(label_xor_constraints)
        print(xor_constraints_cnf.clauses, end="\n\n")
    if xor_constraints_faulty:
        label_xor_constraints_faulty = label_to_int(xor_constraints_faulty)
        xor_constraints_faulty_cnf = xor_to_cnf(label_xor_constraints_faulty)
        print(label_xor_constraints_faulty)
        print(xor_constraints_faulty_cnf.clauses, end="\n\n")
    if fault_active_constraints_control:
        label_fault_active_constraints_control = label_to_int(fault_active_constraints_control)
        fault_active_constraints_control_cnf = equation_01_cnf(label_fault_active_constraints_control)
        print(fault_active_constraints_control_cnf.clauses, end="\n\n")
    if fault_active_constraints_faulty:
        label_fault_active_constraints_faulty = label_to_int(fault_active_constraints_faulty)
        fault_active_constraints_faulty_cnf = equation_01_cnf(label_fault_active_constraints_faulty)
        print(fault_active_constraints_faulty_cnf.clauses, end="\n\n")
        
    print(label_map, end="\n\n")
    
    for gate_idx in range(gates_number):
        for clause in label_xor_constraints_faulty:
            with Minisat22() as solver:
                if clause[0] == label_xor_constraints[gate_idx][0]:
                    solver.append_formula(equal_constraints_cnf)
                    if addition_constraints:
                        solver.append_formula(addition_constraints_cnf)
                    solver.append_formula([fault_active_constraints_control_cnf.clauses[xor_fault_idx]])
                    solver.append_formula([fault_active_constraints_faulty_cnf.clauses[xor_fault_idx]])
                    solver.append_formula(xor_to_cnf([clause]))
                    for clauses in xor_constraints_cnf:
                        if clauses[0] != label_xor_constraints[gate_idx][0] and clauses[0] != -label_xor_constraints[gate_idx][0]:
                            solver.append_formula([clauses])
                            
                    sat = solver.solve()
                    solution = solver.get_model()
                    
                    if sat is True:
                        print("Satisfiable (Test pattern of given SACF can be found)!")
                        print("The generated test pattern is: ", solution)
                    else:
                        print("Unsatisfiable (The SACF will be added to untestable list)!")
                        
                    xor_fault_idx += 1
        gate_idx += 1
        
    
def label_to_int(constraints):
    global label_map
    new_id_constraints = []
    for idx in range(len(constraints)):
        new_id_tuple = ()
        for idy in range(len(constraints[idx])):
            label_name = constraints[idx][idy]
            if label_name not in label_map:
                label_map[label_name] = len(label_map) + 1 
            new_id_tuple += (label_map[label_name],)
        new_id_constraints.append(new_id_tuple)
    return new_id_constraints
    
def equation_cnf(constraints):
    equ_cnf = CNF()
    for idx in range(len(constraints)):
        equ_cnf.append([constraints[idx][0], -constraints[idx][1]])
        equ_cnf.append([-constraints[idx][0], constraints[idx][1]])
    #print(equ_cnf.clauses)
    return equ_cnf

def equation_01_cnf(constraints):
    equ_01_cnf = CNF()
    key_is_1 = label_map.get(1)
    key_is_0 = label_map.get(0)
    for constraint in constraints:
        for label in constraint:
            if label == key_is_1:
                equ_01_cnf.append([constraint[0]])  
            elif label == key_is_0:
                equ_01_cnf.append([-constraint[0]])  
    return equ_01_cnf

def xor_to_cnf(constraints):
    xor_cnf = CNF()
    for constraint in constraints:
        a, b = constraint[:2]
        conjuncts = constraint[2:]
        xor_cnf.append([a, b])
        xor_cnf.append([-a, -b])
        for conjunct in conjuncts:
            xor_cnf.append([a, -b, conjunct])
            xor_cnf.append([-a, b, conjunct])
            for clause in xor_cnf.clauses:
                if clause[:2] == [a, b]:
                    clause.extend([-conjunct])
                elif clause[:2] == [-a, -b]:
                    clause.extend([-conjunct])
    return xor_cnf

if __name__ == '__main__': 
    label_map = {}
    # File path
    #file_path = "/Users/liangchichen/Desktop/ATPG_SACF/Revlib_circuits/ham15_108.real"  
    #file_path = "/Users/liangchichen/Desktop/ATPG_SACF/Revlib_circuits/hwb6_56.real"  
    file_path = "/Users/liangchichen/Desktop/ATPG_SACF/Revlib_circuits/ham3_102.real"  
    #file_path = "/Users/liangchichen/Desktop/ATPG_SACF/Revlib_circuits/toffoli_2.real"  
    #file_path = "/Users/liangchichen/Desktop/ATPG_SACF/Revlib_circuits/ham7_106.real" 
    #file_path = "/Users/liangchichen/Desktop/ATPG_SACF/Revlib_circuits/decode24-v0_38.real"
    main()