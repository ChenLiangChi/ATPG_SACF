from SAT_constraints import funtional_contraints
from SAT_constraints import fault_constraints
from SAT_constraints import additional_constraints
from Read_Circuits import read_gates
from pysat.formula import CNF
from pysat.solvers import Minisat22
# TODO:Add comment to each functions
# TODO:Unsatisfied issue!

def main(): 
    gate_idx = 0
    xor_fault_idx = 0
    num_SACF = 0 # Number of SACF in total
    num_test = 0 # Number of testable SACF
    num_untest = 0 # Number of untestable SACF
    
    # Calling the function to read gates number
    gates_number, control_target_dont, line_number, constant = read_gates(file_path)
    equal_constraints, xor_constraints = funtional_contraints(gates_number, control_target_dont, line_number)
    xor_constraints_faulty, fault_active_constraints_control, fault_active_constraints_faulty = fault_constraints(control_target_dont, xor_constraints)
    addition_constraints = additional_constraints(constant, line_number)
    
    if equal_constraints:
        label_equal_constraints = label_to_int(equal_constraints)
        equal_constraints_cnf = equation_cnf(label_equal_constraints)
        #print("The CNF constraints of equality is: ",equal_constraints_cnf.clauses, end="\n\n")
    if addition_constraints:
        label_addition_constraints = label_to_int(addition_constraints)
        addition_constraints_cnf = equation_01_cnf(label_addition_constraints)
        #print("The CNF constraints of equality is: ",addition_constraints_cnf.clauses, end="\n\n")
    if xor_constraints:
        label_xor_constraints = label_to_int(xor_constraints)
        xor_constraints_cnf = xor_to_cnf(label_xor_constraints)
        print(label_xor_constraints)
        print("The XOR constraints are: ", xor_constraints_cnf.clauses, end="\n\n")
    if xor_constraints_faulty:
        label_xor_constraints_faulty = label_to_int(xor_constraints_faulty)
        xor_constraints_faulty_cnf = xor_to_cnf(label_xor_constraints_faulty)
        print(label_xor_constraints_faulty)
        print("The XOR faulty constraints are: ", xor_constraints_faulty_cnf.clauses, end="\n\n")
    if fault_active_constraints_control:
        label_fault_active_constraints_control = label_to_int(fault_active_constraints_control)
        fault_active_constraints_control_cnf = equation_01_cnf(label_fault_active_constraints_control)
        print(fault_active_constraints_control_cnf.clauses, end="\n\n")
    if fault_active_constraints_faulty:
        label_fault_active_constraints_faulty = label_to_int(fault_active_constraints_faulty)
        fault_active_constraints_faulty_cnf = equation_01_cnf(label_fault_active_constraints_faulty)
        print(fault_active_constraints_faulty_cnf.clauses, end="\n\n")
        
    print(label_map, end="\n\n")
    
    for gate in control_target_dont:
        #Get the numbers of control on each gate
        num_control = len(gate[0])
        pos_SACF = 0
        if xor_constraints_faulty:
            for clause in label_xor_constraints_faulty:
                with Minisat22() as solver:
                    if clause[0] == label_xor_constraints[gate_idx][0]:
                        num_SACF += 1 
                        # Equality on control line and don't care line must be satisfied
                        solver.append_formula(equal_constraints_cnf)
                        if addition_constraints:
                            # An additional contraints such as constant input, must be satisfied
                            solver.append_formula(addition_constraints_cnf)
                        # The control except faulty must be 1    
                        solver.append_formula([fault_active_constraints_control_cnf.clauses[idx] for idx in range(num_control)])
                        # The faulty control must be 0
                        solver.append_formula([fault_active_constraints_faulty_cnf.clauses[xor_fault_idx]])
                        # The SACF constraint on tofolli gate must be satisfied
                        solver.append_formula(xor_to_cnf([clause]))
                        # The tofolli gate functional constraints except the potential fault must be satisfied 
                        for clauses in xor_constraints_cnf:
                            if clauses[0] != label_xor_constraints[gate_idx][0] and clauses[0] != -label_xor_constraints[gate_idx][0]:
                                solver.append_formula([clauses])
                                
                        sat = solver.solve()
                        solution = solver.get_model()
                        
                        print("The SACF is on: ", gate[2][pos_SACF])
                        pos_SACF += 1
                        
                        if sat is True:
                            num_test += 1
                            result, test_pattern = int_to_result(solution)
                            print("Satisfiable!")
                            print("The generated test pattern is: ", test_pattern)
                            print("The propageted result of given test pattern is: ", result, end="\n\n")
                        else:
                            num_untest += 1
                            print("Unsatisfiable (The given SACF is untestable)!", end="\n\n") 
                        xor_fault_idx += 1
                        solver.delete()
        gate_idx += 1
    
    print("Number of possible SACF: ", num_SACF)
    print("Number of testable SACF: ", num_test)
    print("Number of untestable SACF: ", num_untest)

    
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
    #print(xor_cnf.clauses)
    return xor_cnf

def int_to_result(result):
    primary_input = []
    output = {}
    for num in result:
        if num > 0:
            for key, value in label_map.items():
                if value == num:
                    output[key] = 1
        if num < 0:
            for key, value in label_map.items():
                if value == -num:
                    output[key] = 0
    filtered_output = {key: value for key, value in output.items() if key not in (0, 1)}
    sorted_keys = sorted(filtered_output.keys(), key=sort_dict)
    sorted_output = {key: filtered_output[key] for key in sorted_keys}
    
    for key in sorted_output.keys():
        if key.startswith('x1_'):
            primary_input.append(sorted_output[key])
    return sorted_output, primary_input

def sort_dict(key):
    parts = key.split('_')
    return int(parts[0][1:]), int(parts[1])
 
if __name__ == '__main__': 
    label_map = {}
    # File path
    #file_path = "/Users/liangchichen/Desktop/ATPG_SACF/Revlib_circuits/ham15_108.real" 
    #file_path = "/Users/liangchichen/Desktop/ATPG_SACF/Revlib_circuits/alu-v1_28.real" 
    file_path = "/Users/liangchichen/Desktop/ATPG_SACF/Revlib_circuits/rd32_272.real" 
    #file_path = "/Users/liangchichen/Desktop/ATPG_SACF/Revlib_circuits/hwb6_56.real"  
    #file_path = "/Users/liangchichen/Desktop/ATPG_SACF/Revlib_circuits/ham3_102.real"  
    #file_path = "/Users/liangchichen/Desktop/ATPG_SACF/Revlib_circuits/toffoli_2.real"  
    #file_path = "/Users/liangchichen/Desktop/ATPG_SACF/Revlib_circuits/ham7_106.real" 
    #file_path = "/Users/liangchichen/Desktop/ATPG_SACF/Revlib_circuits/decode24-v0_38.real"
    main()