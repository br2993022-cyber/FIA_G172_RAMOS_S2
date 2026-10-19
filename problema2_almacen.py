
"""
Fundamentos de Inteligencia Artificial - Actividad 2 (Seccion 2)
Problema 2: Navegacion de un robot AGV en un almacen como problema de busqueda.

Modela el espacio de estados como una rejilla m x n con celdas libres,
congestionadas y bloqueadas, y construye el grafo NO dirigido y ponderado.

Alumno:Ramos Lopez Bryan Salvdor |  Grupo: 172  |  Docente: Mtr. Javier Garcia Lara
"""

from __future__ import annotations

from dataclasses import dataclass

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx


# ===========================================================================
# 1. DATOS DEL PROBLEMA
# ===========================================================================
# 0 = pasillo libre (costo 1) | 1 = estanteria (bloqueado) | 2 = congestion (costo 3)
MAPA = [
    [0, 0, 0, 0, 0, 0],
    [0, 1, 1, 0, 1, 0],
    [0, 1, 0, 0, 1, 0],
    [0, 0, 0, 2, 2, 0],
    [0, 1, 1, 2, 0, 0],
    [0, 0, 0, 0, 0, 0],
]
COSTO_CELDA = {0: 1.0, 2: 3.0}                       # costo de ENTRAR a la celda
INICIO = (0, 0)                                      # zona de carga
META   = (5, 5)                                      # zona de empaque
MOVIMIENTOS = ((-1, 0), (1, 0), (0, -1), (0, 1))     # arriba, abajo, izq, der


@dataclass(frozen=True)
class Estado:
    """Estado = celda (fila, col) del almacen."""
    fila: int
    col: int


# ===========================================================================
# 2. GENERADOR DE ESTADOS Y ACCIONES
# ===========================================================================
def generar_estados(mapa) -> set[Estado]:
    """S = celdas transitables. Complejidad O(m*n)."""
    return {Estado(f, c)
            for f, fila in enumerate(mapa)
            for c, v in enumerate(fila) if v != 1}


def acciones(estado: Estado, mapa) -> list[tuple[Estado, float]]:
    """A(s): movimientos validos con costo. Factor de ramificacion b <= 4."""
    nf, nc = len(mapa), len(mapa[0])
    res = []
    for df, dc in MOVIMIENTOS:
        f, c = estado.fila + df, estado.col + dc
        if 0 <= f < nf and 0 <= c < nc and mapa[f][c] != 1:
            res.append((Estado(f, c), COSTO_CELDA.get(mapa[f][c], 1.0)))
    return res


# ===========================================================================
# 3. CONSTRUCCION DEL GRAFO CON NETWORKX
# ===========================================================================
def construir_grafo(mapa) -> nx.Graph:
    """G = (V, E, w), no dirigido y ponderado. Complejidad O(|S| * b)."""
    G = nx.Graph()
    for s in generar_estados(mapa):
        G.add_node(s)
        for t, costo in acciones(s, mapa):
            G.add_edge(s, t, weight=costo)
    return G


# ===========================================================================
# 4. ANALISIS DE COMPLEJIDAD
# ===========================================================================
def analizar_complejidad(G: nx.Graph, mapa) -> dict:
    V, E = G.number_of_nodes(), G.number_of_edges()
    grados = [g for _, g in G.degree()]
    b = max(grados) if grados else 0
    filas, cols = len(mapa), len(mapa[0])
    return {
        "|S|": V,
        "|A| (aristas)": E,
        "b_max": b,
        "celdas_totales": filas * cols,
        "d_max (camino simple)": V - 1,
        "costo_generacion": f"O(|S|*b) = O({V * b})",
        "espacio_almacenamiento": f"O(|S|+|A|) = O({V + E})",
        "busqueda_BFS_peor": f"O(b^d) = O({b}^{V - 1})",
        "busqueda_DFS_espacio": f"O(b*d) = O({b * (V - 1)})",
    }


# ===========================================================================
# 5. VISUALIZACION DEL ESPACIO DE ESTADOS
# ===========================================================================
def dibujar(G: nx.Graph, mapa, archivo: str = "grafo_almacen.png") -> None:
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.imshow(mapa, cmap="Pastel1", origin="upper")
    pos = {n: (n.col, n.fila) for n in G.nodes()}
    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#475569", width=1.2)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_size=90, node_color="#334155")
    ax.plot(INICIO[1], INICIO[0], "o", ms=14, mfc="#86efac", mec="#065f46")
    ax.plot(META[1],   META[0],   "o", ms=14, mfc="#fca5a5", mec="#991b1b")
    ax.set_title("Problema 2 - Espacio de busqueda: almacen (rejilla 6x6)")
    ax.set_xticks(range(len(mapa[0])))
    ax.set_yticks(range(len(mapa)))
    plt.tight_layout()
    plt.savefig(archivo, dpi=200)
    print(f"[ok] Diagrama guardado en {archivo}")


# ===========================================================================
# 6. PROGRAMA PRINCIPAL
# ===========================================================================
def main() -> None:
    S = generar_estados(MAPA)
    G = construir_grafo(MAPA)
    print("=== Problema 2: navegacion de robot en almacen ===")
    print("|S| =", len(S), "| A(INICIO) =", acciones(Estado(*INICIO), MAPA))
    for k, v in analizar_complejidad(G, MAPA).items():
        print(f"  {k}: {v}")
    dibujar(G, MAPA)


if __name__ == "__main__":
    main()