from SAT_constraints import funtional_contraints
from SAT_constraints import fault_constraints
from SAT_constraints import additional_constraints
from Read_Circuits import read_gates
from pysat.formula import CNF
from pysat.solvers import Minisat22

def main(): 
    # Calling the function to read gates number
    gates_number, control_target_dont, line_number, constant = read_gates(file_path)
    
    equal_constraints, xor_constraints = funtional_contraints(gates_number, control_target_dont, line_number)
    xor_constraints_faulty, fault_active_constraints_control, fault_active_constraints_faulty = fault_constraints(control_target_dont, xor_constraints)
    addition_constraints = additional_constraints(constant, line_number)
    
    if equal_constraints:
        label_equal_constraints = label_to_int(equal_constraints)
        equal_constraints_cnf = equation_cnf(label_equal_constraints)
        print(equal_constraints_cnf)
    if addition_constraints:
        label_addition_constraints = label_to_int(addition_constraints)
        addition_constraints_cnf = equation_cnf(label_addition_constraints)
        print(addition_constraints_cnf)
        
    print(label_map)
    
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