"""
app.py — CriptoCalc (Streamlit, interfaz neumórfica original)

Este archivo NO reconstruye la interfaz con widgets de Streamlit: en su
lugar incrusta el archivo calculadora.html (HTML + CSS + JS autocontenido)
dentro de la página usando st.components.v1.html, así que se ve y se
comporta exactamente igual que el artefacto original — mismos menús,
mismo estilo neumórfico, mismas animaciones.

Requisito: calculadora.html debe estar en la MISMA carpeta que este app.py
(y subirse junto con él al repositorio de GitHub).
"""

from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="CriptoCalc", page_icon="🔐", layout="wide")

# Oculta el padding/menú por defecto de Streamlit para que el HTML
# incrustado use todo el ancho disponible, sin marcos extra.
st.markdown(
    """
    <style>
        .block-container { padding-top: 1rem; padding-bottom: 0rem; max-width: 100%; }
        header[data-testid="stHeader"] { background: transparent; }
        iframe { border: none; }
    </style>
    """,
    unsafe_allow_html=True,
)

html_path = Path(__file__).parent / "calculadora.html"

if not html_path.exists():
    st.error(
        "No se encontró calculadora.html junto a app.py. "
        "Asegúrate de subir ambos archivos al mismo repositorio/carpeta."
    )
else:
    html_content = html_path.read_text(encoding="utf-8")
    # height suficientemente grande para que se vea toda la app sin
    # necesitar doble scroll (el propio HTML ya tiene su scroll interno
    # en la sección de pasos/tablas).
    components.html(html_content, height=1300, scrolling=True)
