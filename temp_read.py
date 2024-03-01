# Function to read the gates number from the file
def read_gates(file_path):
    gates_number = 0
    control_target_dict = {}
    line_number = None
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('.numvars'):
                line_number = int(line[9:])
            if line.startswith('.variables'):
                variables = line.split()[1:]
            if line.startswith('.outputs'):
                outputs = line.split()[1:]
            '''
            if line.startswith('.constants'):
                constant = line.split()[1:]
            '''
            if line.startswith('t'):
                # Increment gates_number by 1
                gates_number += 1
                # Extracting gate number
                control_target_number = int(line[1])
                if control_target_number > 1:
                    # Extracting don't care, control and target variables for gates with control_target_number > 1
                    # Noted: The letters except the last of each toffoli gate description are always control lines
                    control = ['x{}_{}'.format(gates_number, variables.index(var) + 1) 
                               for var in line[3:(3+(2*(control_target_number-1))):2]]
                    # Noted: The last letter of each toffoli gate description is always the target line
                    target = ['x{}_{}'.format(gates_number, variables.index(line[-1]) + 1)]
                    # Noted: The rest of the letters are denoted as don't care 
                    dont_care = ['x{}_{}'.format(gates_number, variables.index(var) + 1) 
                                 for var in variables if var not in line[3::2]]
                # Dynamically add keys to control_target_dict if needed
                key = 't{}'.format(control_target_number)
                if key not in control_target_dict:
                    control_target_dict[key] = []
                control_target_dict[key].append((control, target, dont_care))
    
        if 'to' not in control_target_dict:
            control_target_dict['to'] = []
        control_target_dict['to'].append(([], [], ['x{}_{}'.format(gates_number+1, outputs.index(var) + 1) 
                                 for var in outputs]))
    return gates_number, control_target_dict, line_number

'''
# File path
file_path = "/Users/liangchichen/Desktop/ATPG_SACF/Revlib_circuits/ham15_108.txt" 
#file_path = "/Users/liangchichen/Desktop/ATPG_SACF/Revlib_circuits/ham3_102.txt"  
#file_path = "/Users/liangchichen/Desktop/ATPG_SACF/Revlib_circuits/toffoli_2.txt"  
gates_number, control_target_dict, line_number = read_gates(file_path)

# Calling the function to read gates number
gates_number, control_target_dict, line_number = read_gates(file_path)
print("Number of gates:", gates_number)
print("Number of lines:", line_number)
for gate_type, values in control_target_dict.items():
    print("Gate Type:", gate_type)
    for control, target in values:
        print("Control:", control, "Target:", target)
'''