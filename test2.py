import json
import re
from typing import List, Dict, Any

def get_value(row: Dict[str, str], col: int) -> str:
    key = f"row{row['row']}col{col+1}"
    return row.get(key, "")

def concat_column(data: List[Dict[str, str]], col: int) -> str:
    return " ".join(get_value(row, col) for row in data if get_value(row, col))

def process_input(input_data: List[Dict[str, str]]) -> List[Dict[str, Any]]:
    output = []
    n = len(input_data)
    m = max(len(row) for row in input_data)
    
    for row in input_data:
        row['row'] = int(re.search(r'row(\d+)', list(row.keys())[0]).group(1))
    
    i = 0
    j = 0
    condition = ""
    
    # Check for "Effects" and adjust starting column
    var0 = concat_column(input_data, 0)
    if "Effects" in var0:
        j = 1
    
    # Skip "Causes" row
    while i < n and (get_value(input_data[i], j).lower() == "causes" or condition == ""):
        i += 1
        condition = get_value(input_data[i], j)
    
    while i < n and j < m:
        level = j
        action = ""
        
        if "always" in condition.lower() or "all the other cases" in condition.lower():
            i += 1
            while i < n and ']' in get_value(input_data[i], j):
                action += get_value(input_data[i], j) + " "
                i += 1
        else:
            while i < n and "set" not in get_value(input_data[i], j).lower():
                condition += get_value(input_data[i], j) + " "
                i += 1
            while i < n and get_value(input_data[i], j):
                action += get_value(input_data[i], j) + " "
                i += 1
        
        output.append({"condition": condition.strip(), "level": level, "action": action.strip()})
        
        i += 1
        if i >= n:
            i = 0
            j += 1
            condition = get_value(input_data[i], j)
    
    return output

def save_output(data: List[Dict[str, Any]], json_file: str, text_file: str):
    # Save as JSON
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    # Save as plain text
    with open(text_file, 'w') as f:
        for item in data:
            f.write(f"{item}\n")

def main(input_file: str, output_json: str, output_text: str):
    # Read input from JSON file
    try:
        with open(input_file, 'r') as f:
            input_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in input file '{input_file}'.")
        return

    # Process the input
    result = process_input(input_data)

    # Save the output
    save_output(result, output_json, output_text)

    print(f"Processing complete. Output saved to '{output_json}' and '{output_text}'.")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_file.json> <output_file.json> <output_file.txt>")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])