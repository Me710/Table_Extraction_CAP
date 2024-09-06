import json

def flatten_input(input_data):
    """Flatten the list of dictionaries into a single dictionary."""
    flat_data = {}
    for row in input_data:
        flat_data.update(row)
    return flat_data

def decode_special_characters(text):
    """Decode special unicode characters for quotes."""
    return text.replace('\u201c', '"').replace('\u201d', '"')

def transform_input(flat_data, max_row, max_col):
    output = []
    condition = ""
    action = ""
    level = -1
    row = 2
    col = 1
    #print(flat_data)
    while row < max_row or col < max_col:  # Iterate over columns
        key = f"row{row}col{col}"
        print("key#######",key)
        row = 2
        while row < max_row:  # Iterate over rows within each column
            if key in flat_data:
                level=col
                #word = decode_special_characters(flat_data[key]).strip().lower
                word = flat_data.get(f"row{row}col{col}", "").lower()
                print("word###################",word)
            
                if "always" in word or "all the other cases" in word:
                    condition = word
                    print("row######",row)
                    row += 1
                    word = flat_data.get(f"row{row}col{col}", "").lower()
                    i=0
                    print("word11111##########",word)
                    while i < len(word):
                        if ']' in word[i]:
                            # Add the current word (which contains ']')
                            action += word[i]
                            row += 1
                            i=0
                            word = flat_data.get(f"row{row}col{col}", "").lower()
                            # Check if the next word (if it exists) contains '['
                            if '[' in word[i]:
                                # If it does, continue the loop
                                continue
                            else:
                                # If it doesn't, or we're at the end, break the loop
                                break
                        else:
                            # If there's no ']', just add the word and continue
                            action += word[i]
                            i += 1
                    print("action##########",action)
                    if condition or action:
                        output.append({'condition': condition.strip(), 'level': level, 'action': action.strip()})
                        print("row########",row)
                        print("col#####",col)
                        condition = ""
                        action = ""
                    print("word2222#####",word) 

                if 'set' not in word:
                    condition += word  
            row += 1
            action += flat_data.get(f"row{row+2}col{col}", "").lower()
        # After processing each column, append the final condition-action pair
        if condition or action:
            output.append({'condition': condition.strip(), 'level': level, 'action': action.strip()})
            condition = ""
            action = ""
        col+=1

    return output

def get_max_row_col(flat_data):
    """Determine the maximum row and column indices from the keys."""
    max_row = max(int(key.split('row')[1].split('col')[0]) for key in flat_data.keys())
    max_col = max(int(key.split('col')[1]) for key in flat_data.keys())
    return max_row, max_col

def main(file_path):
    # Read JSON file
    with open(file_path, 'r') as file:
        input_data = json.load(file)
    
    # Flatten input data
    flat_data = flatten_input(input_data)
    
    # Get maximum row and column indices
    max_row, max_col = get_max_row_col(flat_data)
    
    # Transform input data
    output = transform_input(flat_data, max_row, max_col)
    
    # Print the output
    for item in output:
       print(item)

# Example usage: Provide the path to the JSON file
json_file_path = 'input.json'  # Replace with your JSON file path
main(json_file_path)
