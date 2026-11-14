# Título: app.py - Interfaz web de la red de transporte
# Autor: Laura M. Sánchez Martínez
# Fecha: 14/11/2026
# Descripción: Frontend en Streamlit para registrar tramos y calcular rutas.
"""Interfaz web (Frontend) sobre el grafo y la persistencia en CSV."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from grafo import Dijkstra, Grafo
from io_handler import guardar_registro, leer_grafo

RUTA_CSV: str = "nodos.csv"


def inicializar_estado() -> None:
    """Carga el grafo desde el CSV una sola vez por sesión."""
    # Si el grafo ya está en memoria, no se vuelve a leer el disco
    if "grafo" in st.session_state:
        return
    try:
        grafo, avisos = leer_grafo(RUTA_CSV)
    except FileNotFoundError:
        grafo, avisos = Grafo(), []
        st.session_state["aviso_archivo"] = (
            f"No se encontró {RUTA_CSV}. Se creará al registrar "
            "la primera conexión."
        )
    st.session_state["grafo"] = grafo
    st.session_state["avisos_csv"] = avisos


def convertir_peso(texto: str) -> float:
    """Convierte el texto del peso a número o lanza ValueError."""
    texto = texto.strip()
    if not texto:
        raise ValueError("El peso no puede estar vacío.")
    try:
        peso = float(texto)
    except ValueError:
        raise ValueError(
            f"'{texto}' no es un número válido (ej. 4 o 2.5)."
        ) from None
    if peso < 0:
        raise ValueError("El peso no puede ser negativo.")
    return peso


def registrar_conexion(origen: str, destino: str, peso_texto: str) -> None:
    """Valida, guarda en el CSV y actualiza el grafo en memoria."""
    origen = origen.strip().upper()
    destino = destino.strip().upper()
    try:
        if not origen or not destino:
            raise ValueError("El origen y el destino no pueden estar vacíos.")
        if origen == destino:
            raise ValueError("El origen y el destino deben ser distintos.")
        peso = convertir_peso(peso_texto)
        # 1. Persistir en disco  2. Actualizar el grafo de la sesión
        guardar_registro(RUTA_CSV, origen, destino, peso)
        st.session_state["grafo"].agregar_arista(origen, destino, peso)
    except ValueError as error:
        st.error(f"Dato inválido: {error}")
    except PermissionError:
        st.error(f"No hay permiso para escribir en {RUTA_CSV}. "
                 "¿Está abierto en Excel?")
    else:
        # El CSV ya existe, así que el aviso de "no encontrado" sobra
        st.session_state.pop("aviso_archivo", None)
        st.success(f"Conexión {origen} ↔ {destino} (peso {peso:g}) "
                   "guardada.")


def tabla_red(grafo: Grafo) -> pd.DataFrame:
    """Construye un DataFrame con las conexiones del grafo."""
    return pd.DataFrame(grafo.aristas(),
                        columns=["Origen", "Destino", "Peso"])


def vista_calculadora(grafo: Grafo) -> None:
    """Pestaña para calcular la ruta más corta con Dijkstra."""
    st.subheader("Ruta más corta (Dijkstra)")
    if grafo.nodos:
        st.caption("Nodos disponibles: " + ", ".join(sorted(grafo.nodos)))

    col_origen, col_destino = st.columns(2)
    with col_origen:
        origen = st.text_input("Nodo origen", key="calc_origen")
    with col_destino:
        destino = st.text_input("Nodo destino", key="calc_destino")

    if not st.button("Calcular ruta", type="primary"):
        return

    origen = origen.strip().upper()
    destino = destino.strip().upper()
    if not origen or not destino:
        st.warning("Escribe el nodo origen y el nodo destino.")
        return

    try:
        costo, ruta = Dijkstra(grafo).ruta_mas_corta(origen, destino)
    except KeyError as error:
        # error.args[0] trae el mensaje sin las comillas del KeyError
        st.error(error.args[0])
        return

    if not ruta:
        st.warning(f"No existe una ruta posible entre {origen} y {destino}.")
        return

    st.metric("Costo total mínimo", f"{costo:g}")
    st.success("Recorrido: " + " → ".join(ruta))


def vista_registro() -> None:
    """Pestaña para registrar una nueva conexión."""
    st.subheader("Registrar nueva conexión")
    with st.form("form_registro", clear_on_submit=True):
        col_origen, col_destino, col_peso = st.columns(3)
        with col_origen:
            origen = st.text_input("Origen")
        with col_destino:
            destino = st.text_input("Destino")
        with col_peso:
            peso_texto = st.text_input("Peso")
        enviado = st.form_submit_button("Guardar conexión")
    if enviado:
        registrar_conexion(origen, destino, peso_texto)


def vista_red(grafo: Grafo) -> None:
    """Pestaña que muestra la red actual en forma de tabla."""
    st.subheader("Red actual")
    tabla = tabla_red(grafo)
    if tabla.empty:
        st.info("Todavía no hay conexiones registradas.")
        return

    col_nodos, col_aristas = st.columns(2)
    col_nodos.metric("Nodos", len(grafo.nodos))
    col_aristas.metric("Conexiones", len(tabla))
    st.dataframe(tabla, hide_index=True, width="stretch")

    with st.expander("Ver vecinos de cada nodo"):
        for nombre in sorted(grafo.nodos):
            vecinos = grafo.nodos[nombre].vecinos
            texto = ", ".join(
                f"{vecino.nombre} ({peso:g})"
                for vecino, peso in vecinos.items()
            )
            st.write(f"**{nombre}** → {texto}")


def main() -> None:
    """Arma la página principal de la aplicación."""
    st.set_page_config(page_title="Red de transporte", page_icon="🚉")
    inicializar_estado()
    grafo: Grafo = st.session_state["grafo"]

    st.title("🚉 Red de transporte")
    st.caption("Proyecto 3 · Programación III · Streamlit + Dijkstra")

    # Avisos de la carga inicial del CSV
    if "aviso_archivo" in st.session_state:
        st.warning(st.session_state["aviso_archivo"])
    for aviso in st.session_state["avisos_csv"]:
        st.warning(aviso)

    tab_calc, tab_registro, tab_red = st.tabs(
        ["🧭 Calcular ruta", "➕ Registrar conexión", "📋 Ver red"]
    )
    with tab_calc:
        vista_calculadora(grafo)
    with tab_registro:
        vista_registro()
    with tab_red:
        vista_red(grafo)


main()
