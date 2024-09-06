import re

def process_input(input_data):
    i = 0
    j = 0
    condition = ""
    output = []
    
    # Find the number of rows and columns
    n = len(input_data)
    m = max(len(row) for row in input_data)
    
    def get_value(row, col):
        key = f"row{row+1}col{col+1}"
        return input_data[row].get(key, "")
    
    def concat_column(col):
        return " ".join(get_value(row, col) for row in range(n) if get_value(row, col))
    
    def concat_row(row):
        return " ".join(value for value in input_data[row].values())
    
    # Check for "Effects" and adjust starting column
    if "Effects" in concat_column(0):
        j = 1
    
    # Process conditions and actions
    while i < n and j < m:
        level = j
        condition = ""
        action = ""
        
        while i < n:
            current_word = get_value(i, j).lower()
            
            if "always" in current_word or "all the other cases" in current_word:
                condition = get_value(i, j)
                i += 1
                while i < n and ']' not in get_value(i, j):
                    action += get_value(i, j) + " "
                    i += 1
            else:
                while i < n and 'set' not in get_value(i, j).lower():
                    condition += get_value(i, j) + " "
                    i += 1
                while i < n and get_value(i, j):
                    action += get_value(i, j) + " "
                    i += 1
            
            if condition and action:
                break
        
        if condition or action:
            output.append({"condition": condition.strip(), "level": level, "action": action.strip()})
        
        i += 1
        if i >= n:
            i = 0
            j += 1
    
    return output

# Test the function with the provided input
input_data = [
    {"row1col1": "Causes"},
    {"row2col1": "Always"},
    {"row3col1": "[Get the OVSP side identification]"},
    {"row4col1": "[Get the PBIT test result]"},
    {"row5col1": "\"OVSP Side Identification\" is equal to"},
    {"row6col1": "BOOT_SIDE_ID_INVALID OR \"PBIT test", "row6col2": "All the other cases"},
    {"row7col1": "Result\" is equal to E_PBIT_Failed"},
    {"row8col0": "Effects", "row8col2": "[Get the OVSP config table integrity status]"},
    {"row9col2": "\"OVSP Config table"},
    {"row10col2": "Integrity Status\" is"},
    {"row11col1": "Set {V_Modes_SW_Mode} to", "row11col2": "equal to", "row11col3": "All the other cases"},
    {"row12col1": "E_Modes_Fail", "row12col2": "E_Config_Integrity_"},
    {"row13col2": "KO"},
    {"row14col2": "Set", "row14col3": "Set {V_Modes_SW_Mode} to"},
    {"row15col2": "{V_Modes_SW_Mod", "row15col3": "E_Modes_Operational"}
]

result = process_input(input_data)
for item in result:
    print(item)