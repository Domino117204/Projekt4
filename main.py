import sys
from graph import Graph
from export import export_to_tex

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ['--hamilton', '--non-hamilton']:
        print("Użycie: python main.py --hamilton | --non-hamilton")
        return

    n = int(input("nodes> "))
    if n <= 10:
        print("Liczba wierzchołków musi być większa niż 10.")
        return

    if sys.argv[1] == '--hamilton':
        saturation = int(input("saturation (30 or 70)> "))
        if saturation not in [30, 70]:
            print("Saturacja musi być 30 lub 70.")
            return
        graph = Graph(n)
        graph.generate_hamiltonian_graph(saturation_percent=saturation)

    elif sys.argv[1] == '--non-hamilton':
        graph = Graph(n)
        graph.generate_non_hamiltonian_graph()

    graph.print_graph()
    export_to_tex(graph, "graph_output.tex")

if __name__ == "__main__":
    main()