import json
from pathlib import Path

def remove_double_quotes(filename):
    path = Path(filename)
    if not path.exists():
        print(f"File '{filename}' does not exist.")
        return

    with open(path, 'r') as file:
        data = json.load(file)

    # Function to check if a string contains only numbers (including negative numbers)
    def contains_only_numbers(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    # Recursive function to iterate through the JSON data
    def process_json(data):
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, str) and contains_only_numbers(value):
                    data[key] = int(value) if value.isdigit() else float(value)
                elif key in ["maneuvers", "sharedWith", "typeAttributes"]:
                    if isinstance(value, list):
                        data[key] = [int(item) if item.isdigit() or item.startswith('-') else item for item in value]
                elif isinstance(value, (dict, list)):
                    process_json(value)
        elif isinstance(data, list):
            for item in data:
                process_json(item)

    process_json(data)

    new_filename = path.stem + "_modified" + path.suffix
    with open(new_filename, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"StringModified JSON saved as {new_filename}")

# Usage example
filename = "ISD_11090_RSU#05_MAPEM.json"
remove_double_quotes(filename)
