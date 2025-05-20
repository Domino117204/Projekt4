import random

class Graph:
    def __init__(self, n):
        self.n = n
        self.adj = {i: set() for i in range(1, n + 1)}  # 1-based

    def add_edge(self, u, v):
        if u != v:
            self.adj[u].add(v)
            self.adj[v].add(u)

    def edge_count(self):
        return sum(len(neighbors) for neighbors in self.adj.values()) // 2

    def max_edges(self):
        return self.n * (self.n - 1) // 2

    def print_graph(self):
        print("\nGraph adjacency list:")
        for node in sorted(self.adj):
            print(f"{node}: {sorted(self.adj[node])}")

    def generate_hamiltonian_graph(self, saturation_percent):
        nodes = list(range(1, self.n + 1))
        random.shuffle(nodes)
        for i in range(self.n):
            self.add_edge(nodes[i], nodes[(i + 1) % self.n])  # Cykl

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

    def generate_non_hamiltonian_graph(self):
        self.generate_hamiltonian_graph(saturation_percent=50)
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

    def find_hamilton_cycle(self):
        path = []

        def backtrack(v, visited):
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
            if backtrack(start, {start}):
                return path + [start]
        return None