'''
-----------------------------------------
Only allow the library used MCT!
-----------------------------------------
'''
# Function to read the gates number from the file
def read_gates(file_path):
    gates_number = 0
    control_target_dont = []
    constant = []
    line_number = None
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('.numvars'):
                line_number = int(line[9:])
            if line.startswith('.variables'):
                variables = line.split()[1:]
                #print(variables)
            if line.startswith('.constants'):
                substr = line.split(maxsplit=1)[-1]
                for const in substr:
                    if const == '0' or const == '1':
                        constant.append(int(const))
                    else:
                        constant.append(const)
                #print(constant)
            if line.startswith('t'):
                # Increment gates_number by 1
                gates_number += 1
                # Extracting gate number
                control_target_number = int(line[1:2])
                if control_target_number >= 1:
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
                control_target_dont.append((control, target, dont_care))
    return gates_number, control_target_dont, line_number, constant

'''
# File path
#file_path = "/Users/liangchichen/Desktop/ATPG_SACF/Revlib_circuits/ham15_108.real" 
file_path = "/Users/liangchichen/Desktop/ATPG_SACF/Revlib_circuits/ham3_102.real"  
#file_path = "/Users/liangchichen/Desktop/ATPG_SACF/Revlib_circuits/toffoli_2.real"  
#file_path = "/Users/liangchichen/Desktop/ATPG_SACF/Revlib_circuits/decode24-v0_38.real"

# Calling the function to read the reversible circuits based on MCT library
gates_number, control_target_dont, line_number = read_gates(file_path)
print("Number of gates:", gates_number, end="\n")
print("Number of lines:", line_number, end="\n\n")
print("Control, Target, Don't care: ", end="\n")
for values in control_target_dont:
    print(values)
'''