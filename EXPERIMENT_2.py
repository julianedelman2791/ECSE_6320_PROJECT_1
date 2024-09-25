import time
import numpy as np
import mmap

# Measure memory bandwidth for different read/write intensity ratios
def measure_bandwidth(buffer_size, access_pattern, total_iterations=10**6):
    data = np.random.bytes(buffer_size)
    chunk_size = 4096

    # Memory-mapped buffer for simulating main memory access
    with mmap.mmap(-1, buffer_size) as m:
        start_time = time.time()
        for i in range(total_iterations):
            if access_pattern == 'read_only':
                m.seek(0)
                m.read(buffer_size)
            elif access_pattern == 'write_only':
                m.seek(0)
                for j in range(0, buffer_size, chunk_size):
                    m.write(data[j:j+chunk_size])
            elif access_pattern == '70_read_30_write':
                if i % 10 < 7:
                    m.seek(0)
                    m.read(buffer_size)
                else:
                    m.seek(0)
                    for j in range(0, buffer_size, chunk_size):
                        m.write(data[j:j+chunk_size])
            elif access_pattern == '50_read_50_write':
                if i % 2 == 0:
                    m.seek(0)
                    m.read(buffer_size)
                else:
                    m.seek(0)
                    for j in range(0, buffer_size, chunk_size):
                        m.write(data[j:j+chunk_size])

        end_time = time.time()

    elapsed_time = end_time - start_time
    total_data_accessed = buffer_size * total_iterations

    bandwidth = total_data_accessed / elapsed_time
    return bandwidth / (1024 ** 3)

# Run experiment for different buffer sizes and access patterns
def run_bandwidth_experiment():
    buffer_sizes = [64, 256, 1024]
    access_patterns = ['read_only', 'write_only', '70_read_30_write', '50_read_50_write']

    # Save results
    with open('bandwidth_results.csv', 'w') as f:
        f.write('Buffer Size (B), Access Pattern, Bandwidth (GB/s)\n')
        for buffer_size in buffer_sizes:
            for pattern in access_patterns:
                bandwidth = measure_bandwidth(buffer_size, pattern)
                f.write(f'{buffer_size}, {pattern}, {bandwidth:.2f}\n')
                print(f'Buffer Size: {buffer_size}B | Access Pattern: {pattern} | Bandwidth: {bandwidth:.2f} GB/s')

if __name__ == "__main__":
    run_bandwidth_experiment()