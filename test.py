import pdfplumber
import json

# Open the PDF and extract the table from the specified page
with pdfplumber.open('LLR_CAP.pdf') as pdf:
    first_page = pdf.pages[6]
    tables = first_page.extract_table()

# Initialize an empty list to hold the JSON data
json_data = []

# Iterate over each row in the table
for row_index, row in enumerate(tables):
    # Create a dictionary for the current row
    row_dict = {}
    
    # Dynamically add columns based on the number of elements in the row
    for col_index, cell in enumerate(row):
        if cell is not None and cell != "":  # Only add non-empty values
            cell_key = f"row{row_index+1}col{col_index}"  # Create the cell key (e.g., "row0col0", "row0col1", etc.)
            row_dict[cell_key] = cell   # Assign the cell value to the appropriate cell key
    
    # Append the row dictionary to the JSON data list if it's not empty
    if row_dict:
        json_data.append(row_dict)

# Convert the list of dictionaries to a JSON string with indentation for readability
json_output = json.dumps(json_data, indent=4)

# Print the JSON string
print(json_output)

# Calculate the size of the matrix
num_rows = len(json_data)
num_cols = len(tables[0]) if tables else 0  # Get the number of columns from the first row

# Print the size of the matrix
print(f"Matrix size: {num_rows} x {num_cols}")

# Optionally, write the JSON output to a file
with open('input.json', 'w') as f:
    f.write(json_output)
