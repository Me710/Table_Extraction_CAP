import json
import re
from typing import List, Dict, Any

def get_value(row: Dict[str, str], col: int) -> str:
    key = f"row{col+1}col{col+1}"
    return row.get(key, "")

def concat_column(data: List[Dict[str, str]], col: int) -> str:
    return " ".join(get_value(row, col) for row in data if get_value(row, col))

def find_pattern(text: str, patterns: List[str]) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns)

def process_input(input_data: List[Dict[str, str]], config: Dict[str, Any]) -> List[Dict[str, Any]]:
    output = []
    n = len(input_data)
    m = max(len(row) for row in input_data)
    
    j = 1 if find_pattern(concat_column(input_data, 0), config['effects_patterns']) else 0
    
    i = 0
    while i < n and j < m:
        level = j
        condition = ""
        action = ""
        
        while i < n:
            current_word = get_value(input_data[i], j).lower()
            
            if find_pattern(current_word, config['always_patterns']):
                condition = get_value(input_data[i], j)
                i += 1
                while i < n and ']' not in get_value(input_data[i], j):
                    action += get_value(input_data[i], j) + " "
                    i += 1
            else:
                while i < n and not find_pattern(get_value(input_data[i], j).lower(), config['set_patterns']):
                    condition += get_value(input_data[i], j) + " "
                    i += 1
                while i < n and get_value(input_data[i], j):
                    action += get_value(input_data[i], j) + " "
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

def save_output(data: List[Dict[str, Any]], json_file: str, text_file: str):
    # Save as JSON
    with open(json_file, 'w') as f:
        json.dump(data, f, indent=2)
    
    # Save as plain text
    with open(text_file, 'w') as f:
        for item in data:
            f.write(f"Condition: {item['condition']}\n")
            f.write(f"Level: {item['level']}\n")
            f.write(f"Action: {item['action']}\n")
            f.write("\n")

def main(input_file: str, output_json: str, output_text: str):
    # Configuration
    config = {
        "effects_patterns": [r"effects"],
        "always_patterns": [r"always", r"all the other cases"],
        "set_patterns": [r"set"]
    }

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
    result = process_input(input_data, config)

    # Save the output
    save_output(result, output_json, output_text)

    print(f"Processing complete. Output saved to '{output_json}' and '{output_text}'.")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 4:
        print("Usage: python script.py <input_file.json> <output_file.json> <output_file.txt>")
    else:
        main(sys.argv[1], sys.argv[2], sys.argv[3])