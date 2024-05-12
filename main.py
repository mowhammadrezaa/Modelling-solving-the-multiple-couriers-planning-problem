from minizinc import Instance, Model, Solver
from dat2dzn import read_dat_file
import os


def run_minizinc_model(dat_file, model_file="main.mzn"):
    model = Model(model_file)

    # Use the Gecode solver (adjust based on your available solvers)
    solver = Solver.lookup("gecode")
    instance = Instance(solver, model)
    input_data = read_dat_file(dat_file)
    instance.input['m'] = input_data[0]
    instance.input['n'] = input_data[1]
    instance.input['capacities'] = input_data[2]
    instance.input['item_sizes'] = input_data[3]
    instance.input['distance_matrix'] = input_data[4]

    result = instance.solve()

    if result:
        max_distance = instance["maxDistance"]
        print(f"Max Distance for {dat_file}: {max_distance}")
    else:
        print(f"Failed to find a solution for {dat_file}")


if __name__ == "__main__":
    input_folder = "instances"  # Replace with the folder containing generated .dzn files

    for filename in os.listdir(input_folder):
        if filename.endswith(".dat"):
            input_dat_file = os.path.join(input_folder, filename)
            run_minizinc_model(input_dat_file)
        break
