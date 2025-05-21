def load_input_variables(file_path):
    local_vars = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
        exec(code, {}, local_vars)
    return local_vars
variables = load_input_variables('OR_Tools/input/input1.py')

# Print all loaded variables
print("\nLoaded variables:")
for var_name, value in variables.items():
    print(f"{var_name}:")
    if isinstance(value, dict):
        # Pretty print dictionaries
        for k, v in value.items():
            print(f"  {k}: {v}")
    elif isinstance(value, list):
        print(f"  {value}")
    else:
        # Print other types directly
        print(f"  {value}")
