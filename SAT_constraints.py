from Read_Circuits import read_gates

# File path
#file_path = "/Users/liangchichen/Desktop/ATPG_SACF/Revlib_circuits/ham15_108.txt"  
#file_path = "/Users/liangchichen/Desktop/ATPG_SACF/Revlib_circuits/hwb6_56.txt"  
file_path = "/Users/liangchichen/Desktop/ATPG_SACF/Revlib_circuits/ham3_102.txt"  
#file_path = "/Users/liangchichen/Desktop/ATPG_SACF/Revlib_circuits/toffoli_2.txt"  
#file_path = "/Users/liangchichen/Desktop/ATPG_SACF/Revlib_circuits/ham7_106.txt"  

# Calling the function to read gates number
gates_number, control_target_dont, line_number = read_gates(file_path)
'''
print("Number of gates:", gates_number)
print("Number of lines:", line_number)
for gate_type, values in control_target_dict.items():
    print("Gate Type:", gate_type)
    for control, target, dont_care in values:
        print("Control:", control, "Target:", target, "Don't Care:", dont_care)

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

def fault_constraints(control_target_dont, xor_constraints):
    xor_constraints_faulty = []
    fault_active_constraints_control = []
    fault_active_constraints_faulty = []
    gate_idx = 0

    for values in control_target_dont:
        # Each don't care line can be single additional control fault
        current_control, current_target, faulty_control = values
        if not faulty_control:
            xor_constraints_faulty.append((*xor_constraints[gate_idx],))
            fault_active_constraints_faulty.append((),)
        else:
            for idx in range(len(faulty_control)):
                xor_constraints_faulty.append((*xor_constraints[gate_idx], faulty_control[idx]))
                fault_active_constraints_faulty.append((faulty_control[idx], 0))
        for idx in range(len(current_control)):
                fault_active_constraints_control.append((current_control[idx], 1))        
        gate_idx += 1
    print("The XOR constraints include SACF: ", xor_constraints_faulty, end="\n\n")
    print("The fault activation constraints (all control lines = 1): ", 
          fault_active_constraints_control, end="\n\n")
    print("The fault activation constraints (fault control line = 0): ", 
          fault_active_constraints_faulty, end="\n\n")
    return xor_constraints_faulty, fault_active_constraints_control, fault_active_constraints_faulty
def additional_constraints():
    return

equal_constraints, xor_constraints = funtional_contraints(gates_number, control_target_dont, line_number)
xor_constraints_faulty, fault_active_constraints_control, fault_active_constraints_faulty = fault_constraints(control_target_dont, xor_constraints)