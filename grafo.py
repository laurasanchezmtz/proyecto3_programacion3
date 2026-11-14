# Título: grafo.py - Clases Nodo, Grafo y Dijkstra
# Autor: Laura M. Sánchez Martínez
# Fecha: 14/11/2026
# Descripción: Lógica del grafo ponderado y cálculo de rutas con Dijkstra.
"""Clases POO del grafo: Nodo, Grafo y Dijkstra (Unidad 1)."""

from __future__ import annotations

import heapq


class Nodo:
    """Representa una estación de la red de transporte y sus vecinos."""

    def __init__(self, nombre: str) -> None:
        """Crea un nodo con su nombre y sin conexiones."""
        self.nombre: str = nombre
        self.vecinos: dict[Nodo, float] = {}

    def agregar_vecino(self, vecino: Nodo, peso: float) -> None:
        """Registra una conexión hacia otro nodo con su peso."""
        self.vecinos[vecino] = peso

    def __lt__(self, otro: Nodo) -> bool:
        """Compara nodos por nombre para desempatar en la cola de prioridad."""
        return self.nombre < otro.nombre

    def __repr__(self) -> str:
        """Devuelve el nombre del nodo al imprimirlo."""
        return self.nombre


class Grafo:
    """Grafo ponderado no dirigido representado con lista de adyacencia."""

    def __init__(self) -> None:
        """Crea un grafo vacío."""
        self.nodos: dict[str, Nodo] = {}

    def agregar_nodo(self, nombre: str) -> Nodo:
        """Agrega un nodo si no existe y lo devuelve."""
        if nombre not in self.nodos:
            self.nodos[nombre] = Nodo(nombre)
        return self.nodos[nombre]

    def agregar_arista(self, origen: str, destino: str, peso: float) -> None:
        """Conecta dos nodos en ambos sentidos con el peso indicado."""
        if peso < 0:
            raise ValueError("Dijkstra requiere pesos no negativos.")
        nodo_origen = self.agregar_nodo(origen)
        nodo_destino = self.agregar_nodo(destino)
        nodo_origen.agregar_vecino(nodo_destino, peso)
        nodo_destino.agregar_vecino(nodo_origen, peso)

    def obtener_nodo(self, nombre: str) -> Nodo:
        """Devuelve el nodo con ese nombre o lanza KeyError si no existe."""
        if nombre not in self.nodos:
            raise KeyError(f"El nodo '{nombre}' no existe en el grafo.")
        return self.nodos[nombre]

    def aristas(self) -> list[tuple[str, str, float]]:
        """Devuelve cada conexión una sola vez como (origen, destino, peso)."""
        vistas: set[frozenset[str]] = set()
        resultado: list[tuple[str, str, float]] = []
        for nodo in self.nodos.values():
            for vecino, peso in nodo.vecinos.items():
                # Como el grafo es no dirigido, A-B y B-A son la misma arista
                par = frozenset((nodo.nombre, vecino.nombre))
                if par not in vistas:
                    vistas.add(par)
                    resultado.append((nodo.nombre, vecino.nombre, peso))
        return resultado

    def mostrar(self) -> None:
        """Imprime cada nodo con sus vecinos y pesos."""
        print("Grafo (nodo -> vecino[peso]):")
        for nodo in self.nodos.values():
            conexiones = ", ".join(
                f"{vecino.nombre}[{peso}]"
                for vecino, peso in nodo.vecinos.items()
            )
            print(f"  {nodo.nombre} -> {conexiones}")


class Dijkstra:
    """Calcula la ruta más corta entre dos nodos de un grafo."""

    def __init__(self, grafo: Grafo) -> None:
        """Guarda el grafo sobre el que se ejecutará el algoritmo."""
        self.grafo: Grafo = grafo

    def ruta_mas_corta(
        self, inicio: str, destino: str
    ) -> tuple[float, list[str]]:
        """Devuelve el peso total y la ruta del nodo inicio al destino."""
        nodo_inicio = self.grafo.obtener_nodo(inicio)
        nodo_destino = self.grafo.obtener_nodo(destino)

        # 1. Inicializar: el origen en 0 y los demás en infinito
        distancias: dict[Nodo, float] = {
            nodo: float("inf") for nodo in self.grafo.nodos.values()
        }
        anteriores: dict[Nodo, Nodo | None] = {
            nodo: None for nodo in self.grafo.nodos.values()
        }
        visitados: set[Nodo] = set()
        distancias[nodo_inicio] = 0
        cola: list[tuple[float, Nodo]] = [(0, nodo_inicio)]

        while cola:
            # 2. Seleccionar el nodo no visitado con menor distancia
            distancia_actual, actual = heapq.heappop(cola)
            if actual in visitados:
                continue
            # 3. Marcar como visitado
            visitados.add(actual)

            # 4. Relajar: actualizar vecinos si el camino es más corto
            for vecino, peso in actual.vecinos.items():
                nueva_distancia = distancia_actual + peso
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    anteriores[vecino] = actual
                    heapq.heappush(cola, (nueva_distancia, vecino))

        if distancias[nodo_destino] == float("inf"):
            return float("inf"), []

        # Reconstruir el camino desde el destino hasta el origen
        ruta: list[str] = []
        paso: Nodo | None = nodo_destino
        while paso is not None:
            ruta.append(paso.nombre)
            paso = anteriores[paso]
        ruta.reverse()
        return distancias[nodo_destino], ruta
