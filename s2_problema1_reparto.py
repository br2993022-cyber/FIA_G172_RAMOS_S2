
"""
Fundamentos de Inteligencia Artificial - Actividad 2 (Seccion 2)
Problema 1: Reparto de ultima milla como problema de busqueda.

Modela S, A, f, c y G de una red de reparto urbano y construye el grafo
dirigido y ponderado G=(V,E,w) con NetworkX.

Alumno:Ramos Lopez Bryan Salvdor  |  Grupo: 172  |  Docente: Mtr. Javier Garcia Lara
"""

from __future__ import annotations

from itertools import combinations
from dataclasses import dataclass
from typing import Iterable

import matplotlib
matplotlib.use("Agg")               # render sin ventana (util en Colab/servidor)
import matplotlib.pyplot as plt
import networkx as nx


# ===========================================================================
# 1. DATOS DEL PROBLEMA  (instancia de entrada, parametrizable)
# ===========================================================================
# Red vial: (origen, destino, distancia_km, tiempo_min). Grafo DIRIGIDO:
# existen calles de un solo sentido.
RUTAS: list[tuple[str, str, float, float]] = [
    ("CD", "C1", 4.2,  8),
    ("CD", "C2", 6.8, 13),
    ("C1", "C2", 3.1,  6),
    ("C1", "C3", 5.0,  9),
    ("C2", "C3", 2.4,  5),
    ("C2", "C4", 7.5, 14),
    ("C3", "C4", 4.4,  8),
    ("C3", "CD", 9.0, 16),
    ("C4", "CD", 8.1, 15),
]

ESTADO_INICIAL = "CD"                     # centro de distribucion
ESTADO_META    = "C4"                     # cliente final
CLIENTES       = ("C1", "C2", "C3", "C4")


# ===========================================================================
# 2. DEFINICION FORMAL DEL PROBLEMA   P = (S, s0, A, f, c, G)
# ===========================================================================
@dataclass(frozen=True)
class ProblemaBusqueda:
    """Representacion formal de un problema de busqueda (Bohm, 2021)."""
    inicial: str
    meta: str
    acciones: dict[str, list[tuple[str, float]]]

    def es_meta(self, estado: str) -> bool:
        """Prueba de meta: G = {meta}."""
        return estado == self.meta

    def sucesores(self, estado: str) -> list[tuple[str, float]]:
        """A(s) junto con f(s,a) y c(s,a): lista de (sucesor, costo)."""
        return self.acciones.get(estado, [])


# ===========================================================================
# 3. GENERADOR DE ESTADOS
# ===========================================================================
def generar_estados(rutas: Iterable[tuple[str, str, float, float]]
                    ) -> tuple[set[str], dict[str, list[tuple[str, float]]]]:
    """Genera S y A a partir de la instancia.

    S  = nodos alcanzables (posiciones del vehiculo).
    A(s) = aristas salientes de s etiquetadas con su costo.
    Complejidad: O(|E|).
    """
    estados: set[str] = set()
    acciones: dict[str, list[tuple[str, float]]] = {}
    for origen, destino, km, _min in rutas:
        estados.add(origen)
        estados.add(destino)
        acciones.setdefault(origen, []).append((destino, km))
    return estados, acciones


def estados_aumentados(rutas, clientes) -> set[tuple[str, frozenset]]:
    """Modelo aumentado tipo TSP: estado = (nodo, clientes ya visitados).

    |S'| = |V| * 2^k  con k = numero de clientes -> crecimiento exponencial.
    """
    nodos = {o for o, _, _, _ in rutas} | {d for _, d, _, _ in rutas}
    visitados = [frozenset(c) for i in range(len(clientes) + 1)
                 for c in combinations(clientes, i)]
    return {(n, v) for n in nodos for v in visitados}


# ===========================================================================
# 4. CONSTRUCCION DEL GRAFO CON NETWORKX
# ===========================================================================
def construir_grafo(rutas) -> nx.DiGraph:
    """G = (V, E, w). Grafo dirigido y ponderado."""
    G = nx.DiGraph()
    for origen, destino, km, minutos in rutas:
        G.add_edge(origen, destino, weight=km, tiempo=minutos)
    return G


# ===========================================================================
# 5. ANALISIS DE COMPLEJIDAD
# ===========================================================================
def analizar_complejidad(G: nx.DiGraph) -> dict:
    """Metricas estructurales y cotas asintoticas del espacio de busqueda."""
    V, E = G.number_of_nodes(), G.number_of_edges()
    grados = [g for _, g in G.out_degree()]
    b = max(grados) if grados else 0
    return {
        "|S|": V,
        "|A|": E,
        "b_max": b,
        "densidad": round(nx.density(G), 3),
        "conexo_debil": nx.is_weakly_connected(G),
        "costo_generacion": f"O(|S|+|A|) = O({V + E})",
        "espacio_almacenamiento": f"O(|S|+|A|) = O({V + E})",
        "peor_caso_busqueda": f"O(b^d) = O({b}^d)",
    }


# ===========================================================================
# 6. VISUALIZACION DEL ESPACIO DE ESTADOS
# ===========================================================================
def dibujar(G: nx.DiGraph, archivo: str = "grafo_reparto.png") -> None:
    pos = nx.spring_layout(G, seed=7)
    etiquetas = nx.get_edge_attributes(G, "weight")
    plt.figure(figsize=(8, 6))
    nx.draw_networkx_nodes(G, pos, node_size=1800,
                           node_color="#c7d2fe", edgecolors="#4338ca")
    nx.draw_networkx_labels(G, pos, font_size=12, font_weight="bold")
    nx.draw_networkx_edges(G, pos, arrows=True, arrowsize=20, width=1.4)
    nx.draw_networkx_edge_labels(
        G, pos, edge_labels={k: f"{v} km" for k, v in etiquetas.items()},
        font_size=9, font_color="#b91c1c")
    plt.title("Problema 1 - Espacio de busqueda: red de reparto")
    plt.axis("off")
    plt.tight_layout()
    plt.savefig(archivo, dpi=200)
    print(f"[ok] Diagrama guardado en {archivo}")


# ===========================================================================
# 7. PROGRAMA PRINCIPAL
# ===========================================================================
def main() -> None:
    S, A = generar_estados(RUTAS)
    problema = ProblemaBusqueda(ESTADO_INICIAL, ESTADO_META, A)
    G = construir_grafo(RUTAS)

    print("=== Problema 1: reparto de ultima milla ===")
    print("S =", sorted(S))
    print("A(CD) =", problema.sucesores("CD"))
    print("s0 es meta:", problema.es_meta("CD"),
          "| C4 es meta:", problema.es_meta("C4"))
    print("|S'| modelo aumentado (TSP):", len(estados_aumentados(RUTAS, CLIENTES)))
    for k, v in analizar_complejidad(G).items():
        print(f"  {k}: {v}")
    dibujar(G)


if __name__ == "__main__":
    main()