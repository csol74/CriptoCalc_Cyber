"""
app.py — CriptoCalc
Calculadora de matemática modular, criptografía clásica y moderna,
algoritmos hash, codificación y uso de SALT.

Ejecutar localmente:
    streamlit run app.py
"""

import streamlit as st
import crypto_utils as cu


# ============================================================
# CONFIGURACIÓN
# ============================================================

st.set_page_config(
    page_title="CriptoCalc",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# DISEÑO VISUAL
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       VARIABLES
    ======================================================== */

    :root {
        --bg: #F4F7FB;
        --card: #FFFFFF;
        --card-soft: #EEF3F9;

        --primary: #2563EB;
        --primary-dark: #1D4ED8;
        --primary-light: #DBEAFE;

        --text: #172033;
        --muted: #64748B;

        --border: #DCE4EF;

        --dark: #111827;
        --dark-soft: #1E293B;

        --radius: 18px;
    }


    /* ========================================================
       FONDO GENERAL
    ======================================================== */

    .stApp {
        background:
            radial-gradient(
                circle at 90% 5%,
                rgba(37, 99, 235, 0.08),
                transparent 28%
            ),
            radial-gradient(
                circle at 10% 90%,
                rgba(59, 130, 246, 0.05),
                transparent 25%
            ),
            linear-gradient(
                135deg,
                #F4F7FB 0%,
                #EEF3F9 100%
            );

        color: var(--text);
    }


    /* ========================================================
       CONTENEDOR
    ======================================================== */

    .block-container {
        max-width: 1180px;
        padding-top: 2.2rem;
        padding-bottom: 4rem;
    }


    /* ========================================================
       SIDEBAR
    ======================================================== */

    section[data-testid="stSidebar"] {
        background: #111827;
        border-right: 1px solid rgba(255,255,255,0.06);
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1.7rem;
    }

    section[data-testid="stSidebar"] * {
        color: #E5E7EB;
    }


    /* Logo sidebar */

    .sidebar-logo {
        display: flex;
        align-items: center;
        gap: 12px;

        padding: 8px 8px 22px 8px;
        margin-bottom: 10px;
    }

    .sidebar-logo-icon {
        width: 42px;
        height: 42px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 13px;

        background: linear-gradient(
            145deg,
            #3B82F6,
            #1D4ED8
        );

        font-size: 20px;

        box-shadow:
            0 8px 18px rgba(37,99,235,0.30);
    }

    .sidebar-logo-title {
        font-size: 18px;
        font-weight: 800;
        letter-spacing: -0.4px;
    }

    .sidebar-logo-subtitle {
        font-size: 11px;
        color: #94A3B8;
        margin-top: 1px;
    }


    /* Radio menu */

    section[data-testid="stSidebar"] div[role="radiogroup"] {
        gap: 5px;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label {
        border-radius: 11px;
        padding: 9px 11px;

        transition:
            background 0.18s ease,
            transform 0.18s ease;
    }

    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {
        background: rgba(255,255,255,0.07);
        transform: translateX(2px);
    }


    /* ========================================================
       HEADER
    ======================================================== */

    .crypto-header {
        display: flex;
        align-items: center;
        gap: 17px;

        margin-bottom: 5px;
    }

    .crypto-logo {
        width: 62px;
        height: 62px;

        display: flex;
        align-items: center;
        justify-content: center;

        border-radius: 18px;

        background: linear-gradient(
            145deg,
            #2563EB,
            #1D4ED8
        );

        color: white;

        font-size: 29px;

        box-shadow:
            0 12px 25px rgba(37,99,235,0.24);
    }

    .crypto-title {
        font-size: 2.35rem;
        line-height: 1;

        font-weight: 850;

        letter-spacing: -1.5px;

        color: #172033;

        margin: 0;
    }

    .crypto-subtitle {
        margin-top: 7px;

        color: #64748B;

        font-size: 0.92rem;
    }


    /* ========================================================
       BADGE SUPERIOR
    ======================================================== */

    .security-badge {
        display: inline-flex;
        align-items: center;

        padding: 6px 10px;

        margin-top: 17px;

        border-radius: 999px;

        background: #E8F0FF;

        border: 1px solid #D5E3FF;

        color: #2563EB;

        font-size: 11px;
        font-weight: 750;

        letter-spacing: 0.2px;
    }


    /* ========================================================
       TARJETA PRINCIPAL
    ======================================================== */

    .operation-card {
        background:
            rgba(255,255,255,0.90);

        border:
            1px solid rgba(220,228,239,0.95);

        border-radius: 22px;

        padding: 24px 27px;

        margin-top: 25px;

        box-shadow:
            0 12px 35px rgba(37,55,80,0.07);

        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
    }

    .operation-number {
        display: inline-flex;

        align-items: center;
        justify-content: center;

        width: 31px;
        height: 31px;

        border-radius: 10px;

        background: #E8F0FF;

        color: #2563EB;

        font-size: 12px;
        font-weight: 800;

        margin-bottom: 10px;
    }

    .operation-title {
        font-size: 1.18rem;

        font-weight: 800;

        letter-spacing: -0.3px;

        color: #172033;
    }

    .operation-description {
        margin-top: 5px;

        font-size: 0.87rem;

        color: #64748B;

        line-height: 1.5;
    }


    /* ========================================================
       SELECTORES
    ======================================================== */

    div[data-baseweb="select"] > div {
        border-radius: 13px !important;
        border-color: #DCE4EF !important;
        background: #F8FAFD !important;
    }

    div[data-baseweb="select"] > div:focus-within {
        border-color: #2563EB !important;
        box-shadow:
            0 0 0 3px rgba(37,99,235,0.10);
    }


    /* ========================================================
       INPUTS
    ======================================================== */

    div[data-baseweb="input"] {
        border-radius: 13px !important;
        border: 1px solid #DCE4EF !important;
        background: #F8FAFD !important;

        transition:
            border-color 0.18s ease,
            box-shadow 0.18s ease;
    }

    div[data-baseweb="input"]:focus-within {
        border-color: #2563EB !important;

        box-shadow:
            0 0 0 3px rgba(37,99,235,0.10);
    }


    /* ========================================================
       BOTONES
    ======================================================== */

    div.stButton > button {
        width: 100%;

        min-height: 46px;

        border-radius: 13px;

        border: 1px solid #DCE4EF;

        background: #FFFFFF;

        color: #172033;

        font-weight: 700;

        transition:
            transform 0.15s ease,
            box-shadow 0.15s ease,
            background 0.15s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-1px);

        background: #F8FAFD;

        border-color: #BFCDE0;

        box-shadow:
            0 8px 18px rgba(37,55,80,0.09);
    }

    div.stButton > button[kind="primary"] {
        background:
            linear-gradient(
                135deg,
                #2563EB,
                #1D4ED8
            );

        color: white;

        border: none;

        box-shadow:
            0 8px 19px rgba(37,99,235,0.23);
    }

    div.stButton > button[kind="primary"]:hover {
        background:
            linear-gradient(
                135deg,
                #1D4ED8,
                #1E40AF
            );

        box-shadow:
            0 11px 25px rgba(37,99,235,0.29);
    }


    /* ========================================================
       RESULTADO
    ======================================================== */

    .result-box {
        position: relative;

        background:
            linear-gradient(
                145deg,
                #172033,
                #0F172A
            );

        color: #E8EEF7;

        border-radius: 17px;

        padding: 20px 22px;

        margin-top: 18px;

        border:
            1px solid rgba(255,255,255,0.05);

        box-shadow:
            inset 0 1px 0 rgba(255,255,255,0.04),
            0 12px 28px rgba(15,23,42,0.16);

        font-family:
            ui-monospace,
            "SF Mono",
            Menlo,
            Consolas,
            monospace;

        font-size: 14px;

        line-height: 1.65;

        white-space: pre-wrap;

        overflow-x: auto;
    }

    .result-box::before {
        content: "RESULTADO";

        display: block;

        color: #60A5FA;

        font-family:
            -apple-system,
            BlinkMacSystemFont,
            "Segoe UI",
            sans-serif;

        font-size: 10px;

        font-weight: 800;

        letter-spacing: 1.6px;

        margin-bottom: 9px;
    }


    /* ========================================================
       EXPANDER
    ======================================================== */

    div[data-testid="stExpander"] {
        margin-top: 12px;

        border:
            1px solid #DCE4EF;

        border-radius: 14px;

        background:
            rgba(255,255,255,0.72);
    }


    /* ========================================================
       RADIO / MODO
    ======================================================== */

    div[role="radiogroup"] {
        gap: 7px;
    }


    /* ========================================================
       ALERTAS
    ======================================================== */

    div[data-testid="stAlert"] {
        border-radius: 13px;
    }


    /* ========================================================
       FOOTER
    ======================================================== */

    .app-footer {
        text-align: center;

        margin-top: 45px;

        padding-top: 20px;

        border-top: 1px solid #DCE4EF;

        color: #94A3B8;

        font-size: 11px;
    }


    /* ========================================================
       RESPONSIVE
    ======================================================== */

    @media (max-width: 768px) {

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
            padding-top: 1.5rem;
        }

        .crypto-title {
            font-size: 1.9rem;
        }

        .crypto-logo {
            width: 52px;
            height: 52px;
            font-size: 24px;
        }

        .operation-card {
            padding: 20px;
            border-radius: 18px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <div class="sidebar-logo">

        <div class="sidebar-logo-icon">
            🔐
        </div>

        <div>
            <div class="sidebar-logo-title">
                CriptoCalc
            </div>

            <div class="sidebar-logo-subtitle">
                Crypto Laboratory
            </div>
        </div>

    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# MENÚ
# ============================================================

MENU_1 = "1. Operaciones matemáticas modulares"
MENU_2 = "2. Criptografía Clásica"
MENU_3 = "3. Criptografía Moderna"
MENU_4 = "4. Algoritmos Hash"
MENU_5 = "5. Codificación"
MENU_6 = "6. Uso de SALT"

menu = st.sidebar.radio(
    "MENÚ PRINCIPAL",
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

st.sidebar.caption(
    "UNAB · Proyecto de Grado I — SIEM-IA"
)


# ============================================================
# HEADER PRINCIPAL
# ============================================================

st.markdown(
    """
    <div class="crypto-header">

        <div class="crypto-logo">
            🔐
        </div>

        <div>
            <div class="crypto-title">
                CriptoCalc
            </div>

            <div class="crypto-subtitle">
                Laboratorio interactivo de matemática y criptografía
            </div>
        </div>

    </div>

    <div class="security-badge">
        ● SISTEMA DE CÁLCULO CRIPTOGRÁFICO
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# FUNCIÓN DE RESULTADOS
# ============================================================

def show_result(main_text: str, steps_text: str = ""):

    st.markdown(
        f'<div class="result-box">{main_text}</div>',
        unsafe_allow_html=True
    )

    if steps_text:

        with st.expander("Ver pasos / tabla"):

            st.code(
                steps_text,
                language="text"
            )


# ============================================================
# FUNCIÓN PARA ENCABEZADOS
# ============================================================

def show_section(number, title, description):

    st.markdown(
        f"""
        <div class="operation-card">

            <div class="operation-number">
                {number}
            </div>

            <div class="operation-title">
                {title}
            </div>

            <div class="operation-description">
                {description}
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )


# ========================================================================
# 1. MATEMÁTICA MODULAR
# ========================================================================

if menu == MENU_1:

    show_section(
        "01",
        "Operaciones matemáticas modulares",
        "Calcula módulos, inversos, MCD y operaciones XOR."
    )

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


    if sub.startswith("1.1"):

        a = st.number_input(
            "Valor a",
            value=17,
            step=1
        )

        n = st.number_input(
            "Módulo n",
            value=5,
            step=1,
            min_value=1
        )

        if st.button(
            "Calcular módulo",
            type="primary"
        ):

            b = cu.mod(
                int(a),
                int(n)
            )

            show_result(
                f"{int(a)} mod {int(n)} = {b}",
                f"b = a − n·⌊a/n⌋ = "
                f"{int(a)} − {int(n)}·"
                f"{int(a)//int(n)} = {b}"
            )


    elif sub.startswith("1.2"):

        a = st.number_input(
            "Valor a",
            value=7,
            step=1
        )

        n = st.number_input(
            "Módulo n",
            value=12,
            step=1,
            min_value=1
        )

        if st.button(
            "Calcular inverso",
            type="primary"
        ):

            inv = cu.mod(
                -int(a),
                int(n)
            )

            show_result(
                f"Inverso aditivo de "
                f"{int(a)} mod {int(n)} = {inv}",
                f"({int(a)} + {inv}) mod "
                f"{int(n)} = "
                f"{cu.mod(int(a)+inv, int(n))} ✔"
            )


    elif sub.startswith("1.3"):

        a = st.number_input(
            "Valor a (decimal)",
            value=12,
            step=1,
            min_value=0
        )

        c = st.number_input(
            "Resultado c = a ⊕ b (decimal)",
            value=9,
            step=1,
            min_value=0
        )

        if st.button(
            "Calcular XOR",
            type="primary"
        ):

            b = int(a) ^ int(c)

            show_result(
                f"b = a ⊕ c = "
                f"{int(a)} ⊕ {int(c)} = {b}",

                f"Binario: "
                f"{bin(int(a))} ⊕ "
                f"{bin(int(c))} = "
                f"{bin(b)}\n\n"

                f"Comprobación: "
                f"{int(a)} ⊕ {b} = "
                f"{int(a)^b} "
                f"(debe ser {int(c)})"
            )


    elif sub.startswith("1.4"):

        a = st.number_input(
            "Valor a",
            value=8,
            step=1
        )

        n = st.number_input(
            "Valor n",
            value=17,
            step=1,
            min_value=1
        )

        if st.button(
            "Calcular MCD",
            type="primary"
        ):

            g, steps = cu.gcd_steps(
                int(a),
                int(n)
            )

            existe = g == 1

            show_result(
                f"MCD({int(a)}, {int(n)}) = {g}\n"
                +
                (
                    "✔ Existe inverso multiplicativo "
                    "(MCD = 1)"
                    if existe
                    else
                    "✘ No existe inverso multiplicativo "
                    "(MCD ≠ 1)"
                ),

                "\n".join(steps)
            )


    elif sub.startswith("1.5"):

        a = st.number_input(
            "Valor a",
            value=3,
            step=1
        )

        n = st.number_input(
            "Módulo n",
            value=11,
            step=1,
            min_value=2
        )

        if st.button(
            "Buscar inverso",
            type="primary"
        ):

            found, rows = (
                cu.multiplicative_inverse_traditional(
                    int(a),
                    int(n)
                )
            )

            table = (
                "x | a·x mod n\n"
                +
                "\n".join(
                    f"{x} | {r}"
                    for x, r in rows
                )
            )

            if found is not None:

                show_result(
                    f"Inverso multiplicativo de "
                    f"{int(a)} mod {int(n)} = {found}",
                    table
                )

            else:

                show_result(
                    f"No existe inverso multiplicativo "
                    f"de {int(a)} mod {int(n)} "
                    f"(MCD ≠ 1)",
                    table
                )


    elif sub.startswith("1.6"):

        a = st.number_input(
            "Valor a",
            value=3,
            step=1
        )

        n = st.number_input(
            "Módulo n",
            value=11,
            step=1,
            min_value=2
        )

        if st.button(
            "Ejecutar Euclides",
            type="primary"
        ):

            g, x, _y, rows = (
                cu.extended_euclid(
                    int(a),
                    int(n)
                )
            )

            table = (
                "Ronda | q | r_ant | "
                "r_act | resto | s | t\n"
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

                inv = cu.mod(
                    x,
                    int(n)
                )

                show_result(
                    f"MCD({int(a)},{int(n)}) = {g}\n"
                    f"Inverso multiplicativo de "
                    f"{int(a)} mod {int(n)} = {inv}\n"
                    f"(rondas: {len(rows)})",
                    table
                )

            else:

                show_result(
                    f"MCD({int(a)},{int(n)}) = {g}\n"
                    f"No existe inverso multiplicativo "
                    f"(MCD ≠ 1)",
                    table
                )


# ========================================================================
# 2. CRIPTOGRAFÍA CLÁSICA
# ========================================================================

elif menu == MENU_2:

    show_section(
        "02",
        "Criptografía clásica",
        "Experimenta con diferentes técnicas de cifrado y descifrado."
    )

    sub = st.selectbox(
        "Método criptográfico",
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
            "HOLA MUNDO"
        )

        key = st.number_input(
            "Clave (0-26)",
            value=3,
            step=1,
            min_value=0,
            max_value=26
        )

        mode = st.radio(
            "Modo",
            ["Cifrar", "Descifrar"],
            horizontal=True
        )

        if st.button(
            "Ejecutar cifrado",
            type="primary"
        ):

            clean, out = cu.shift_cipher(
                text,
                int(key),
                cu.A27,
                decrypt=(mode == "Descifrar")
            )

            show_result(
                f"Texto limpio: {clean}\n"
                f"Resultado: {out}",

                f"Alfabeto (27): {cu.A27}\n"
                f"Desplazamiento: k={int(key)}"
            )


    elif sub.startswith("2.2"):

        text = st.text_input(
            "Texto",
            "HOLA MUNDO",
            key="cesar_text"
        )

        key = st.number_input(
            "Clave (0-25)",
            value=3,
            step=1,
            min_value=0,
            max_value=25,
            key="cesar_key"
        )

        mode = st.radio(
            "Modo",
            ["Cifrar", "Descifrar"],
            horizontal=True,
            key="cesar_mode"
        )

        if st.button(
            "Ejecutar César",
            key="cesar_btn",
            type="primary"
        ):

            clean, out = cu.shift_cipher(
                text,
                int(key),
                cu.A26,
                decrypt=(mode == "Descifrar")
            )

            show_result(
                f"Texto limpio: {clean}\n"
                f"Resultado: {out}",

                f"Alfabeto (26): {cu.A26}\n"
                f"Desplazamiento: k={int(key)}"
            )


    elif sub.startswith("2.3"):

        text = st.text_input(
            "Texto (o hexadecimal si descifras)",
            "HOLA"
        )

        key = st.text_input(
            "Clave",
            "CLAVE"
        )

        mode = st.radio(
            "Modo",
            ["Cifrar", "Descifrar"],
            horizontal=True,
            key="vernam_mode"
        )

        if st.button(
            "Ejecutar Vernam",
            key="vernam_btn",
            type="primary"
        ):

            if not key:

                st.warning(
                    "La clave no puede estar vacía."
                )

            else:

                out = cu.vernam(
                    text,
                    key,
                    decrypt=(mode == "Descifrar")
                )

                show_result(
                    f"Resultado: {out}",
                    "Clave repetida byte a byte con XOR (⊕).\n"
                    "Resultado en hexadecimal."
                )


    elif sub.startswith("2.4"):

        text = st.text_input(
            "Texto",
            "HOLA MUNDO",
            key="atbash_text"
        )

        if st.button(
            "Ejecutar ATBASH",
            key="atbash_btn",
            type="primary"
        ):

            clean, out = cu.atbash(text)

            show_result(
                f"Texto limpio: {clean}\n"
                f"Resultado: {out}",

                "ATBASH: letra_i ↔ letra_(25−i)"
            )


    elif sub.startswith("2.5"):

        text = st.text_input(
            "Texto",
            "ATACAR AL AMANECER"
        )

        key = st.text_input(
            "Clave",
            "CLAVE"
        )

        mode = st.radio(
            "Modo",
            ["Cifrar", "Descifrar"],
            horizontal=True,
            key="col_mode"
        )

        if st.button(
            "Ejecutar transposición",
            key="col_btn",
            type="primary"
        ):

            if mode == "Cifrar":

                padded, out, order, rows, cols = (
                    cu.columnar_encrypt(
                        text,
                        key
                    )
                )

                show_result(
                    f"Texto (relleno con X): {padded}\n"
                    f"Resultado: {out}",

                    f"Columnas: {cols} · Filas: {rows}\n"
                    f"Orden de lectura: {order}"
                )

            else:

                cipher_clean = cu.only_letters(
                    text,
                    cu.A26
                )

                out, order, rows, cols = (
                    cu.columnar_decrypt(
                        cipher_clean,
                        key
                    )
                )

                show_result(
                    f"Resultado: {out}",

                    f"Columnas: {cols} · Filas: {rows}\n"
                    f"Orden de lectura: {order}"
                )


    elif sub.startswith("2.6"):

        text = st.text_input(
            "Texto",
            "HOLA MUNDO",
            key="afin_text"
        )

        a = st.number_input(
            "a",
            value=5,
            step=1,
            key="afin_a"
        )

        b = st.number_input(
            "b",
            value=8,
            step=1,
            key="afin_b"
        )

        mode = st.radio(
            "Modo",
            ["Cifrar", "Descifrar"],
            horizontal=True,
            key="afin_mode"
        )

        if st.button(
            "Ejecutar afín",
            key="afin_btn",
            type="primary"
        ):

            try:

                clean, out = cu.affine(
                    text,
                    int(a),
                    int(b),
                    cu.A26,
                    decrypt=(mode == "Descifrar")
                )

                formula = (
                    "D(y) = a⁻¹·(y − b) mod 26"
                    if mode == "Descifrar"
                    else
                    f"E(x) = ({int(a)}·x + "
                    f"{int(b)}) mod 26"
                )

                show_result(
                    f"Texto limpio: {clean}\n"
                    f"Resultado: {out}",
                    formula
                )

            except ValueError as e:

                st.error(str(e))


    elif sub.startswith("2.7"):

        text = st.text_input(
            "Texto",
            "HOLA MUNDO",
            key="sub_text"
        )

        key = st.text_input(
            "Clave",
            "CRIPTO"
        )

        mode = st.radio(
            "Modo",
            ["Cifrar", "Descifrar"],
            horizontal=True,
            key="sub_mode"
        )

        if st.button(
            "Ejecutar sustitución",
            key="sub_btn",
            type="primary"
        ):

            clean, out, cipher_alpha = (
                cu.substitution(
                    text,
                    key,
                    decrypt=(mode == "Descifrar")
                )
            )

            show_result(
                f"Texto limpio: {clean}\n"
                f"Resultado: {out}",

                f"Alfabeto claro:   {cu.A26}\n"
                f"Alfabeto cifrado: {cipher_alpha}"
            )


# ========================================================================
# 3. CRIPTOGRAFÍA MODERNA
# ========================================================================

elif menu == MENU_3:

    show_section(
        "03",
        "Criptografía moderna",
        "Experimenta con Diffie-Hellman, RSA y exponenciación rápida."
    )

    sub = st.selectbox(
        "Algoritmo",
        [
            "3.1 Diffie-Hellman",
            "3.2 RSA",
            "3.3 Algoritmo de exponenciación rápida",
        ],
    )


    if sub.startswith("3.1"):

        p = st.number_input(
            "p (primo)",
            value=23,
            step=1,
            min_value=2
        )

        g = st.number_input(
            "g (generador)",
            value=5,
            step=1,
            min_value=1
        )

        a = st.number_input(
            "a (privada de Alice)",
            value=6,
            step=1,
            min_value=1
        )

        b = st.number_input(
            "b (privada de Bob)",
            value=15,
            step=1,
            min_value=1
        )

        if st.button(
            "Ejecutar Diffie-Hellman",
            type="primary"
        ):

            A, B, sA, sB = (
                cu.diffie_hellman(
                    int(p),
                    int(g),
                    int(a),
                    int(b)
                )
            )

            ok = (
                "✔ Los secretos coinciden"
                if sA == sB
                else
                "✘ No coinciden (revisa los datos)"
            )

            show_result(

                f"Clave pública Alice:\n"
                f"A = g^a mod p = {A}\n\n"

                f"Clave pública Bob:\n"
                f"B = g^b mod p = {B}\n\n"

                f"Secreto Alice:\n"
                f"B^a mod p = {sA}\n\n"

                f"Secreto Bob:\n"
                f"A^b mod p = {sB}\n\n"

                f"{ok}",

                f"p={int(p)}, "
                f"g={int(g)}, "
                f"a={int(a)}, "
                f"b={int(b)}"
            )


    elif sub.startswith("3.2"):

        p = st.number_input(
            "p (primo)",
            value=61,
            step=1,
            min_value=2
        )

        q = st.number_input(
            "q (primo)",
            value=53,
            step=1,
            min_value=2
        )

        e = st.number_input(
            "e (exponente público)",
            value=17,
            step=1,
            min_value=2
        )

        m = st.number_input(
            "Mensaje m",
            value=65,
            step=1,
            min_value=0
        )

        if st.button(
            "Ejecutar RSA",
            type="primary"
        ):

            try:

                n, phi, d, c, back = (
                    cu.rsa_demo(
                        int(p),
                        int(q),
                        int(e),
                        int(m)
                    )
                )

                show_result(

                    f"n = p·q = {n}\n"
                    f"φ(n) = (p−1)(q−1) = {phi}\n"
                    f"d = e⁻¹ mod φ(n) = {d}\n\n"

                    f"Cifrado:\n"
                    f"c = m^e mod n = {c}\n\n"

                    f"Descifrado:\n"
                    f"m = c^d mod n = {back}",

                    f"Clave pública: "
                    f"(n={n}, e={int(e)})\n"
                    f"Clave privada: "
                    f"(n={n}, d={d})"
                )

            except ValueError as err:

                st.error(str(err))


    elif sub.startswith("3.3"):

        base = st.number_input(
            "Base",
            value=7,
            step=1
        )

        exp = st.number_input(
            "Exponente",
            value=560,
            step=1,
            min_value=0
        )

        m = st.number_input(
            "Módulo",
            value=561,
            step=1,
            min_value=1
        )

        if st.button(
            "Ejecutar exponenciación",
            type="primary"
        ):

            result, binary, rows = (
                cu.fast_pow_steps(
                    int(base),
                    int(exp),
                    int(m)
                )
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
                f"{int(base)}^{int(exp)} "
                f"mod {int(m)} = {result}",

                f"Exponente en binario: "
                f"{binary}\n\n"
                f"{table}"
            )


# ========================================================================
# 4. HASH
# ========================================================================

elif menu == MENU_4:

    show_section(
        "04",
        "Algoritmos Hash",
        "Genera hashes utilizando MD5, SHA-256 y SHA-512."
    )

    sub = st.selectbox(
        "Algoritmo",
        [
            "4.1 MD5",
            "4.2 SHA-256",
            "4.3 SHA-512"
        ]
    )

    text = st.text_input(
        "Texto",
        "Universidad Autónoma de Bucaramanga"
    )

    algo = {
        "4.1": "MD5",
        "4.2": "SHA256",
        "4.3": "SHA512"
    }[
        sub.split()[0]
    ]

    if st.button(
        "Generar Hash",
        type="primary"
    ):

        show_result(
            f"{algo}:\n\n"
            f"{cu.hash_text(text, algo)}"
        )


# ========================================================================
# 5. CODIFICACIÓN
# ========================================================================

elif menu == MENU_5:

    show_section(
        "05",
        "Codificación",
        "Convierte información entre ASCII, hexadecimal, binario y Base64."
    )

    sub = st.selectbox(
        "Método",
        [
            "5.1 ASCII",
            "5.2 Hexadecimal",
            "5.3 Binario",
            "5.4 Base64"
        ]
    )

    text = st.text_input(
        "Texto / valor",
        "Hola"
    )

    mode = st.radio(
        "Modo",
        [
            "Codificar",
            "Decodificar"
        ],
        horizontal=True
    )

    if st.button(
        "Procesar",
        type="primary"
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

            show_result(
                f"Resultado:\n\n{out}"
            )

        except Exception as err:

            st.error(
                f"Entrada inválida para decodificar: {err}"
            )


# ========================================================================
# 6. SALT
# ========================================================================

elif menu == MENU_6:

    show_section(
        "06",
        "Hash con SALT",
        "Observa cómo cambia el resultado de un hash al utilizar diferentes SALT."
    )

    sub = st.selectbox(
        "Algoritmo",
        [
            "6.1 Hash con SALT — MD5",
            "6.2 Hash con SALT — SHA-256",
            "6.3 Hash con SALT — SHA-512"
        ]
    )

    algo = {
        "6.1": "MD5",
        "6.2": "SHA256",
        "6.3": "SHA512"
    }[
        sub.split()[0]
    ]

    password = st.text_input(
        "Contraseña",
        "MiClaveSecreta",
        type="password"
    )

    if st.button(
        "Generar hashes con SALT",
        type="primary"
    ):

        results = cu.salted_hashes(
            password,
            algo
        )

        table = (
            "Salt | Hash ("
            + algo
            + ")\n"
            +
            "\n".join(
                f"{s} | {h}"
                for s, h in results
            )
        )

        show_result(
            f"Contraseña procesada con {algo}\n"
            f"Se generaron {len(results)} hashes con SALT diferentes.",

            table
        )


# ========================================================================
# FOOTER
# ========================================================================

st.markdown(
    """
    <div class="app-footer">
        CriptoCalc · UNAB · Proyecto de Grado I — SIEM-IA
        <br>
        Laboratorio educativo de matemática y criptografía
    </div>
    """,
    unsafe_allow_html=True
)
