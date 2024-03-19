'''
-----------------------------------------
Only allow the used library: MCT!
-----------------------------------------
'''
'''
    Function used to read the circuit description file, and convert it into the form can be applied in
    SAT constrints. 4 variables are returned: gates_number; control_target_dont; line_number; constant
    -> gates_number: Numbers of gate of the given circuit
    -> control_target_dont: The nodes of control, target, and don't care lines of each gate
    -> line_number: Numbers of line of the given circuit
    -> constant: All constant on inputs
'''
def read_gates(file_path):
    gates_number = 0
    control_target_dont = []
    constant = []
    line_number = None
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            # Read line number
            if line.startswith('.numvars'):
                line_number = int(line[9:])
            # Read variables of the circuit
            if line.startswith('.variables'):
                variables = line.split()[1:]
            # Read constants on inputs
            if line.startswith('.constants'):
                substr = line.split(maxsplit=1)[-1]
                for const in substr:
                    if const == '0' or const == '1':
                        constant.append(int(const))
                    else:
                        constant.append(const)
            '''
                Read gate details
                Each gate consist of 3 different elements: control; target; dont_care
                control: all the control lines
                target: the target line
                dont_care: remaining lines which are not included in control or target
                Noted: The node of each line of each gate is specified as the form xa_b,
                       while a represents gate number and b represent line number
            '''
            if line.startswith('t'):
                gates_number += 1
                control_target_number = int(line[1:2]) # Extracting gate number
                if control_target_number >= 1:
                    control = ['x{}_{}'.format(gates_number, variables.index(var) + 1) 
                               for var in line[3:(3+(2*(control_target_number-1))):2]]
                    target = ['x{}_{}'.format(gates_number, variables.index(line[-1]) + 1)]
                    dont_care = ['x{}_{}'.format(gates_number, variables.index(var) + 1) 
                                 for var in variables if var not in line[3::2]]
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