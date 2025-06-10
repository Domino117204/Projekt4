import time
import csv
import random
import sys

sys.setrecursionlimit(10000)

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
            self.add_edge(nodes[i], nodes[(i + 1) % self.n])  # cykl

        target_edges = int(self.max_edges() * (saturation_percent / 100))
        while self.edge_count() + 3 <= target_edges:
            u, v, w = random.sample(range(1, self.n + 1), 3)
            if v not in self.adj[u] and w not in self.adj[v] and u not in self.adj[w]:
                self.add_edge(u, v)
                self.add_edge(v, w)
                self.add_edge(w, u)

        for node in range(1, self.n + 1):
            if len(self.adj[node]) % 2 != 0:
                for other in range(1, self.n + 1):
                    if other != node and other not in self.adj[node]:
                        self.add_edge(node, other)
                        break

    def generate_non_hamiltonian_graph(self, saturation_percent):
        self.generate_hamiltonian_graph(saturation_percent)
        # Izoluj ostatni wierzchołek
        isolated = self.n
        for neighbor in list(self.adj[isolated]):
            self.adj[neighbor].remove(isolated)
        self.adj[isolated].clear()

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

    def find_hamilton_cycle(self, timeout=10):
        path = []
        start_time = time.perf_counter()

        def backtrack(v, visited):
            if time.perf_counter() - start_time > timeout:
                raise TimeoutError("Hamilton search timeout.")
            if len(path) == self.n:
                return path[0] in self.adj[v]
            for u in self.adj[v]:
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
            try:
                if backtrack(start, {start}):
                    return path + [start]
            except TimeoutError:
                return None
        return None

def run_experiment():
    n_values = list(range(50, 201, 10))  # np. 10, 15, ..., 30
    euler_times = []
    hamilton_times = []

    for n in n_values:
        print(f"[Hamiltonowski] Przetwarzanie n = {n}")
        g = Graph(n)
        g.generate_hamiltonian_graph(saturation_percent=30)

        start = time.perf_counter()
        _ = g.find_euler_cycle()
        euler_time = time.perf_counter() - start
        euler_times.append(euler_time)

        start = time.perf_counter()
        _ = g.find_hamilton_cycle(timeout=10)
        hamilton_time = time.perf_counter() - start
        hamilton_times.append(hamilton_time)

    # Zapis osobno
    with open("czasy_euler.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "time"])
        for i in range(len(n_values)):
            writer.writerow([n_values[i], euler_times[i]])

    with open("czasy_hamilton.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "time"])
        for i in range(len(n_values)):
            writer.writerow([n_values[i], hamilton_times[i]])

    print("✓ Wyniki zapisano do czasy_euler.csv i czasy_hamilton.csv.")


def run_non_hamiltonian_experiment():
    n_values = [20, 25, 30]
    hamilton_times = []

    for n in n_values:
        print(f"[Niehamiltonowski] Przetwarzanie n = {n}")
        g = Graph(n)
        g.generate_non_hamiltonian_graph(saturation_percent=50)

        start = time.perf_counter()
        _ = g.find_hamilton_cycle(timeout=10)
        elapsed = time.perf_counter() - start
        hamilton_times.append(elapsed)

    with open("czasy_niehamilton.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["n", "time"])
        for i in range(len(n_values)):
            writer.writerow([n_values[i], hamilton_times[i]])

    print("✓ Wyniki Niehamiltonowskie zapisano do czasy_niehamilton.csv.")


# Uruchom wszystko
run_experiment()
run_non_hamiltonian_experiment()
