import pdfplumber
import json

with pdfplumber.open('LLR_CAP.pdf') as pdf:
    first_page = pdf.pages[9]
    tables = first_page.extract_table()
    print(tables)

json_data = []
for row in tables:
    json_data.append({
        "col1": row[0],
        "col2": row[1],
        "col3": row[2],
        "col4": row[3],
        "col5": row[4]
    })

# Convert the list of dictionaries to a JSON string
json_output = json.dumps(json_data, indent=4)

# Print or save the JSON string
print(json_output)

# Optionally, write to a file
with open('output.json', 'w') as f:
    f.write(json_output)
