import time
import os
import csv
from graph import Graph
import sys
sys.setrecursionlimit(10000^6)

def benchmark():
    folder = "Sprawozdanie/results"
    os.makedirs(folder, exist_ok=True)

    # 1. Grafy Hamiltonowskie, nasycenie 30%, n od 2^15 do 2^20
    ns_large = [2 ** i for i in range(5, 11)]
    euler_times = []
    hamilton_times = []

    print("Benchmark grafów hamiltonowskich (nasycenie 30%)")
    for n in ns_large:
        print(f"n={n}")
        g = Graph(n)
        g.generate_hamiltonian_graph(saturation_percent=30)

        start = time.perf_counter()
        g.find_euler_cycle()
        euler_times.append(time.perf_counter() - start)

        start = time.perf_counter()
        g.find_hamilton_cycle()
        hamilton_times.append(time.perf_counter() - start)

    # 2. Grafy niehamiltonowskie, nasycenie 50%, n = 20..30
    ns_small = list(range(20, 31))
    nonhamilton_times = []

    print("\nBenchmark grafów niehamiltonowskich (nasycenie 50%)")
    for n in ns_small:
        print(f"n={n}")
        g = Graph(n)
        # Usuń saturation_percent, jeśli metoda go nie obsługuje
        g.generate_non_hamiltonian_graph()

        start = time.perf_counter()
        g.find_hamilton_cycle()
        nonhamilton_times.append(time.perf_counter() - start)

if __name__ == "__main__":
    benchmark()

