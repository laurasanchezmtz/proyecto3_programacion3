# Proyecto 3: Interfaz Web con Streamlit

Programación III — Unidad 3 · Laura M. Sánchez Martínez

Aplicación web en Streamlit que funciona como capa visual (Frontend) sobre el
grafo y el algoritmo de Dijkstra (Unidad 1) y la persistencia en CSV
(Unidad 2). Permite calcular la ruta más corta, registrar nuevas conexiones
y ver la red actual en una tabla.

## Estructura

```
proyecto_3_streamlit/
├── app.py             # Interfaz visual Streamlit
├── main.py            # Ejecución Dijkstra por consola (Proyecto 2)
├── grafo.py           # Clases Nodo, Grafo y Dijkstra
├── io_handler.py      # Lectura/escritura del CSV
├── nodos.csv          # Base de datos de tramos (Origen, Destino, Peso)
├── requirements.txt   # streamlit, pandas, flake8
└── README.md
```

## Cómo ejecutar

```bash
pip install -r requirements.txt
streamlit run app.py      # interfaz web
python main.py            # versión de consola del Proyecto 2
flake8 .                  # validación de estilo (no debe mostrar nada)
```

## Funcionalidades

- **Lectura única del CSV:** el grafo se guarda en `st.session_state["grafo"]`
  y `nodos.csv` solo se lee si esa clave todavía no existe en la sesión.
- **Registro de conexiones:** cada conexión válida se guarda en `nodos.csv` y
  se agrega directamente al grafo en memoria, sin volver a leer el archivo.
- **Visor de red:** tabla con `pandas` + `st.dataframe`.
- **Ruta óptima:** origen y destino con `st.text_input`; muestra el costo
  total y el recorrido, o avisa si no existe ruta.
- **Layout:** `st.tabs` (3 pestañas), `st.columns`, `st.expander` y
  `st.form`.

## Manejo de excepciones (sin tracebacks en pantalla)

| Situación | Excepción | Aviso |
|---|---|---|
| `nodos.csv` no existe | `FileNotFoundError` | `st.warning` |
| Peso con texto, vacío o negativo | `ValueError` | `st.error` |
| Origen/destino vacío o iguales | `ValueError` | `st.error` |
| Nodo que no existe en el grafo | `KeyError` | `st.error` |
| CSV abierto en otro programa | `PermissionError` | `st.error` |
| Fila corrupta en el CSV | `KeyError` / `ValueError` | `st.warning` |
