import math
import random
import matplotlib.pyplot as plt

# Problema: encontrar una ruta corta en una cuadrícula evitando obstáculos.
# Cada estado es una coordenada (fila, columna).
INICIO = (0, 0)
META = (5, 5)
OBSTACULOS = {(1, 1), (1, 2), (2, 2), (3, 2), (4, 4)}

def vecinos(estado):
    """Regresa movimientos válidos dentro de una cuadrícula de 6x6."""
    r, c = estado
    candidatos = [(r-1,c), (r+1,c), (r,c-1), (r,c+1)]
    return [(nr,nc) for nr,nc in candidatos
            if 0 <= nr < 6 and 0 <= nc < 6
            and (nr,nc) not in OBSTACULOS]

def costo(estado):
    """Distancia Manhattan estimada a la meta."""
    return abs(estado[0] - META[0]) + abs(estado[1] - META[1])

def reconstruir(padres, estado):
    ruta = [estado]
    while estado in padres:
        estado = padres[estado]
        ruta.append(estado)
    return list(reversed(ruta))

def hill_climbing(max_pasos=100):
    actual = INICIO
    ruta = [actual]
    visitados = {actual}
    for _ in range(max_pasos):
        if actual == META:
            return ruta, True
        opciones = [v for v in vecinos(actual) if v not in visitados]
        if not opciones:
            break
        mejor = min(opciones, key=costo)
        # Solo avanza si mejora la heurística; puede atascarse en un óptimo local.
        if costo(mejor) >= costo(actual):
            break
        actual = mejor
        ruta.append(actual)
        visitados.add(actual)
    return ruta, actual == META

def simulated_annealing(iteraciones=500, temperatura_inicial=8.0,
                        enfriamiento=0.985):
    actual = INICIO
    mejor = actual
    ruta = [actual]
    mejor_costo = costo(actual)
    temperatura = temperatura_inicial

    for _ in range(iteraciones):
        if actual == META:
            break
        opciones = vecinos(actual)
        if not opciones:
            break
        siguiente = random.choice(opciones)
        diferencia = costo(siguiente) - costo(actual)

        # Acepta siempre mejoras; a veces acepta empeoramientos según temperatura.
        if diferencia <= 0 or random.random() < math.exp(-diferencia / max(temperatura, 1e-9)):
            actual = siguiente
            ruta.append(actual)
            if costo(actual) < mejor_costo:
                mejor, mejor_costo = actual, costo(actual)
        temperatura *= enfriamiento

    # El algoritmo es estocástico; se informa si llegó a la meta.
    return ruta, actual == META

if __name__ == "__main__":
    random.seed(7)  # Facilita reproducir la ejecución.
    ruta_hc, exito_hc = hill_climbing()
    ruta_sa, exito_sa = simulated_annealing()

    print("HILL CLIMBING")
    print("Ruta:", ruta_hc)
    print("Pasos:", len(ruta_hc)-1, "| ¿Llegó a la meta?:", exito_hc)
    print("\nSIMULATED ANNEALING")
    print("Ruta encontrada durante la búsqueda:", ruta_sa)
    print("Movimientos registrados:", len(ruta_sa)-1,
          "| ¿Terminó en la meta?:", exito_sa)

    # Visualización del mapa y de las rutas.
    fig, ax = plt.subplots(figsize=(6, 6))
    for r, c in OBSTACULOS:
        ax.scatter(c, r, marker="s", s=500, color="black")
    ax.scatter(INICIO[1], INICIO[0], marker="o", s=180, label="Inicio")
    ax.scatter(META[1], META[0], marker="*", s=250, label="Meta")
    if len(ruta_hc) > 1:
        ax.plot([p[1] for p in ruta_hc], [p[0] for p in ruta_hc],
                marker="o", label="Hill Climbing")
    if len(ruta_sa) > 1:
        ax.plot([p[1] for p in ruta_sa], [p[0] for p in ruta_sa],
                marker="x", linestyle="--", label="Simulated Annealing")
    ax.set_xticks(range(6)); ax.set_yticks(range(6))
    ax.set_xlim(-0.5, 5.5); ax.set_ylim(5.5, -0.5)
    ax.grid(True); ax.set_title("Búsqueda local en una cuadrícula")
    ax.set_xlabel("Columna"); ax.set_ylabel("Fila")
    ax.legend(); plt.tight_layout(); plt.show()
