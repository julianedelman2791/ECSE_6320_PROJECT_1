import time
import numpy as np
import matplotlib.pyplot as plt

# Perform matrix multiplication and measure execution time
def measure_matrix_multiplication(size):

    A = np.random.rand(size, size)
    B = np.random.rand(size, size)

    start_time = time.time()
    C = np.dot(A, B)
    end_time = time.time()

    return end_time - start_time

# Run the experiment for multiple matrix sizes
def run_cache_miss_experiment():
    matrix_sizes = [100, 200, 500, 1000, 2000, 3000]

    execution_times = []

    for size in matrix_sizes:
        time_taken = measure_matrix_multiplication(size)
        execution_times.append(time_taken)
        print(f'Matrix Size: {size}x{size} | Time Taken: {time_taken:.6f} seconds')

    # Save the results in a CSV
    with open('cache_miss_experiment_results.csv', 'w') as f:
        f.write('Matrix Size,Time Taken (s)\n')
        for size, time_taken in zip(matrix_sizes, execution_times):
            f.write(f'{size},{time_taken:.6f}\n')

    return matrix_sizes, execution_times

# Run the experiment
matrix_sizes, execution_times = run_cache_miss_experiment()