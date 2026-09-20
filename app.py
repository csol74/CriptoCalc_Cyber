```python
"""
app.py — CriptoCalc
Aplicación de matemática modular, criptografía clásica y moderna,
algoritmos hash, codificación y uso de SALT.

Diseño:
    Streamlit 1.50+

Ejecutar:
    streamlit run app.py
"""

import streamlit as st
import crypto_utils as cu


# ============================================================================
# CONFIGURACIÓN
# ============================================================================

st.set_page_config(
    page_title="CriptoCalc",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================================
# ESTILOS
# ============================================================================

st.markdown(
    """
    <style>

    /* ================================================================
       BASE
       ================================================================ */

    .stApp {
        background: #eef1f6;
    }

    .main .block-container {
        max-width: 1350px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }


    /* ================================================================
       SIDEBAR
       ================================================================ */

    section[data-testid="stSidebar"] {
        background: #e3e7ee;
        border-right: 1px solid #d4dae4;
    }

    section[data-testid="stSidebar"] > div {
        padding: 1.5rem 1rem 1rem 1rem;
    }

    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 5px 22px 5px;
    }

    .brand-icon {
        width: 44px;
        height: 44px;
        border-radius: 13px;
        background: #e8734a;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 21px;
        box-shadow: 4px 4px 9px #c5cbd5;
    }

    .brand-title {
        font-size: 1.15rem;
        font-weight: 800;
        color: #263241;
        line-height: 1.1;
    }

    .brand-subtitle {
        font-size: 0.7rem;
        color: #788394;
        margin-top: 4px;
    }

    section[data-testid="stSidebar"] .stRadio > label {
        font-size: 0.73rem;
        font-weight: 800;
        color: #7a8493;
        letter-spacing: 0.7px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] {
        gap: 5px;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        border-radius: 11px;
        padding: 9px 10px;
        transition: all 0.15s ease;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.65);
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label[data-checked="true"] {
        background: #ffffff;
        box-shadow:
            3px 3px 8px #cbd1dc,
            -3px -3px 8px #ffffff;
    }

    .sidebar-footer {
        position: fixed;
        bottom: 18px;
        color: #8a94a3;
        font-size: 0.68rem;
        line-height: 1.4;
    }


    /* ================================================================
       HERO
       ================================================================ */

    .hero {
        background: linear-gradient(
            135deg,
            #ffffff 0%,
            #f7f8fa 100%
        );

        border: 1px solid #dce1e8;
        border-radius: 22px;
        padding: 27px 32px;
        margin-bottom: 20px;

        box-shadow:
            8px 8px 18px #d2d7e0,
            -8px -8px 18px #ffffff;
    }

    .hero-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 20px;
    }

    .hero-title {
        font-size: 2rem;
        font-weight: 850;
        color: #263241;
        margin: 0;
        letter-spacing: -0.8px;
    }

    .hero-title span {
        color: #e8734a;
    }

    .hero-description {
        margin-top: 7px;
        color: #6d7889;
        font-size: 0.91rem;
        line-height: 1.5;
    }

    .status {
        background: #fff1eb;
        color: #d45d37;
        border-radius: 20px;
        padding: 7px 13px;
        font-size: 0.72rem;
        font-weight: 750;
        white-space: nowrap;
    }


    /* ================================================================
       MODULE HEADER
       ================================================================ */

    .module-header {
        background: #ffffff;
        border: 1px solid #dde2e9;
        border-radius: 17px;
        padding: 17px 21px;
        margin-bottom: 18px;

        box-shadow:
            5px 5px 12px #d4d9e2,
            -5px -5px 12px #ffffff;
    }

    .module-title {
        font-size: 1.22rem;
        font-weight: 800;
        color: #263241;
        margin-bottom: 4px;
    }

    .module-description {
        color: #778293;
        font-size: 0.83rem;
    }

    .module-count {
        display: inline-block;
        margin-top: 9px;
        background: #f1f3f7;
        color: #697486;
        border-radius: 20px;
        padding: 4px 9px;
        font-size: 0.67rem;
        font-weight: 700;
    }


    /* ================================================================
       CARDS
       ================================================================ */

    .card {
        background: #ffffff;
        border: 1px solid #dde2e9;
        border-radius: 17px;
        padding: 20px;
        box-shadow:
            5px 5px 12px #d4d9e2,
            -5px -5px 12px #ffffff;
    }

    .card-title {
        font-size: 0.78rem;
        color: #e8734a;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.7px;
        margin-bottom: 13px;
    }


    /* ================================================================
       RESULTADOS
       ================================================================ */

    .result-label {
        font-size: 0.76rem;
        color: #e8734a;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        margin-top: 4px;
        margin-bottom: 8px;
    }

    .result-box {
        background: #f7f8fa;
        color: #263241;

        border: 1px solid #d9dee6;
        border-left: 5px solid #e8734a;

        border-radius: 14px;
        padding: 17px 19px;

        box-shadow:
            inset 3px 3px 7px #d8dde5,
            inset -3px -3px 7px #ffffff;

        font-family:
            ui-monospace,
            "SF Mono",
            Menlo,
            Consolas,
            monospace;

        font-size: 13.5px;
        line-height: 1.65;
        white-space: pre-wrap;
        overflow-wrap: anywhere;
    }


    /* ================================================================
       INPUTS
       ================================================================ */

    div[data-baseweb="input"] {
        border-radius: 10px !important;
    }

    div[data-baseweb="select"] > div {
        border-radius: 10px !important;
    }

    div[data-testid="stTextInput"] input,
    div[data-testid="stNumberInput"] input {
        background: #f8f9fb;
    }

    div[data-testid="stTextInput"] label,
    div[data-testid="stNumberInput"] label,
    div[data-testid="stSelectbox"] label,
    div[data-testid="stRadio"] label {
        color: #465264;
        font-weight: 650;
    }


    /* ================================================================
       BOTONES
       ================================================================ */

    div.stButton > button {
        border-radius: 11px;
        min-height: 42px;
        font-weight: 750;
        border: 0;

        box-shadow:
            4px 4px 10px #cbd1db,
            -4px -4px 10px #ffffff;

        transition: all 0.15s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-1px);
    }

    div.stButton > button:active {
        transform: translateY(1px);
        box-shadow:
            inset 3px 3px 7px #cbd1db,
            inset -3px -3px 7px #ffffff;
    }

    div.stButton > button[kind="primary"] {
        background: #e8734a;
        color: #ffffff;
    }

    div.stButton > button[kind="primary"]:hover {
        background: #dc6841;
    }


    /* ================================================================
       EXPANDERS
       ================================================================ */

    div[data-testid="stExpander"] {
        border: 1px solid #dce1e8;
        border-radius: 12px;
        background: #f7f8fa;
        margin-top: 12px;
    }


    /* ================================================================
       TABS
       ================================================================ */

    button[data-baseweb="tab"] {
        font-weight: 650;
    }


    /* ================================================================
       FOOTER
       ================================================================ */

    .app-footer {
        text-align: center;
        color: #8b95a4;
        font-size: 0.68rem;
        margin-top: 38px;
        padding-top: 15px;
        border-top: 1px solid #d9dee6;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================================
# MARCA
# ============================================================================

st.sidebar.markdown(
    """
    <div class="brand">
        <div class="brand-icon">🔐</div>
        <div>
            <div class="brand-title">CriptoCalc</div>
            <div class="brand-subtitle">Herramientas criptográficas</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================================
# MENÚ
# ============================================================================

MENU_1 = "1. Operaciones matemáticas modulares"
MENU_2 = "2. Criptografía Clásica"
MENU_3 = "3. Criptografía Moderna"
MENU_4 = "4. Algoritmos Hash"
MENU_5 = "5. Codificación"
MENU_6 = "6. Uso de SALT"

menu = st.sidebar.radio(
    "Módulos",
    [
        MENU_1,
        MENU_2,
        MENU_3,
        MENU_4,
        MENU_5,
        MENU_6,
    ],
)


st.sidebar.markdown("---")

st.sidebar.markdown(
    """
    <div class="sidebar-footer">
        <strong>UNAB</strong><br>
        Proyecto de Grado I — SIEM-IA
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================================
# ENCABEZADO
# ============================================================================

st.markdown(
    """
    <div class="hero">
        <div class="hero-top">
            <div>
                <div class="hero-title">
                    Cripto<span>Calc</span>
                </div>

                <div class="hero-description">
                    Plataforma interactiva para matemática modular,
                    criptografía, funciones hash y codificación.
                </div>
            </div>

            <div class="status">
                ● Sistema listo
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================================
# INFORMACIÓN DE MÓDULOS
# ============================================================================

MODULE_INFO = {
    MENU_1: (
        "Matemática modular",
        "Operaciones fundamentales utilizadas como base para diferentes algoritmos criptográficos.",
        "6 herramientas",
    ),
    MENU_2: (
        "Criptografía clásica",
        "Métodos históricos de sustitución, desplazamiento y transposición.",
        "7 algoritmos",
    ),
    MENU_3: (
        "Criptografía moderna",
        "Demostraciones interactivas de algoritmos y operaciones criptográficas modernas.",
        "3 herramientas",
    ),
    MENU_4: (
        "Algoritmos Hash",
        "Generación de valores hash mediante diferentes funciones de resumen.",
        "3 algoritmos",
    ),
    MENU_5: (
        "Codificación",
        "Conversión entre texto y diferentes representaciones de datos.",
        "4 formatos",
    ),
    MENU_6: (
        "Uso de SALT",
        "Demostración del uso de valores SALT en la generación de hashes.",
        "3 algoritmos",
    ),
}

module_title, module_description, module_count = MODULE_INFO[menu]

st.markdown(
    f"""
    <div class="module-header">
        <div class="module-title">{module_title}</div>
        <div class="module-description">{module_description}</div>
        <div class="module-count">{module_count}</div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================================
# FUNCIÓN DE RESULTADO
# ============================================================================

def show_result(main_text: str, steps_text: str = ""):

    st.markdown(
        '<div class="result-label">Resultado</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        f'<div class="result-box">{main_text}</div>',
        unsafe_allow_html=True,
    )

    if steps_text:
        with st.expander("Ver pasos / tabla de cálculo"):
            st.code(steps_text, language="text")


# ============================================================================
# 1. MATEMÁTICA MODULAR
# ============================================================================

if menu == MENU_1:

    sub = st.selectbox(
        "Operación",
        [
            "1.1 Calcular a mod n = b",
            "1.2 Calcular inverso aditivo",
            "1.3 Calcular inverso de XOR",
            "1.4 MCD e indicar si existe inverso multiplicativo",
            "1.5 Inverso multiplicativo (método tradicional)",
            "1.6 Inverso multiplicativo (Algoritmo Extendido de Euclides)",
        ],
    )

    st.markdown(
        '<div class="card-title">Parámetros de cálculo</div>',
        unsafe_allow_html=True,
    )

    if sub.startswith("1.1"):

        col1, col2 = st.columns(2)

        with col1:
            a = st.number_input("a", value=17, step=1)

        with col2:
            n = st.number_input(
                "n",
                value=5,
                step=1,
                min_value=1,
            )

        if st.button("Calcular", type="primary", use_container_width=True):

            b = cu.mod(int(a), int(n))

            show_result(
                f"{int(a)} mod {int(n)} = {b}",
                f"b = a − n·⌊a/n⌋ = {int(a)} − "
                f"{int(n)}·{int(a)//int(n)} = {b}",
            )

    elif sub.startswith("1.2"):

        col1, col2 = st.columns(2)

        with col1:
            a = st.number_input("a", value=7, step=1)

        with col2:
            n = st.number_input(
                "n (módulo)",
                value=12,
                step=1,
                min_value=1,
            )

        if st.button("Calcular", type="primary", use_container_width=True):

            inv = cu.mod(-int(a), int(n))

            show_result(
                f"Inverso aditivo de {int(a)} mod {int(n)} = {inv}",
                f"({int(a)} + {inv}) mod {int(n)} = "
                f"{cu.mod(int(a) + inv, int(n))} ✔",
            )

    elif sub.startswith("1.3"):

        col1, col2 = st.columns(2)

        with col1:
            a = st.number_input(
                "Valor a (decimal)",
                value=12,
                step=1,
                min_value=0,
            )

        with col2:
            c = st.number_input(
                "Resultado c = a ⊕ b (decimal)",
                value=9,
                step=1,
                min_value=0,
            )

        if st.button("Calcular", type="primary", use_container_width=True):

            b = int(a) ^ int(c)

            show_result(
                f"b = a ⊕ c = {int(a)} ⊕ {int(c)} = {b}",
                f"Binario: {bin(int(a))} ⊕ {bin(int(c))} = {bin(b)}\n"
                f"Comprobación: {int(a)} ⊕ {b} = {int(a) ^ b} "
                f"(debe ser {int(c)})",
            )

    elif sub.startswith("1.4"):

        col1, col2 = st.columns(2)

        with col1:
            a = st.number_input("a", value=8, step=1)

        with col2:
            n = st.number_input(
                "n",
                value=17,
                step=1,
                min_value=1,
            )

        if st.button("Calcular", type="primary", use_container_width=True):

            g, steps = cu.gcd_steps(int(a), int(n))

            existe = g == 1

            show_result(
                f"MCD({int(a)}, {int(n)}) = {g}\n"
                + (
                    "✔ Existe inverso multiplicativo (gcd = 1)"
                    if existe
                    else "✘ No existe inverso multiplicativo (gcd ≠ 1)"
                ),
                "\n".join(steps),
            )

    elif sub.startswith("1.5"):

        col1, col2 = st.columns(2)

        with col1:
            a = st.number_input("a", value=3, step=1)

        with col2:
            n = st.number_input(
                "n (módulo)",
                value=11,
                step=1,
                min_value=2,
            )

        if st.button("Calcular", type="primary", use_container_width=True):

            found, rows = cu.multiplicative_inverse_traditional(
                int(a),
                int(n),
            )

            table = (
                "x | a·x mod n\n"
                + "\n".join(
                    f"{x} | {r}"
                    for x, r in rows
                )
            )

            if found is not None:

                show_result(
                    f"Inverso multiplicativo de "
                    f"{int(a)} mod {int(n)} = {found}",
                    table,
                )

            else:

                show_result(
                    f"No existe inverso multiplicativo de "
                    f"{int(a)} mod {int(n)} (gcd ≠ 1)",
                    table,
                )

    elif sub.startswith("1.6"):

        col1, col2 = st.columns(2)

        with col1:
            a = st.number_input("a", value=3, step=1)

        with col2:
            n = st.number_input(
                "n (módulo)",
                value=11,
                step=1,
                min_value=2,
            )

        if st.button("Calcular", type="primary", use_container_width=True):

            g, x, _y, rows = cu.extended_euclid(
                int(a),
                int(n),
            )

            table = (
                "Ronda | q | r_ant | r_act | resto | s | t\n"
            )

            for row in rows:

                table += (
                    f"{row['ronda']} | "
                    f"{row['q']} | "
                    f"{row['r_ant']} | "
                    f"{row['r_act']} | "
                    f"{row['resto']} | "
                    f"{row['s']} | "
                    f"{row['t']}\n"
                )

            if g == 1:

                inv = cu.mod(x, int(n))

                show_result(
                    f"MCD({int(a)},{int(n)}) = {g}\n"
                    f"Inverso multiplicativo de "
                    f"{int(a)} mod {int(n)} = {inv}\n"
                    f"(rondas: {len(rows)})",
                    table,
                )

            else:

                show_result(
                    f"MCD({int(a)},{int(n)}) = {g}\n"
                    "No existe inverso multiplicativo (gcd ≠ 1)",
                    table,
                )


# ============================================================================
# 2. CRIPTOGRAFÍA CLÁSICA
# ============================================================================

elif menu == MENU_2:

    sub = st.selectbox(
        "Algoritmo",
        [
            "2.1 Cifrado módulo 27",
            "2.2 Cifrado César",
            "2.3 Cifrado Vernam",
            "2.4 Cifrado ATBASH",
            "2.5 Transposición columnar simple",
            "2.6 Cifrado afín",
            "2.7 Sustitución simple",
        ],
    )

    if sub.startswith("2.1"):

        text = st.text_input(
            "Texto",
            "HOLA MUNDO",
        )

        key = st.number_input(
            "Clave (0-26)",
            value=3,
            step=1,
            min_value=0,
            max_value=26,
        )

        mode = st.radio(
            "Modo",
            ["Cifrar", "Descifrar"],
            horizontal=True,
        )

        if st.button(
            "Calcular",
            type="primary",
            use_container_width=True,
        ):

            clean, out = cu.shift_cipher(
                text,
                int(key),
                cu.A27,
                decrypt=(mode == "Descifrar"),
            )

            show_result(
                f"Texto limpio: {clean}\nResultado: {out}",
                f"Alfabeto (27): {cu.A27}\n"
                f"Desplazamiento: k={int(key)}",
            )

    elif sub.startswith("2.2"):

        text = st.text_input(
            "Texto",
            "HOLA MUNDO",
            key="cesar_text",
        )

        key = st.number_input(
            "Clave (0-25)",
            value=3,
            step=1,
            min_value=0,
            max_value=25,
            key="cesar_key",
        )

        mode = st.radio(
            "Modo",
            ["Cifrar", "Descifrar"],
            horizontal=True,
            key="cesar_mode",
        )

        if st.button(
            "Calcular",
            key="cesar_btn",
            type="primary",
            use_container_width=True,
        ):

            clean, out = cu.shift_cipher(
                text,
                int(key),
                cu.A26,
                decrypt=(mode == "Descifrar"),
            )

            show_result(
                f"Texto limpio: {clean}\nResultado: {out}",
                f"Alfabeto (26): {cu.A26}\n"
                f"Desplazamiento: k={int(key)}",
            )

    elif sub.startswith("2.3"):

        col1, col2 = st.columns(2)

        with col1:
            text = st.text_input(
                "Texto (o hex si descifras)",
                "HOLA",
            )

        with col2:
            key = st.text_input(
                "Clave (texto)",
                "CLAVE",
            )

        mode = st.radio(
            "Modo",
            ["Cifrar", "Descifrar"],
            horizontal=True,
            key="vernam_mode",
        )

        if st.button(
            "Calcular",
            key="vernam_btn",
            type="primary",
            use_container_width=True,
        ):

            if not key:

                st.warning("La clave no puede estar vacía.")

            else:

                out = cu.vernam(
                    text,
                    key,
                    decrypt=(mode == "Descifrar"),
                )

                show_result(
                    f"Resultado: {out}",
                    "Clave repetida byte a byte con XOR (⊕). "
                    "Resultado en hexadecimal.",
                )

    elif sub.startswith("2.4"):

        text = st.text_input(
            "Texto",
            "HOLA MUNDO",
            key="atbash_text",
        )

        if st.button(
            "Calcular",
            key="atbash_btn",
            type="primary",
            use_container_width=True,
        ):

            clean, out = cu.atbash(text)

            show_result(
                f"Texto limpio: {clean}\nResultado: {out}",
                "ATBASH: letra_i ↔ letra_(25−i)",
            )

    elif sub.startswith("2.5"):

        col1, col2 = st.columns(2)

        with col1:

            text = st.text_input(
                "Texto",
                "ATACAR AL AMANECER",
            )

        with col2:

            key = st.text_input(
                "Clave (palabra o dígitos)",
                "CLAVE",
            )

        mode = st.radio(
            "Modo",
            ["Cifrar", "Descifrar"],
            horizontal=True,
            key="col_mode",
        )

        if st.button(
            "Calcular",
            key="col_btn",
            type="primary",
            use_container_width=True,
        ):

            if mode == "Cifrar":

                padded, out, order, rows, cols = cu.columnar_encrypt(
                    text,
                    key,
                )

                show_result(
                    f"Texto (relleno con X): {padded}\n"
                    f"Resultado: {out}",
                    f"Columnas: {cols} · Filas: {rows}\n"
                    f"Orden de lectura: {order}",
                )

            else:

                cipher_clean = cu.only_letters(
                    text,
                    cu.A26,
                )

                out, order, rows, cols = cu.columnar_decrypt(
                    cipher_clean,
                    key,
                )

                show_result(
                    f"Resultado: {out}",
                    f"Columnas: {cols} · Filas: {rows}\n"
                    f"Orden de lectura: {order}",
                )

    elif sub.startswith("2.6"):

        text = st.text_input(
            "Texto",
            "HOLA MUNDO",
            key="afin_text",
        )

        col1, col2 = st.columns(2)

        with col1:

            a = st.number_input(
                "a",
                value=5,
                step=1,
                key="afin_a",
            )

        with col2:

            b = st.number_input(
                "b",
                value=8,
                step=1,
                key="afin_b",
            )

        mode = st.radio(
            "Modo",
            ["Cifrar", "Descifrar"],
            horizontal=True,
            key="afin_mode",
        )

        if st.button(
            "Calcular",
            key="afin_btn",
            type="primary",
            use_container_width=True,
        ):

            try:

                clean, out = cu.affine(
                    text,
                    int(a),
                    int(b),
                    cu.A26,
                    decrypt=(mode == "Descifrar"),
                )

                formula = (
                    "D(y) = a⁻¹·(y − b) mod 26"
                    if mode == "Descifrar"
                    else f"E(x) = ({int(a)}·x + {int(b)}) mod 26"
                )

                show_result(
                    f"Texto limpio: {clean}\nResultado: {out}",
                    formula,
                )

            except ValueError as e:

                st.error(str(e))

    elif sub.startswith("2.7"):

        text = st.text_input(
            "Texto",
            "HOLA MUNDO",
            key="sub_text",
        )

        key = st.text_input(
            "Clave (palabra)",
            "CRIPTO",
        )

        mode = st.radio(
            "Modo",
            ["Cifrar", "Descifrar"],
            horizontal=True,
            key="sub_mode",
        )

        if st.button(
            "Calcular",
            key="sub_btn",
            type="primary",
            use_container_width=True,
        ):

            clean, out, cipher_alpha = cu.substitution(
                text,
                key,
                decrypt=(mode == "Descifrar"),
            )

            show_result(
                f"Texto limpio: {clean}\nResultado: {out}",
                f"Alfabeto claro:   {cu.A26}\n"
                f"Alfabeto cifrado: {cipher_alpha}",
            )


# ============================================================================
# 3. CRIPTOGRAFÍA MODERNA
# ============================================================================

elif menu == MENU_3:

    sub = st.selectbox(
        "Algoritmo",
        [
            "3.1 Diffie-Hellman",
            "3.2 RSA",
            "3.3 Algoritmo de exponenciación rápida",
        ],
    )

    if sub.startswith("3.1"):

        col1, col2 = st.columns(2)

        with col1:

            p = st.number_input(
                "p (primo)",
                value=23,
                step=1,
                min_value=2,
            )

            g = st.number_input(
                "g (generador)",
                value=5,
                step=1,
                min_value=1,
            )

        with col2:

            a = st.number_input(
                "a (privada de Alice)",
                value=6,
                step=1,
                min_value=1,
            )

            b = st.number_input(
                "b (privada de Bob)",
                value=15,
                step=1,
                min_value=1,
            )

        if st.button(
            "Calcular",
            type="primary",
            use_container_width=True,
        ):

            A, B, sA, sB = cu.diffie_hellman(
                int(p),
                int(g),
                int(a),
                int(b),
            )

            ok = (
                "✔ Los secretos coinciden"
                if sA == sB
                else "✘ No coinciden (revisa los datos)"
            )

            show_result(
                f"Clave pública Alice A = g^a mod p = {A}\n"
                f"Clave pública Bob   B = g^b mod p = {B}\n"
                f"Secreto (Alice) = B^a mod p = {sA}\n"
                f"Secreto (Bob)   = A^b mod p = {sB}\n"
                f"{ok}",
                f"p={int(p)}, g={int(g)}, "
                f"a={int(a)}, b={int(b)}",
            )

    elif sub.startswith("3.2"):

        col1, col2 = st.columns(2)

        with col1:

            p = st.number_input(
                "p (primo)",
                value=61,
                step=1,
                min_value=2,
            )

            q = st.number_input(
                "q (primo)",
                value=53,
                step=1,
                min_value=2,
            )

            e = st.number_input(
                "e (exponente público)",
                value=17,
                step=1,
                min_value=2,
            )

        with col2:

            m = st.number_input(
                "Mensaje m (número < n)",
                value=65,
                step=1,
                min_value=0,
            )

        if st.button(
            "Calcular",
            type="primary",
            use_container_width=True,
        ):

            try:

                n, phi, d, c, back = cu.rsa_demo(
                    int(p),
                    int(q),
                    int(e),
                    int(m),
                )

                show_result(
                    f"n = p·q = {n}\n"
                    f"φ(n) = (p−1)(q−1) = {phi}\n"
                    f"d = e⁻¹ mod φ(n) = {d}\n"
                    f"Cifrado: c = m^e mod n = {c}\n"
                    f"Descifrado: m = c^d mod n = {back}",
                    f"Clave pública: (n={n}, e={int(e)})\n"
                    f"Clave privada: (n={n}, d={d})",
                )

            except ValueError as err:

                st.error(str(err))

    elif sub.startswith("3.3"):

        col1, col2, col3 = st.columns(3)

        with col1:

            base = st.number_input(
                "Base",
                value=7,
                step=1,
            )

        with col2:

            exp = st.number_input(
                "Exponente",
                value=560,
                step=1,
                min_value=0,
            )

        with col3:

            m = st.number_input(
                "Módulo",
                value=561,
                step=1,
                min_value=1,
            )

        if st.button(
            "Calcular",
            type="primary",
            use_container_width=True,
        ):

            result, binary, rows = cu.fast_pow_steps(
                int(base),
                int(exp),
                int(m),
            )

            table = (
                "bit | cuadrado | ×base si bit=1\n"
            )

            for row in rows:

                table += (
                    f"{row['bit']} | "
                    f"{row['cuadrado']} | "
                    f"{row['tras_mult']}\n"
                )

            show_result(
                f"{int(base)}^{int(exp)} mod {int(m)} = {result}",
                f"Exponente en binario: {binary}\n\n{table}",
            )


# ============================================================================
# 4. ALGORITMOS HASH
# ============================================================================

elif menu == MENU_4:

    sub = st.selectbox(
        "Algoritmo",
        [
            "4.1 MD5",
            "4.2 SHA-256",
            "4.3 SHA-512",
        ],
    )

    text = st.text_input(
        "Texto",
        "Universidad Autónoma de Bucaramanga",
    )

    algo = {
        "4.1": "MD5",
        "4.2": "SHA256",
        "4.3": "SHA512",
    }[sub.split()[0]]

    if st.button(
        "Generar hash",
        type="primary",
        use_container_width=True,
    ):

        result = cu.hash_text(
            text,
            algo,
        )

        show_result(
            f"{algo}: {result}"
        )


# ============================================================================
# 5. CODIFICACIÓN
# ============================================================================

elif menu == MENU_5:

    sub = st.selectbox(
        "Formato",
        [
            "5.1 ASCII",
            "5.2 Hexadecimal",
            "5.3 Binario",
            "5.4 Base64",
        ],
    )

    text = st.text_input(
        "Texto / valor a codificar o decodificar",
        "Hola",
    )

    mode = st.radio(
        "Modo",
        ["Codificar", "Decodificar"],
        horizontal=True,
    )

    if st.button(
        "Procesar",
        type="primary",
        use_container_width=True,
    ):

        try:

            if sub.startswith("5.1"):

                out = (
                    cu.to_ascii(text)
                    if mode == "Codificar"
                    else cu.from_ascii(text)
                )

            elif sub.startswith("5.2"):

                out = (
                    cu.to_hex(text)
                    if mode == "Codificar"
                    else cu.from_hex(text)
                )

            elif sub.startswith("5.3"):

                out = (
                    cu.to_binary(text)
                    if mode == "Codificar"
                    else cu.from_binary(text)
                )

            else:

                out = (
                    cu.to_b64(text)
                    if mode == "Codificar"
                    else cu.from_b64(text)
                )

            show_result(out)

        except Exception as err:

            st.error(
                f"Entrada inválida para decodificar: {err}"
            )


# ============================================================================
# 6. USO DE SALT
# ============================================================================

elif menu == MENU_6:

    sub = st.selectbox(
        "Algoritmo",
        [
            "6.1 Hash con SALT — MD5",
            "6.2 Hash con SALT — SHA-256",
            "6.3 Hash con SALT — SHA-512",
        ],
    )

    algo = {
        "6.1": "MD5",
        "6.2": "SHA256",
        "6.3": "SHA512",
    }[sub.split()[0]]

    password = st.text_input(
        "Contraseña",
        "MiClaveSecreta",
        type="password",
    )

    if st.button(
        "Generar hashes con SALT",
        type="primary",
        use_container_width=True,
    ):

        results = cu.salted_hashes(
            password,
            algo,
        )

        table = (
            "Salt | Hash (" + algo + ")\n"
            + "\n".join(
                f"{s} | {h}"
                for s, h in results
            )
        )

        show_result(
            f'Contraseña: "{password}" — '
            f"3 hashes con salts distintos:",
            table,
        )


# ============================================================================
# PIE DE APLICACIÓN
# ============================================================================

st.markdown(
    """
    <div class="app-footer">
        CriptoCalc · Matemática modular · Criptografía · Hash · Codificación
        <br>
        UNAB · Proyecto de Grado I — SIEM-IA
    </div>
    """,
    unsafe_allow_html=True,
)
```
