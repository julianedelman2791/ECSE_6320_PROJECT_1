import time
import mmap
import os

# Measure read/write latency using chunking
def measure_latency(buffer_size, iterations=100000):
    chunk_size = 4096
    data = bytearray(min(buffer_size, chunk_size))

    # Memory-map the buffer
    with mmap.mmap(-1, buffer_size) as m:
        start_write = time.time()
        for _ in range(iterations):
            for i in range(0, buffer_size, chunk_size):
                m.seek(i)
                m.write(data)
        end_write = time.time()
        write_latency = (end_write - start_write) / iterations

        # Measure read latency
        start_read = time.time()
        for _ in range(iterations):
            for i in range(0, buffer_size, chunk_size):
                m.seek(i)
                m.read(chunk_size)
        end_read = time.time()
        read_latency = (end_read - start_read) / iterations

    return write_latency, read_latency

# Run latency measurements for different buffer sizes
def main():
    buffer_sizes = [64, 256, 1024, 4096, 16384]
    results = []

    for buffer_size in buffer_sizes:
        write_lat, read_lat = measure_latency(buffer_size)
        results.append({
            'buffer_size': buffer_size,
            'write_latency': write_lat,
            'read_latency': read_lat
        })
        print(f"Buffer Size: {buffer_size}B | Write Latency: {write_lat * 1e9:.2f} ns | Read Latency: {read_lat * 1e9:.2f} ns")

    # Save the results to a CSV file
    with open('latency_results.csv', 'w') as f:
        f.write('Buffer Size (B),Write Latency (ns),Read Latency (ns)\n')
        for result in results:
            f.write(f"{result['buffer_size']},{result['write_latency'] * 1e9},{result['read_latency'] * 1e9}\n")

if __name__ == "__main__":
    main()