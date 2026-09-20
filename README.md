# CriptoCalc — Calculadora de Matemática Modular y Criptografía (Streamlit)

Calculadora con 6 menús: operaciones de matemática modular, criptografía
clásica, criptografía moderna, algoritmos hash, codificación y generación de
hashes con SALT.

## Estructura del proyecto

```
streamlit_app/
├── app.py                  # Interfaz Streamlit (los 6 menús y submenús)
├── crypto_utils.py         # Toda la lógica de cálculo (matemática pura, sin dependencias externas)
├── requirements.txt        # Dependencias del proyecto
├── .streamlit/
│   └── config.toml         # Tema visual (colores claros consistentes en toda la app)
└── README.md
```

> **Importante:** la carpeta `.streamlit/` (con el punto al inicio) debe subirse
> tal cual a GitHub. Sin `config.toml`, Streamlit Cloud usa su tema oscuro por
> defecto y el texto/los widgets pierden contraste con los colores que fija el
> propio `app.py`. Algunos clientes de Git ocultan carpetas que empiezan con
> punto — revisa que quedó incluida en el commit (`git status` debe mostrarla).

## Versión de Python y dependencias

- **Python recomendado: 3.11** (funciona igual en 3.10, 3.12 y 3.13; usa solo
  la librería estándar — `hashlib`, `base64`, `secrets`, `string`,
  `unicodedata` — más Streamlit).
- **Streamlit:** se fija una versión mínima `streamlit>=1.50` en
  `requirements.txt` (la última estable en PyPI a la fecha ronda la serie
  1.5x–1.6x). No hace falta instalar nada más: la lógica criptográfica no usa
  librerías de terceros (ni `pycryptodome` ni `cryptography`), así el
  despliegue es rápido y no depende de compilar nada.

## Ejecutar en local

```bash
# 1. Clona tu repo
git clone https://github.com/<tu-usuario>/<tu-repo>.git
cd <tu-repo>

# 2. Crea un entorno virtual (recomendado)
python3.11 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Instala dependencias
pip install -r requirements.txt

# 4. Ejecuta la app
streamlit run app.py
```

Se abrirá en `http://localhost:8501`.

## Desplegar en Streamlit Community Cloud

1. Sube este proyecto a un repositorio de GitHub (público o privado; con
   privado necesitas conectar tu cuenta de GitHub a Streamlit).
2. Entra a **https://share.streamlit.io** e inicia sesión con GitHub.
3. Clic en **"New app"** → selecciona el repositorio, la rama, y como
   **Main file path** escribe `app.py` (ajusta la ruta si dejas la carpeta
   `streamlit_app/` dentro del repo, ej. `streamlit_app/app.py`).
4. En **"Advanced settings"**, antes de desplegar, puedes elegir la versión
   de Python desde el selector de la interfaz (Streamlit Community Cloud
   **ya no usa un archivo `runtime.txt`** para fijar la versión; ese archivo
   es ignorado). Elige **Python 3.11** si el selector está disponible; si no
   aparece, no te preocupes — el proyecto no usa nada específico de versión
   y corre igual en 3.9–3.13.
5. Clic en **"Deploy"**. En 1–2 minutos tendrás una URL pública tipo
   `https://<algo>.streamlit.app`.
