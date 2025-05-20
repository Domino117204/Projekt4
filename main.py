import sys
from graph import Graph
from export import export_to_tex

def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ['--hamilton', '--non-hamilton'] or len(sys.argv) >= 3:
        print("Użycie: python main.py --hamilton | --non-hamilton")
        return

    while True:
        try:
            n = int(input("nodes> "))
            if n <= 10:
                print("Liczba wierzchołków musi być większa niż 10.")
            else:
                break
        except ValueError:
            print("Podaj poprawną liczbę całkowitą.")

    graph = Graph(n)
    if sys.argv[1] == '--hamilton':
        while True:
            try:
                saturation = int(input("saturation (30 or 70)> "))
                if saturation not in [30, 70]:
                    print("Saturacja musi być 30 lub 70.")
                else:
                    graph.generate_hamiltonian_graph(saturation_percent=saturation)
                    break
            except ValueError:
                print("Podaj poprawną liczbę całkowitą.")
    else:
        graph.generate_non_hamiltonian_graph()

    while True:
        print("\nWybierz operację:")
        print("1. Wypisanie grafu (lista sąsiedztwa)")
        print("2. Znalezienie cyklu Eulera")
        print("3. Znalezienie cyklu Hamiltona")
        print("4. Eksport do LaTeX")
        print("5. Wyjście")
        choice = input("> ")

        if choice == "1":
            graph.print_graph()
        elif choice == "2":
            cycle = graph.find_euler_cycle()
            if cycle:
                print("Cykl Eulera:", cycle)
            else:
                print("Brak cyklu Eulera.")
        elif choice == "3":
            cycle = graph.find_hamilton_cycle()
            if cycle:
                print("Cykl Hamiltona:", cycle)
            else:
                print("Brak cyklu Hamiltona.")
        elif choice == "4":
            export_to_tex(graph)
        elif choice == "5":
            break
        else:
            print("Nieprawidłowy wybór.")

if __name__ == "__main__":
    main()