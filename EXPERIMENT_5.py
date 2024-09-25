import time
import numpy as np

# Perform matrix multiplication and simulate TLB misses by spreading data across memory pages
def measure_matrix_multiplication_with_tlb(size, stride):

    A = np.random.rand(size, size)
    B = np.random.rand(size, size)

    start_time = time.time()
    C = np.zeros((size, size))
    
    for i in range(0, size, stride):
        if i + stride <= size:
            C[i:i+stride, :] = np.dot(A[i:i+stride, :], B)

    end_time = time.time()

    return end_time - start_time

# Run the TLB miss experiment with varying matrix sizes and strides
def run_tlb_miss_experiment():

    matrix_sizes = [100, 200, 500, 1000, 2000, 3000]
    stride_sizes = [8, 16, 32, 64, 128]

    execution_times = []

    for size in matrix_sizes:
        for stride in stride_sizes:
            time_taken = measure_matrix_multiplication_with_tlb(size, stride)
            execution_times.append((size, stride, time_taken))
            print(f'Matrix Size: {size}x{size} | Stride: {stride} | Time Taken: {time_taken:.6f} seconds')

    # Save the results to a CSV
    with open('tlb_miss_experiment_corrected.csv', 'w') as f:
        f.write('Matrix Size,Stride,Time Taken (s)\n')
        for size, stride, time_taken in execution_times:
            f.write(f'{size},{stride},{time_taken:.6f}\n')

    return execution_times

# Run the experiment
run_tlb_miss_experiment()