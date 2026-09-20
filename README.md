# CriptoCalc — interfaz neumórfica en Streamlit

Este proyecto usa el **mismo `calculadora.html`** del artefacto original
(HTML + CSS + JS autocontenido, con el diseño neumórfico, animaciones y las
6 categorías/submenús). `app.py` no reconstruye nada con widgets de
Streamlit: simplemente incrusta ese HTML completo dentro de la página con
`st.components.v1.html(...)`, así que se ve y funciona idéntico al artefacto
original, sin importar el tema claro/oscuro de Streamlit Cloud.

## Estructura del proyecto

```
criptocalc-visual/
├── app.py             # Incrusta calculadora.html dentro de Streamlit
├── calculadora.html   # La interfaz neumórfica (HTML+CSS+JS)
└── requirements.txt   # Dependencias
```

> **Importante:** `app.py` y `calculadora.html` deben estar **en la misma
> carpeta**. `app.py` busca `calculadora.html` junto a sí mismo; si no lo
> encuentra, la app muestra un mensaje de error en vez de la calculadora.

## Versión de Python y dependencias

- Python recomendado: **3.11** (funciona igual en 3.10–3.13).
- Única dependencia: `streamlit>=1.50` (ver `requirements.txt`). El HTML
  incrustado carga por su cuenta la librería `crypto-js` desde un CDN
  (`cdnjs.cloudflare.com`) para los hashes MD5/SHA-256/SHA-512, así que no
  hace falta instalar nada de criptografía en Python.

## 1. Ejecutar en local

```bash
# Clona tu repo
git clone https://github.com/<tu-usuario>/<tu-repo>.git
cd <tu-repo>

# Entorno virtual (recomendado)
python3.11 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Instala la única dependencia
pip install -r requirements.txt

# Ejecuta la app
streamlit run app.py
```

Se abrirá en `http://localhost:8501` mostrando la calculadora completa.

## 2. Subir a GitHub

Sube **los tres archivos** (`app.py`, `calculadora.html`, `requirements.txt`)
al repositorio, manteniéndolos en la misma carpeta (puede ser la raíz del
repo o una subcarpeta, mientras los tres queden juntos).

## 3. Desplegar en Streamlit Community Cloud

1. Entra a **https://share.streamlit.io** e inicia sesión con GitHub.
2. Clic en **"New app"** → selecciona el repositorio y la rama.
3. En **"Main file path"** escribe `app.py` (o `carpeta/app.py` si lo
   dejaste dentro de una subcarpeta).
4. Clic en **"Deploy"**. En 1–2 minutos tendrás una URL pública tipo
   `https://<algo>.streamlit.app` con la calculadora funcionando igual que
   el artefacto original.

Cada `git push` posterior a ese repo redespliega la app automáticamente.
