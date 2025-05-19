import sys
from graph import Graph
from algorithms import find_euler_cycle, find_hamilton_cycle

def main():
    if len(sys.argv) < 2:
        print("Usage: ./program --hamilton | --non-hamilton")
        return

    mode = sys.argv[1]
    n = int(input("nodes> "))
    saturation = int(input("saturation> ")) if mode == '--hamilton' else 50

    graph = Graph(n)

    if mode == '--hamilton':
        graph.generate_hamiltonian_graph(saturation)
    elif mode == '--non-hamilton':
        graph.generate_non_hamiltonian_graph()
    else:
        print("Invalid mode")
        return

    graph.print_graph()

    print("\nEuler cycle:", find_euler_cycle(graph))
    print("Hamilton cycle:", find_hamilton_cycle(graph))

if __name__ == "__main__":
    main()
