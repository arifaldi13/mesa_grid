import os
import itertools
import numpy as np

class InlistManager:
    def __init__(self, filename):
        self.filename = filename
        self.blocks = self.load_inlist()

    def load_inlist(self):
        """Load the inlist file into a dictionary of blocks, ignoring comments and commented parameters."""
        blocks = {}
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                current_block = None
                for line in f:
                    line = line.strip()
                    if line.startswith("!"):  # Skip fully commented lines
                        continue
                    if line.startswith("&"):  # Block start
                        current_block = line[1:].split("!")[0].strip()  # Ignore inline comments
                        blocks[current_block] = {}
                    elif line == "/":  # Block end
                        current_block = None
                    elif current_block and "=" in line:
                        # Skip inline commented lines
                        if line.strip().startswith("!"):
                            continue
                        # Parse parameter and value, ignoring inline comments
                        param, value = line.split('=', 1)
                        param = param.split("!")[0].strip()
                        value = value.split("!")[0].strip()
                        blocks[current_block][param] = value
        return blocks

    def save_inlist(self, filename=None):
        """Save the current blocks and parameters to the given inlist file."""
        if not filename:
            filename = self.filename
        with open(filename, 'w') as f:
            for block, params in self.blocks.items():
                f.write(f"&{block}\n")
                for param, value in params.items():
                    f.write(f"  {param} = {value}\n")
                f.write("/\n\n")

    def add_parameter(self, block, param, value):
        """Add or update a parameter in a specific block."""
        if block not in self.blocks:
            self.blocks[block] = {}
        self.blocks[block][param] = value
        self.save_inlist()

    def remove_parameter(self, block, param):
        """Remove a parameter from a specific block."""
        if block in self.blocks and param in self.blocks[block]:
            del self.blocks[block][param]
            self.save_inlist()
        else:
            print(f"Parameter '{param}' not found in block '{block}'.")

    def update_parameter(self, block, param, value):
        """Update an existing parameter in a specific block."""
        if block in self.blocks and param in self.blocks[block]:
            self.blocks[block][param] = value
            self.save_inlist()
        else:
            print(f"Parameter '{param}' not found in block '{block}'.")

    def get_parameter(self, block, param):
        """Get the value of a parameter from a specific block."""
        if block in self.blocks:
            return self.blocks[block].get(param, None)
        else:
            print(f"Block '{block}' not found.")
            return None

    def generate_inlists(self, param_sets=None, table_file=None):
        """Generate inlist files for all combinations of parameters."""
        if param_sets:
            # Generate all combinations of parameter values
            param_combinations = itertools.product(*[values[0] for values in param_sets.values()])

            for i, param_values in enumerate(param_combinations):
                # Create a copy of the current inlist manager to modify
                temp_inlist = InlistManager(self.filename)

                # Update parameters with the current combination
                for param, (values, block) in param_sets.items():
                    value = param_values[list(param_sets.keys()).index(param)]
                    temp_inlist.add_parameter(block, param, value)

                # Generate the filename for the inlist
                file_name = f"inlist_{i+1}.txt"

                # Save the modified inlist to a new file
                temp_inlist.save_inlist(file_name)
                print(f"Generated {file_name}")
        elif table_file:
            # Load the table using NumPy
            data = np.loadtxt(table_file, dtype=str, delimiter=None)

            # Extract parameter names and block names
            param_names = data[0]  # First row
            block_names = data[1]  # Second row

            # Extract values as rows (starting from the third row)
            values = data[2:]

            # Iterate over rows of parameter values
            for i, row in enumerate(values):
                # Create a copy of the current inlist manager to modify
                temp_inlist = InlistManager(self.filename)

                # Update parameters with values from the current row
                for param, block, value in zip(param_names, block_names, row):
                    temp_inlist.add_parameter(block, param, value)

                # Generate the filename for the inlist
                file_name = f"inlist_{i+1}.txt"

                # Save the modified inlist to a new file
                temp_inlist.save_inlist(file_name)
                print(f"Generated {file_name}")

    def run_grid(self, param_sets=None, table_file=None):
        """Generate inlist files for all combinations of parameters."""
        if param_sets:
            # Generate all combinations of parameter values
            param_combinations = itertools.product(*[values[0] for values in param_sets.values()])

            for i, param_values in enumerate(param_combinations):
                # Create a copy of the current inlist manager to modify
                temp_inlist = InlistManager(self.filename)

                # Update parameters with the current combination
                for param, (values, block) in param_sets.items():
                    value = param_values[list(param_sets.keys()).index(param)]
                    temp_inlist.add_parameter(block, param, value)

                # Run the combination
                temp_inlist.save_inlist()
                print(f"Running the combination no. {i+1}")
                os.system("./rn")
        elif table_file:
            # Load the table using NumPy
            data = np.loadtxt(table_file, dtype=str, delimiter=None)

            # Extract parameter names and block names
            param_names = data[0]  # First row
            block_names = data[1]  # Second row

            # Extract values as rows (starting from the third row)
            values = data[2:]

            # Iterate over rows of parameter values
            for i, row in enumerate(values):
                # Create a copy of the current inlist manager to modify
                temp_inlist = InlistManager(self.filename)

                # Update parameters with values from the current row
                for param, block, value in zip(param_names, block_names, row):
                    temp_inlist.add_parameter(block, param, value)

                # Run the combination
                temp_inlist.save_inlist()
                print(f"Running the combination no. {i+1}")
                os.system("./rn")
