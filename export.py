import math

def export_to_tex(graph, filename="graph.tex", directed=False):
    """
    Eksportuje graf do pliku LaTeX z użyciem pakietu TikZ.
    """
    if graph.n == 0:
        print("Graf jest pusty, eksport przerwany.")
        return

    edges = set()
    for u in range(graph.n):
        for v in graph.adj[u]:
            if directed or (v, u) not in edges:
                edges.add((u, v))

    with open(filename, "w") as f:
        f.write("\\documentclass{article}\n")
        f.write("\\usepackage{tikz}\n")
        f.write("\\begin{document}\n")
        f.write("\\begin{center}\n")
        f.write("\\begin{tikzpicture}[auto, node distance=3cm, thick]\n")
        f.write("\\tikzstyle{every node}=[circle,draw,minimum size=8mm,inner sep=1pt]\n\n")

        angle_step = 360 / graph.n
        radius = 5
        for i in range(graph.n):
            angle = i * angle_step
            x = radius * math.cos(math.radians(angle))
            y = radius * math.sin(math.radians(angle))
            f.write(f"\\node ({i}) at ({x:.2f},{y:.2f}) {{{i}}};\n")

        f.write("\n")

        for u, v in edges:
            arrow = "->" if directed else "--"
            f.write(f"\\draw ({u}) {arrow} ({v});\n")

        f.write("\\end{tikzpicture}\n")
        f.write("\\end{center}\n")
        f.write("\\end{document}\n")

    print(f"Graph exported to {filename}")