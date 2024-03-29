'''
-----------------------------------------
Only allow the used library: MCT!
-----------------------------------------
'''
'''
    Consists of 3 functions: functional_constraints(); fault_conctraints(); additional_constraints()
    These functions are used to setup the SAT constraints based on circuit functionality, and seeking
    for the possible constraints on "single additional control fault (SACF)"
'''
from Read_Circuits import read_gates
'''
    Constructing the circuit behavioral constraints, 2 arrays are returned: equal_constraint; xor_constraints
    -> equal_constraints: The node on next gate is equal to current gate on same control or don't care line
    -> xor_constraints: The node on next gate on the target line is equal to current target line XOR all current
                     control lines
'''
def funtional_contraints(gates_number, control_target_dont, line_number):
    equal_constraints = []
    xor_constraints = []
    gate_idx = 0
    labels_array = [['x{}_{}'.format(j+1, i+1)for i in range(line_number)]for j in range(gates_number+1)]
    #print(labels_array)
    for values in control_target_dont:
        gate_idx += 1
        current_control, current_target, current_dont_care = values
        #print(current_control, current_target, current_dont_care)
        
        # Equality constraints for control lines
        for idx in range(len(current_control)):
            control_line_num = int(current_control[idx].split('_')[1]) - 1
            equal_constraints.append((labels_array[gate_idx][control_line_num], current_control[idx]))
        # Equality constraints for don't care
        for idx in range(len(current_dont_care)):
            dont_care_num = int(current_dont_care[idx].split('_')[1]) - 1
            equal_constraints.append((labels_array[gate_idx][dont_care_num], current_dont_care[idx]))
        
        # XOR constraint for target line, idx is always '0', since only one target at each gate
        for idx in range(len(current_target)):
            target_line_num = int(current_target[idx].split('_')[1]) - 1
            xor_constraints.append((labels_array[gate_idx][target_line_num], current_target[idx], 
                                    *current_control))
    print("The constraints for control line and empty (a, b) <=> a=b: ", equal_constraints, end="\n\n")       
    print("The constraints for target line (a, b, c) <=> a=b^c: ", xor_constraints, end="\n\n")
    return equal_constraints, xor_constraints
'''
    Constructing the faulty (SACF) behavioral constraints, 3 arrays are returned: xor_constraints_faulty;
    fault_active_constraints_control; fault_active_constraints_faulty
    -> xor_constraints_faulty: The node on next gate on the target line is equal to current target line XOR all
                            current control lines plus one faulty control line
    -> fault_active_constraints_control: All control lines except faulty one are equal to 1 
    -> fault_active_constraints_faulty: The faulty control line must equal to 0
'''
def fault_constraints(control_target_dont, xor_constraints):
    xor_constraints_faulty = []
    fault_active_constraints_control = []
    fault_active_constraints_faulty = []
    gate_idx = 0

    for values in control_target_dont:
        # Each don't care line can be single additional control fault
        current_control, current_target, faulty_control = values
        for idx in range(len(faulty_control)):
            xor_constraints_faulty.append((*xor_constraints[gate_idx], faulty_control[idx]))
            fault_active_constraints_faulty.append((faulty_control[idx], 0))
        if faulty_control:
            for idx in range(len(current_control)):
                fault_active_constraints_control.append((current_control[idx], 1))        
        gate_idx += 1
    print("The XOR constraints include SACF: ", xor_constraints_faulty, end="\n\n")
    print("The fault activation constraints (all control lines = 1): ", 
          fault_active_constraints_control, end="\n\n")
    print("The fault activation constraints (fault control line = 0): ", 
          fault_active_constraints_faulty, end="\n\n")
    return xor_constraints_faulty, fault_active_constraints_control, fault_active_constraints_faulty
'''
    Constructing the additional constraints, such as constant inputs. 1 array is returned: addition_constraints
    -> addition_constraints: If an input is constant, x1_a = const, where a is the line number
'''
def additional_constraints(constant, line_number):
    addition_constraints = []
    circuit_input = ['x{}_{}'.format(1, i+1)for i in range(line_number)]
    for idx in range(len(constant)):
        if constant[idx] == 0 or constant[idx] == 1:
            addition_constraints.append((circuit_input[idx], constant[idx]))
    if not addition_constraints:
        print("No additional constraint. ", end="\n\n")
    else:
        print("The additional constraints: (Inputs are constant): ", addition_constraints, end="\n\n")
    return addition_constraints


'''
# File path
#file_path = "/Users/liangchichen/Desktop/ATPG_SACF/Revlib_circuits/ham15_108.real"  
#file_path = "/Users/liangchichen/Desktop/ATPG_SACF/Revlib_circuits/hwb6_56.real"  
file_path = "/Users/liangchichen/Desktop/ATPG_SACF/Revlib_circuits/ham3_102.real"  
#file_path = "/Users/liangchichen/Desktop/ATPG_SACF/Revlib_circuits/toffoli_2.real"  
#file_path = "/Users/liangchichen/Desktop/ATPG_SACF/Revlib_circuits/ham7_106.real" 
#file_path = "/Users/liangchichen/Desktop/ATPG_SACF/Revlib_circuits/decode24-v0_38.real" 

# Calling the function to read gates number
gates_number, control_target_dont, line_number, constant = read_gates(file_path)


# Calling the function to read the reversible circuits based on MCT library
gates_number, control_target_dont, line_number = read_gates(file_path)
print("Number of gates:", gates_number, end="\n")
print("Number of lines:", line_number, end="\n\n")
print("Control, Target, Don't care: ", end="\n")
for values in control_target_dont:
    print(values)


equal_constraints, xor_constraints = funtional_contraints(gates_number, control_target_dont, line_number)
xor_constraints_faulty, fault_active_constraints_control, fault_active_constraints_faulty = fault_constraints(control_target_dont, xor_constraints)
addition_constraints = additional_constraints(constant, line_number)
'''