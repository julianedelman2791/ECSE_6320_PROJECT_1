import time
import numpy as np
import mmap

# Measure read/write latency and throughput
def measure_latency_throughput(buffer_size, operation, throughput_level, total_operations=10000):
    data = np.random.bytes(buffer_size)
    max_delay = 0.01

    # Memory-mapped buffer to simulate memory access
    with mmap.mmap(-1, buffer_size) as m:
        start_time = time.time()
        total_latency = 0

        for i in range(total_operations):
            operation_start = time.time()

            # Simulate read or write based on the operation
            if operation == 'read':
                m.seek(0)
                m.read(buffer_size)
            elif operation == 'write':
                m.seek(0)
                m.write(data)

            # Calculate latency
            operation_latency = time.time() - operation_start
            total_latency += operation_latency

            if i % 1000 == 0:
                print(f'Operation {i}/{total_operations}, Latency: {operation_latency:.6f} s')

            delay = min((1 / throughput_level) - operation_latency, max_delay)  # Control throughput, with max delay
            if delay > 0:
                time.sleep(delay)

        end_time = time.time()

    elapsed_time = end_time - start_time
    avg_latency = total_latency / total_operations
    total_throughput = total_operations / elapsed_time

    return avg_latency * 1e6, total_throughput

# Run experiment for different throughput levels
def run_latency_throughput_experiment():
    buffer_size = 1024
    operations = ['read', 'write']
    throughput_levels = [100, 500, 1000, 5000, 10000]

    # Open a CSV file to save results
    with open('latency_throughput_results.csv', 'w') as f:
        f.write('Operation,Throughput Level (ops/sec),Latency (us),Actual Throughput (ops/sec)\n')
        
        for operation in operations:
            print(f'--- Running {operation.upper()} operations ---')
            for throughput in throughput_levels:
                print(f'-- Throughput Level: {throughput} ops/sec --')
                avg_latency, actual_throughput = measure_latency_throughput(buffer_size, operation, throughput)
                f.write(f'{operation},{throughput},{avg_latency:.2f},{actual_throughput:.2f}\n')
                print(f'Operation: {operation} | Throughput Level: {throughput} ops/sec | '
                      f'Latency: {avg_latency:.2f} us | Throughput: {actual_throughput:.2f} ops/sec')

if __name__ == "__main__":
    run_latency_throughput_experiment()