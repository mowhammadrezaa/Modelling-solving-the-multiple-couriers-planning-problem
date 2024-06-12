import os
import math


def check_triangular_inequality(distance_matrix_):
    n = len(distance_matrix_)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                if i != j and i != k and j != k:
                    if distance_matrix_[i][j] > distance_matrix_[i][k] + distance_matrix_[k][j]:
                        return False
    return True


def is_symmetric_m(matrix):
    # Check if the matrix is equal to its transpose
    return all(matrix[i][j] == matrix[j][i] for i in range(len(matrix)) for j in range(len(matrix[0])))


def read_dat_file(dat_file):
    with open(dat_file, 'r') as file:
        lines = file.readlines()

    m = int(lines[0].strip())  # Number of couriers
    n = int(lines[1].strip())  # Number of items
    capacities = sorted(list(map(int, lines[2].split())), reverse=True)  # Courier capacities
    item_sizes = list(map(int, lines[3].split()))  # Item sizes
    distance_matrix = [list(map(int, line.split())) for line in lines[4:]]

    # compute min-used capacities
    extra_resources = sum(capacities) - sum(item_sizes)
    is_extra_resource_high = True if min(capacities) - extra_resources < 0 else False

    if is_extra_resource_high:
        min_used_capacities = [min(item_sizes)] * m
    else:
        min_used_capacities = [max(capacity - extra_resources, min(item_sizes)) for capacity in capacities]

    # compute max-used capacities
    max_used_capacities = []
    for capacity in capacities:
        if is_extra_resource_high:
            max_used_capacity = min(int((sum(item_sizes) / m) + 2 * max(item_sizes)), capacity)
        else:
            max_used_capacity = capacity
        max_used_capacities.append(max_used_capacity)

    # compute min durations
    min_durations = [min(math.ceil(min_used_capacity/max(item_sizes)), n-m+1)
                     for min_used_capacity in min_used_capacities]
    # compute max durations
    max_durations = []
    for capacity in max_used_capacities:
        s = 0
        counter = 0
        for item_size in sorted(item_sizes):
            s += item_size
            counter += 1
            if s >= capacity:
                break
        max_durations.append(counter)
    return (m, n,
            capacities,
            item_sizes,
            distance_matrix,
            is_symmetric_m(distance_matrix),
            min_used_capacities,
            max_used_capacities,
            min_durations,
            max_durations
            )


def write_dzn_file(
        dzn_file, m, n,
        capacities,
        item_sizes,
        distance_matrix,
        is_symmetric,
        min_used_capacities,
        max_used_capacities,
        min_durations,
        max_durations
):
    with open(dzn_file, 'w') as file:
        file.write("% MCP DATA\n\n")
        file.write("% Set data parameters\n")
        file.write(f"m = {m}; % Number of couriers\n")
        file.write(f"n = {n}; % Number of items\n")
        file.write(f"capacity = {capacities}; % Courier capacities\n")
        file.write(f"itemSize = {item_sizes}; % Item sizes\n")
        file.write("distanceMatrix = [|")
        for row in distance_matrix:
            file.write(", ".join(map(str, row)) + "\n                  |")
        file.write("];\n")
        file.write(f"is_symmetric = {'true' if is_symmetric else 'false'};\n")
        file.write(f"min_used_capacities = {min_used_capacities};\n")
        file.write(f"max_used_capacities = {max_used_capacities};\n")
        file.write(f"min_durations = {min_durations};\n")
        file.write(f"max_durations = {max_durations};\n")
    return


if __name__ == "__main__":
    input_folder = "instances"
    output_folder = "output_instances"

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".dat"):
            input_dat_file = os.path.join(input_folder, filename)
            output_dzn_file = os.path.join(output_folder, filename.replace(".dat", ".dzn"))
            write_dzn_file(output_dzn_file, *read_dat_file(input_dat_file))
            
            print(f"{output_dzn_file} has been created.")

