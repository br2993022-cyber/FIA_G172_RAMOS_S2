from collections import deque
import matplotlib.pyplot as plt
import networkx as nx

# Grafo no dirigido que representa caminos entre ubicaciones.
grafo = {
    "A": ["B", "C"],
    "B": ["A", "D", "E"],
    "C": ["A", "F"],
    "D": ["B", "G"],
    "E": ["B", "G", "H"],
    "F": ["C", "H"],
    "G": ["D", "E", "I"],
    "H": ["E", "F", "I"],
    "I": ["G", "H"]
}

INICIO = "A"
META = "I"

def reconstruir_camino(padres, meta):
    camino = []
    actual = meta
    while actual is not None:
        camino.append(actual)
        actual = padres[actual]
    return list(reversed(camino))

def bfs(grafo, inicio, meta):
    """Búsqueda en anchura: explora por niveles y encuentra camino mínimo
    en número de aristas cuando todas las aristas tienen el mismo costo."""
    cola = deque([inicio])
    padres = {inicio: None}
    orden = []

    while cola:
        actual = cola.popleft()
        orden.append(actual)
        if actual == meta:
            return reconstruir_camino(padres, meta), orden
        for vecino in grafo[actual]:
            if vecino not in padres:
                padres[vecino] = actual
                cola.append(vecino)
    return None, orden

def dfs(grafo, inicio, meta):
    """Búsqueda en profundidad: explora una rama antes de retroceder."""
    pila = [inicio]
    padres = {inicio: None}
    orden = []

    while pila:
        actual = pila.pop()
        orden.append(actual)
        if actual == meta:
            return reconstruir_camino(padres, meta), orden
        # reversed conserva un orden de visita fácil de interpretar.
        for vecino in reversed(grafo[actual]):
            if vecino not in padres:
                padres[vecino] = actual
                pila.append(vecino)
    return None, orden

if __name__ == "__main__":
    camino_bfs, orden_bfs = bfs(grafo, INICIO, META)
    camino_dfs, orden_dfs = dfs(grafo, INICIO, META)

    print("BFS - recorrido:", " -> ".join(orden_bfs))
    print("BFS - camino:", " -> ".join(camino_bfs))
    print("BFS - longitud:", len(camino_bfs)-1, "aristas")
    print()
    print("DFS - recorrido:", " -> ".join(orden_dfs))
    print("DFS - camino:", " -> ".join(camino_dfs))
    print("DFS - longitud:", len(camino_dfs)-1, "aristas")

    # Dibuja el grafo y resalta los caminos encontrados.
    G = nx.Graph()
    for nodo, vecinos in grafo.items():
        for vecino in vecinos:
            G.add_edge(nodo, vecino)
    posiciones = {
        "A": (0, 2), "B": (-1, 1), "C": (1, 1),
        "D": (-1.8, 0), "E": (-0.5, 0), "F": (1.8, 0),
        "G": (-1.2, -1), "H": (1, -1), "I": (0, -2)
    }
    plt.figure(figsize=(8, 6))
    nx.draw_networkx(G, posiciones, node_size=900, font_size=11)
    nx.draw_networkx_edges(G, posiciones,
        edgelist=list(zip(camino_bfs, camino_bfs[1:])),
        width=3, style="solid", edge_color="tab:blue")
    nx.draw_networkx_edges(G, posiciones,
        edgelist=list(zip(camino_dfs, camino_dfs[1:])),
        width=2, style="dashed", edge_color="tab:orange")
    plt.title("Grafo de búsqueda: BFS (azul) y DFS (naranja)")
    plt.axis("off"); plt.tight_layout(); plt.show()
