import random

class Graph:
    def __init__(self, n):
        """Inicjalizacja pustego grafu o n wierzchołkach."""
        self.n = n
        self.adj = {i: set() for i in range(n)}  # lista sąsiedztwa

    def add_edge(self, u, v):
        """Dodaje krawędź między u i v."""
        if u != v:
            self.adj[u].add(v)
            self.adj[v].add(u)

    def edge_count(self):
        """Zwraca liczbę krawędzi."""
        return sum(len(neighbors) for neighbors in self.adj.values()) // 2

    def max_edges(self):
        """Maksymalna liczba krawędzi w grafie nieskierowanym bez pętli."""
        return self.n * (self.n - 1) // 2

    def print_graph(self):
        """Wypisuje graf jako listę sąsiedztwa."""
        print("\nGraph adjacency list:")
        for node in sorted(self.adj):
            print(f"{node}: {sorted(self.adj[node])}")

    def generate_hamiltonian_graph(self, saturation_percent):
        """Tworzy spójny graf hamiltonowski z podanym nasyceniem i parzystymi stopniami."""
        nodes = list(range(self.n))
        random.shuffle(nodes)
        for i in range(self.n):
            self.add_edge(nodes[i], nodes[(i + 1) % self.n])  # cykl

        target_edges = int(self.max_edges() * (saturation_percent / 100))
        while self.edge_count() < target_edges:
            u, v, w = random.sample(range(self.n), 3)
            if v not in self.adj[u] and w not in self.adj[v] and u not in self.adj[w]:
                self.add_edge(u, v)
                self.add_edge(v, w)
                self.add_edge(w, u)

        for node in self.adj:
            if len(self.adj[node]) % 2 != 0:
                for other in range(self.n):
                    if other != node and other not in self.adj[node]:
                        self.add_edge(node, other)
                        break

    def generate_non_hamiltonian_graph(self):
        """Tworzy graf z nasyceniem 50%, ale nie hamiltonowski (izolując jeden wierzchołek)."""
        self.generate_hamiltonian_graph(saturation_percent=50)

        isolated = random.choice(list(self.adj.keys()))
        for neighbor in list(self.adj[isolated]):
            self.adj[neighbor].remove(isolated)
        self.adj[isolated].clear()
