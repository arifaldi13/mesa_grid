# MESA Grid Simulation Tool

This Python script, `mesa_grid.py`, provides a set of utilities to manage and run grid simulations using the MESA stellar evolution code. It simplifies the creation of inlist files for parameter studies and automates the execution of simulations for multiple parameter combinations.

## Features

1. **Inlist Management**:
   - Load, modify, and save MESA inlist files.
   - Handle blocks and parameters in a structured format.
   - Supports comments in inlist files (`!`).

2. **Grid Simulation**:
   - Automatically generate inlist files for grid simulations based on:
     - Parameter sets in `dictionary` type.
     - Parameter tables loaded from a file (using `run_grid_from_table`).

3. **Automation of MESA Runs**:
   - Sequentially run MESA simulations for each generated inlist file.
   - Organize and manage output data efficiently.

## Requirements

- Python 3.x
- NumPy
- MESA installed and configured in the system.

## Installation

Clone the repository or copy `mesa_grid.py` into your work folder. Ensure Python and MESA are properly installed and accessible via the command line. It uses `os`, `itertools`, and `numpy` library, so make sure those are installed.

## Usage

### 1. Import the `InlistManager` Class

```python
from mesa_grid import InlistManager
```

### 2. Initialize with a Template Inlist

Create an instance of `InlistManager` with a inlist file:

```python
inlist_manager = InlistManager("inlist")
```

The inlist file could already exist or you may write a new one using this code.

### 3. Inlist Editing

Use the following methods to modify the inlist programmatically:

- **Add a Parameter:**

  ```python
  inlist.add_parameter("section_name", "new_param", "value")
  ```
  
  Example:
  
  ```python
  inlist.add_parameter("controls", "initial_mass", "3.2")
  ```

  Please note that the value should be in `string` type. If the value you desired already a string, use secondary quotation marks inside, for example `"'profile_columns.list'"`.

- **Remove a Parameter:**

  ```python
  inlist.remove_parameter("controls", "initial_mass")
  ```

- **Update a Parameter:**

  ```python
  inlist.update_parameter("controls", "initial_mass", "5")
  ```

- **Get a Parameter:**

  ```python
  value = inlist.get_parameter("controls", "initial_mass")
  print(value)  # Outputs the value of initial_mass


### 4. Generate Inlist Files

#### Using Parameter Sets

Provide a dictionary of parameter sets, including the block name for each parameter:

```python
param_sets = {
        "initial_mass": ([1, 2, 3, 4], "controls"),
        "initial_z": ([0.01, 0.02, 0.03], "controls")
}

inlist_manager.generate_inlists(param_sets)
```

This generates inlist files for all combinations of `initial_mass` and `initial_z`.

#### Using a Parameter Table

For example, create a text file (e.g., `parameter_table.txt`) in the following format:

```
initial_mass   initial_z
controls       controls
1              0.01
1              0.02
2              0.01
2              0.02
```

Run:

```python
inlist_manager.generate_inlists(table_file = "parameter_table.txt")
```

This generates inlist files for each row in the table.

### 4. Run MESA Simulations

#### Using Parameter Sets

Directly execute simulations for all parameter combinations:

```python
inlist_manager.run_grid(param_sets)
```

#### Using a Parameter Table

Directly execute simulations for all rows in the parameter table:

```python
inlist_manager.run_grid(table_file = "parameter_table.txt")
```

Each simulation runs sequentially using the MESA executable `.\rn`, and the outputs are organized automatically.

## License

This tool is provided under the MIT License. You are free to modify and use it for your simulations. I will be glad if you mention this work in your acknowledgment.

## Acknowledgments

This tool is designed to streamline grid simulations in MESA and is inspired by the need for efficient parameter studies in stellar evolution research. See the [MESA website](https://docs.mesastar.org).

---

Feel free to adjust the content to match any additional functionality or context you want to include!
