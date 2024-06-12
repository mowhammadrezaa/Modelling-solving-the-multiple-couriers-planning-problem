# Modelling Solving the Multiple Couriers Planning Problem

## Description

In the age of online deliveries, especially heightened by the COVID-19 pandemic, efficient scheduling of dispatching items through multiple couriers has become crucial for companies. This project aims to solve the Multiple Couriers Planning (MCP) problem. The objective is to assign items to couriers and plan their tours in a way that minimizes the total tour distance while respecting each courier's load capacity.

## Key Features

- **Optimizes courier assignments and routes**
- **Minimizes transportation costs**
- **Handles varying item sizes and courier capacities**
- **Supports large problem instances**

## Installation Instructions

1. **Install MiniZinc:**
   Download and install MiniZinc from [MiniZinc Downloads](https://www.minizinc.org/).

2. **Install Python:**
   Download and install Python from [Python Downloads](https://www.python.org/downloads/).


## Usage Guidelines

1. **Prepare Input Instances:**
   - Create a folder named `instances`.
   - Add input `.dat` files to the `instances` folder. Each file should contain:
     - Number of couriers (`m`)
     - Number of locations (`n`)
     - List of courier capacities
     - List of item sizes
     - An (n+1) x (n+1) distance matrix, where index 0 is the origin point
     Example:
     ```
     2
     3
     50 100
     50 20 80
     0 1 2 1
     2 0 4 5
     1 2 0 4
     4 3 1 0
     ```

2. **Generate Input Files with Python:**
   ```sh
   python dat2dzn.py
   ```

3. **Use MiniZinc IDE:**
   - Download and open the MiniZinc IDE.
   - Open `model.mzn` and a specific `.dzn` instance created by `dat2dzn.py`.
   - Choose the `chuffed` solver.
   - In the configuration editor (top right), set the optimization level to `-O2 (two pass compilation)`.
   - Run the model.

4. **Output Format:**
   ```
   assignment = [4, 3, 1, 2, 5, 6];
   start = [1, 4];
   end = [3, 6];
   used_capacity = [14, 10];
   duration = [3, 3];
   distance_traveled = [14, 14];
   _objective = 14;
   ```
   - `assignment`: item identifiers
   - `start` and `end`: range of assignments for each courier
   - `duration`: number of items each courier handles
   - `distance_traveled`: travel distance for each courier
   - `_objective`: maximum distance traveled among all couriers

## Contribution Guidelines

1. **Solve the MCP problem using different techniques** (SAT, SMT, LP).
2. **Introduce algorithms to optimize large instances:**
   - Handle high item numbers and large capacity-item size gaps.
3. **Fork the repository:**
   ```sh
   git clone https://github.com/your-repo.git
   ```
4. **Create a new branch:**
   ```sh
   git checkout -b new-feature
   ```
5. **Make your changes and submit a pull request.**

## Relevant Links and Resources

- [MiniZinc Downloads](https://www.minizinc.org/downloads.html)
- [Python Downloads](https://www.python.org/downloads/)
- [MiniZinc Python Library](https://pypi.org/project/minizinc/)

---

Feel free to reach out if you have any questions or need further assistance. Happy optimizing!