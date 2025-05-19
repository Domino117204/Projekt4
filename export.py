import math

def export_to_tex(graph, filename="graph.tex"):
    edges = set()
    for u in range(graph.n):
        for v in graph.adj[u]:
            if (v, u) not in edges:  # unikamy duplikacji w grafie nieskierowanym
                edges.add((u, v))

    with open(filename, "w") as f:
        f.write("\\documentclass{article}\n")
        f.write("\\usepackage{tikz}\n")
        f.write("\\begin{document}\n")
        f.write("\\begin{tikzpicture}[>=stealth,shorten >=1pt,auto,node distance=3cm,thick]\n")
        f.write("\\tikzstyle{every node}=[circle,draw,minimum size=8mm]\n\n")

        node_positions = {}
        angle_step = 360 / graph.n
        radius = 5

        for i in range(graph.n):
            angle = i * angle_step
            x = radius * math.cos(math.radians(angle))
            y = radius * math.sin(math.radians(angle))
            node_positions[i] = (x, y)
            f.write(f"\\node ({i}) at ({x:.2f},{y:.2f}) {{{i}}};\n")

        f.write("\n")

        for u, v in edges:
            f.write(f"\\draw ({u}) -- ({v});\n")

        f.write("\\end{tikzpicture}\n")
        f.write("\\end{document}\n")

    print(f"Graph exported to {filename}")
