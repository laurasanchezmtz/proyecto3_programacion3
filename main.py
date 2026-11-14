# Título: main.py - Menú de consola de la red de transporte
# Autor: Laura M. Sánchez Martínez
# Fecha: 14/11/2026
# Descripción: Ejecución por consola de Dijkstra (Proyecto 2).
"""Proyecto 2: red de transporte con persistencia en CSV y Dijkstra."""

from __future__ import annotations

from grafo import Dijkstra
from io_handler import capturar_conexiones, cargar_grafo

RUTA_CSV: str = "nodos.csv"


def calcular_ruta() -> None:
    """Carga el grafo desde el CSV y muestra la ruta más corta."""
    grafo = cargar_grafo(RUTA_CSV)
    if not grafo.nodos:
        print("El grafo está vacío.")
        return

    grafo.mostrar()
    print("\nNodos disponibles:", ", ".join(grafo.nodos))
    origen = input("Nodo de inicio: ").strip().upper()
    destino = input("Nodo de destino: ").strip().upper()

    try:
        peso_total, ruta = Dijkstra(grafo).ruta_mas_corta(origen, destino)
    except KeyError as error:
        print(f"Error: {error}")
        return

    if not ruta:
        print(f"No existe ruta entre {origen} y {destino}.")
    else:
        print(f"\nRuta más corta de {origen} a {destino}: "
              f"{' -> '.join(ruta)}")
        print(f"Peso total: {peso_total}")


def menu() -> None:
    """Muestra el menú principal y ejecuta la opción elegida."""
    while True:
        print("\n=== Red de transporte ===")
        print("1. Agregar conexiones")
        print("2. Ver grafo")
        print("3. Calcular ruta más corta (Dijkstra)")
        print("4. Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            capturar_conexiones(RUTA_CSV)
        elif opcion == "2":
            cargar_grafo(RUTA_CSV).mostrar()
        elif opcion == "3":
            calcular_ruta()
        elif opcion == "4":
            print("¡Hasta luego!")
            break
        else:
            print("Opción no válida, elige del 1 al 4.")


if __name__ == "__main__":
    menu()
