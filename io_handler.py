# Título: io_handler.py - Persistencia de la red en CSV
# Autor: Laura M. Sánchez Martínez
# Fecha: 14/11/2026
# Descripción: Entrada segura por consola y lectura/escritura de nodos.csv.
"""Funciones de entrada segura y lectura/escritura del archivo CSV."""

from __future__ import annotations

import csv
import os

from grafo import Grafo

CAMPOS: list[str] = ["Origen", "Destino", "Peso"]


def pedir_nodo(mensaje: str) -> str:
    """Pide un nombre de nodo hasta que el usuario no lo deje vacío."""
    while True:
        nombre = input(mensaje).strip().upper()
        if nombre:
            return nombre
        print("Error: el nombre del nodo no puede estar vacío.")


def pedir_peso(mensaje: str) -> float:
    """Pide un peso numérico no negativo hasta que sea válido."""
    while True:
        texto = input(mensaje).strip()
        try:
            if not texto:
                raise ValueError("el peso no puede estar vacío.")
            peso = float(texto)
            if peso < 0:
                raise ValueError("el peso no puede ser negativo.")
            return peso
        except ValueError as error:
            if "could not convert" in str(error):
                print(f"Error: '{texto}' no es un número (ej. 4 o 2.5).")
            else:
                print(f"Error: {error}")


def guardar_registro(ruta: str, origen: str, destino: str,
                     peso: float) -> None:
    """Escribe una conexión al final del CSV (puede lanzar PermissionError).

    Es la versión sin mensajes: la usa la interfaz de Streamlit para
    decidir ella misma cómo mostrar el error al usuario.
    """
    archivo_nuevo = not os.path.exists(ruta)
    with open(ruta, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=CAMPOS)
        if archivo_nuevo:
            escritor.writeheader()
        escritor.writerow({"Origen": origen, "Destino": destino, "Peso": peso})


def guardar_conexion(ruta: str, origen: str, destino: str,
                     peso: float) -> None:
    """Guarda una conexión e informa el resultado por consola."""
    try:
        guardar_registro(ruta, origen, destino, peso)
        print(f"Conexión {origen}-{destino} ({peso}) guardada en {ruta}.")
    except PermissionError:
        print(f"Error: no hay permiso para escribir en {ruta}.")


def capturar_conexiones(ruta: str) -> None:
    """Captura conexiones por consola y guarda cada una en el CSV."""
    while True:
        origen = pedir_nodo("Nodo origen: ")
        destino = pedir_nodo("Nodo destino: ")
        if origen == destino:
            print("Error: el origen y el destino deben ser distintos.")
            continue
        peso = pedir_peso("Peso: ")
        guardar_conexion(ruta, origen, destino, peso)

        continuar = input("¿Deseas agregar otra conexión? (s/n): ")
        if continuar.strip().lower() not in ("s", "si", "sí"):
            break


def leer_grafo(ruta: str) -> tuple[Grafo, list[str]]:
    """Construye el grafo desde el CSV y devuelve también los avisos.

    Lanza FileNotFoundError si el archivo no existe, para que quien la
    llame (consola o Streamlit) decida cómo avisar al usuario.
    """
    grafo = Grafo()
    avisos: list[str] = []
    with open(ruta, "r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)
        # La fila 1 es el encabezado, los datos empiezan en la 2
        for numero_fila, fila in enumerate(lector, start=2):
            try:
                grafo.agregar_arista(
                    fila["Origen"].strip().upper(),
                    fila["Destino"].strip().upper(),
                    float(fila["Peso"]),
                )
            except KeyError as error:
                avisos.append(f"Falta el encabezado {error}, "
                              f"fila {numero_fila} omitida.")
            except (ValueError, AttributeError):
                avisos.append(f"Datos inválidos en la fila "
                              f"{numero_fila}, se omitió.")
    return grafo, avisos


def cargar_grafo(ruta: str) -> Grafo:
    """Lee el CSV e imprime los avisos por consola (versión de main.py)."""
    try:
        grafo, avisos = leer_grafo(ruta)
    except FileNotFoundError:
        print(f"No se encontró {ruta}. Primero agrega conexiones.")
        return Grafo()
    for aviso in avisos:
        print(f"Aviso: {aviso}")
    return grafo
