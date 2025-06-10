import time
import csv
import random
from concurrent.futures import ThreadPoolExecutor

class Graph:
    def __init__(self, n):
        self.n = n
        self.adj = {i: set() for i in range(1, n + 1)}

    def add_edge(self, u, v):
        if u != v:
            self.adj[u].add(v)
            self.adj[v].add(u)

    def edge_count(self):
        return sum(len(neighbors) for neighbors in self.adj.values()) // 2

    def max_edges(self):
        return self.n * (self.n - 1) // 2

    def generate_hamiltonian_graph(self, saturation_percent):
        nodes = list(range(1, self.n + 1))
        random.shuffle(nodes)
        for i in range(self.n):
            self.add_edge(nodes[i], nodes[(i + 1) % self.n])

        target_edges = int(self.max_edges() * (saturation_percent / 100))
        attempts = 0
        max_attempts = 10000

        while self.edge_count() < target_edges and attempts < max_attempts:
            u, v = random.sample(range(1, self.n + 1), 2)
            if v not in self.adj[u]:
                self.add_edge(u, v)
            attempts += 1

        for node in range(1, self.n + 1):
            if len(self.adj[node]) % 2 != 0:
                for other in range(1, self.n + 1):
                    if other != node and other not in self.adj[node]:
                        self.add_edge(node, other)
                        break

    def generate_non_hamiltonian_graph(self):
        self.n += 1
        self.adj[self.n] = set()  # dodaj izolowany wierzchołek
        for i in range(1, self.n - 1):
            self.add_edge(i, i + 1)

    def is_eulerian(self):
        return all(len(self.adj[v]) % 2 == 0 for v in self.adj)

    def find_euler_cycle(self):
        if not self.is_eulerian():
            return None
        graph_copy = {u: self.adj[u].copy() for u in self.adj}
        stack = []
        circuit = []
        current = next(iter(graph_copy))
        while stack or graph_copy[current]:
            if not graph_copy[current]:
                circuit.append(current)
                current = stack.pop()
            else:
                stack.append(current)
                neighbor = graph_copy[current].pop()
                graph_copy[neighbor].remove(current)
                current = neighbor
        circuit.append(current)
        return circuit[::-1]

    def find_hamilton_cycle(self):
        path = []

        def backtrack(v, visited):
            if len(path) == self.n:
                return path[0] in self.adj[v]
            for u in sorted(self.adj[v], key=lambda x: len(self.adj[x])):
                if u not in visited:
                    visited.add(u)
                    path.append(u)
                    if backtrack(u, visited):
                        return True
                    visited.remove(u)
                    path.pop()
            return False

        for start in range(1, self.n + 1):
            path = [start]
            if backtrack(start, {start}):
                return path + [start]
        return None

def save_to_csv(filename, data):
    print(f"Zapisuję dane do pliku: {filename}")
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['nodes', 'time'])
            writer.writerows(data)
    except IOError as e:
        print(f"Błąd zapisu do pliku {filename}: {e}")

def run_benchmark_for_n(n, saturation_ham, saturation_nonham):
    results = {}
    print(f"\n[Hamilton] Tworzenie grafu Hamiltonowskiego z n={n}, nasycenie={saturation_ham}%")
    g = Graph(n)
    g.generate_hamiltonian_graph(saturation_ham)

    print("  - Pomiar czasu cyklu Eulera...")
    start = time.perf_counter()
    _ = g.find_euler_cycle()
    elapsed = time.perf_counter() - start
    results['euler'] = (n, elapsed)

    print("  - Pomiar czasu cyklu Hamiltona...")
    start = time.perf_counter()
    _ = g.find_hamilton_cycle()
    elapsed = time.perf_counter() - start
    results['hamilton'] = (n, elapsed)

    return results

def run_benchmark_for_nonham(n):
    results = {}
    print(f"\n[Non-Hamilton] Tworzenie grafu NIE-hamiltonowskiego z n={n}")
    g = Graph(n)
    g.generate_non_hamiltonian_graph()

    print("  - Pomiar czasu cyklu Hamiltona (dla grafu niehamiltonowskiego)...")
    start = time.perf_counter()
    _ = g.find_hamilton_cycle()
    elapsed = time.perf_counter() - start
    results['nonham_hamilton'] = (n, elapsed)

    return results

def benchmark():
    n_values_ham = [10, 12, 14, 16, 18, 20, 22, 24]
    n_values_nonham = [20, 22, 24, 26, 28, 30]
    saturation_ham = 30
    saturation_nonham = 50

    euler_times = []
    hamilton_times = []
    nonham_hamilton_times = []

    with ThreadPoolExecutor() as executor:
        ham_results = list(executor.map(lambda n: run_benchmark_for_n(n, saturation_ham, saturation_nonham), n_values_ham))
        nonham_results = list(executor.map(run_benchmark_for_nonham, n_values_nonham))

    for result in ham_results:
        euler_times.append(result['euler'])
        hamilton_times.append(result['hamilton'])

    for result in nonham_results:
        nonham_hamilton_times.append(result['nonham_hamilton'])

    save_to_csv('euler_times.csv', euler_times)
    save_to_csv('hamilton_times.csv', hamilton_times)
    save_to_csv('nonham_hamilton_times.csv', nonham_hamilton_times)

    print("\nBenchmark zakończony.")

if __name__ == "__main__":
    benchmark()