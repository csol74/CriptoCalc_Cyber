"""
app.py — CriptoCalc (versión Streamlit)
Calculadora de matemática modular, criptografía clásica y moderna,
algoritmos hash, codificación y uso de SALT.

Ejecutar localmente:
    streamlit run app.py
"""

import streamlit as st
import crypto_utils as cu

st.set_page_config(page_title="CriptoCalc", page_icon="🔐", layout="centered")

st.markdown(
    """
    <style>
    /* Caja de resultado con efecto "hundido" (neumorfismo), sobre el
       tema claro definido en .streamlit/config.toml — así combina con
       el resto de la app tanto en local como en Streamlit Cloud. */
    .result-box {
        background:#E7EBF2;
        color:#2b3644;
        border-radius:16px;
        padding:16px 18px;
        margin-top:6px;
        box-shadow: inset 5px 5px 10px #b9c0cf, inset -5px -5px 10px #ffffff;
        font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
        font-size:14.5px;
        white-space: pre-wrap;
    }
    div.stButton > button[kind="primary"] {
        border-radius: 12px;
        box-shadow: 4px 4px 10px #b9c0cf, -4px -4px 10px #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🔐 CriptoCalc")
st.caption("Matemática modular · Criptografía clásica y moderna · Hash · Codificación · SALT")

MENU_1 = "1. Operaciones matemáticas modulares"
MENU_2 = "2. Criptografía Clásica"
MENU_3 = "3. Criptografía Moderna"
MENU_4 = "4. Algoritmos Hash"
MENU_5 = "5. Codificación"
MENU_6 = "6. Uso de SALT"

menu = st.sidebar.radio(
    "Menú principal",
    [MENU_1, MENU_2, MENU_3, MENU_4, MENU_5, MENU_6],
)

st.sidebar.markdown("---")
st.sidebar.caption("UNAB · Proyecto de Grado I — SIEM-IA")


def show_result(main_text: str, steps_text: str = ""):
    st.markdown(f'<div class="result-box">{main_text}</div>', unsafe_allow_html=True)
    if steps_text:
        with st.expander("Ver pasos / tabla"):
            st.code(steps_text, language="text")


# ===========================================================================
# 1. MATEMÁTICA MODULAR
# ===========================================================================
if menu == MENU_1:
    sub = st.selectbox(
        "Submenú",
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
        a = st.number_input("a", value=17, step=1)
        n = st.number_input("n", value=5, step=1, min_value=1)
        if st.button("Calcular", type="primary"):
            b = cu.mod(int(a), int(n))
            show_result(f"{int(a)} mod {int(n)} = {b}",
                        f"b = a − n·⌊a/n⌋ = {int(a)} − {int(n)}·{int(a)//int(n)} = {b}")

    elif sub.startswith("1.2"):
        a = st.number_input("a", value=7, step=1)
        n = st.number_input("n (módulo)", value=12, step=1, min_value=1)
        if st.button("Calcular", type="primary"):
            inv = cu.mod(-int(a), int(n))
            show_result(f"Inverso aditivo de {int(a)} mod {int(n)} = {inv}",
                        f"({int(a)} + {inv}) mod {int(n)} = {cu.mod(int(a)+inv, int(n))} ✔")

    elif sub.startswith("1.3"):
        a = st.number_input("Valor a (decimal)", value=12, step=1, min_value=0)
        c = st.number_input("Resultado c = a ⊕ b (decimal)", value=9, step=1, min_value=0)
        if st.button("Calcular", type="primary"):
            b = int(a) ^ int(c)
            show_result(f"b = a ⊕ c = {int(a)} ⊕ {int(c)} = {b}",
                        f"Binario: {bin(int(a))} ⊕ {bin(int(c))} = {bin(b)}\n"
                        f"Comprobación: {int(a)} ⊕ {b} = {int(a)^b} (debe ser {int(c)})")

    elif sub.startswith("1.4"):
        a = st.number_input("a", value=8, step=1)
        n = st.number_input("n", value=17, step=1, min_value=1)
        if st.button("Calcular", type="primary"):
            g, steps = cu.gcd_steps(int(a), int(n))
            existe = g == 1
            show_result(
                f"MCD({int(a)}, {int(n)}) = {g}\n"
                + ("✔ Existe inverso multiplicativo (gcd = 1)" if existe
                   else "✘ No existe inverso multiplicativo (gcd ≠ 1)"),
                "\n".join(steps),
            )

    elif sub.startswith("1.5"):
        a = st.number_input("a", value=3, step=1)
        n = st.number_input("n (módulo)", value=11, step=1, min_value=2)
        if st.button("Calcular", type="primary"):
            found, rows = cu.multiplicative_inverse_traditional(int(a), int(n))
            table = "x | a·x mod n\n" + "\n".join(f"{x} | {r}" for x, r in rows)
            if found is not None:
                show_result(f"Inverso multiplicativo de {int(a)} mod {int(n)} = {found}", table)
            else:
                show_result(f"No existe inverso multiplicativo de {int(a)} mod {int(n)} (gcd ≠ 1)", table)

    elif sub.startswith("1.6"):
        a = st.number_input("a", value=3, step=1)
        n = st.number_input("n (módulo)", value=11, step=1, min_value=2)
        if st.button("Calcular", type="primary"):
            g, x, _y, rows = cu.extended_euclid(int(a), int(n))
            table = "Ronda | q | r_ant | r_act | resto | s | t\n"
            for row in rows:
                table += (f"{row['ronda']} | {row['q']} | {row['r_ant']} | "
                          f"{row['r_act']} | {row['resto']} | {row['s']} | {row['t']}\n")
            if g == 1:
                inv = cu.mod(x, int(n))
                show_result(
                    f"MCD({int(a)},{int(n)}) = {g}\n"
                    f"Inverso multiplicativo de {int(a)} mod {int(n)} = {inv}\n"
                    f"(rondas: {len(rows)})",
                    table,
                )
            else:
                show_result(f"MCD({int(a)},{int(n)}) = {g}\nNo existe inverso multiplicativo (gcd ≠ 1)", table)

# ===========================================================================
# 2. CRIPTOGRAFÍA CLÁSICA
# ===========================================================================
elif menu == MENU_2:
    sub = st.selectbox(
        "Submenú",
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
        text = st.text_input("Texto", "HOLA MUNDO")
        key = st.number_input("Clave (0-26)", value=3, step=1, min_value=0, max_value=26)
        mode = st.radio("Modo", ["Cifrar", "Descifrar"], horizontal=True)
        if st.button("Calcular", type="primary"):
            clean, out = cu.shift_cipher(text, int(key), cu.A27, decrypt=(mode == "Descifrar"))
            show_result(f"Texto limpio: {clean}\nResultado: {out}",
                        f"Alfabeto (27): {cu.A27}\nDesplazamiento: k={int(key)}")

    elif sub.startswith("2.2"):
        text = st.text_input("Texto", "HOLA MUNDO", key="cesar_text")
        key = st.number_input("Clave (0-25)", value=3, step=1, min_value=0, max_value=25, key="cesar_key")
        mode = st.radio("Modo", ["Cifrar", "Descifrar"], horizontal=True, key="cesar_mode")
        if st.button("Calcular", key="cesar_btn", type="primary"):
            clean, out = cu.shift_cipher(text, int(key), cu.A26, decrypt=(mode == "Descifrar"))
            show_result(f"Texto limpio: {clean}\nResultado: {out}",
                        f"Alfabeto (26): {cu.A26}\nDesplazamiento: k={int(key)}")

    elif sub.startswith("2.3"):
        text = st.text_input("Texto (o hex si descifras)", "HOLA")
        key = st.text_input("Clave (texto)", "CLAVE")
        mode = st.radio("Modo", ["Cifrar", "Descifrar"], horizontal=True, key="vernam_mode")
        if st.button("Calcular", key="vernam_btn", type="primary"):
            if not key:
                st.warning("La clave no puede estar vacía.")
            else:
                out = cu.vernam(text, key, decrypt=(mode == "Descifrar"))
                show_result(f"Resultado: {out}", "Clave repetida byte a byte con XOR (⊕). Resultado en hexadecimal.")

    elif sub.startswith("2.4"):
        text = st.text_input("Texto", "HOLA MUNDO", key="atbash_text")
        if st.button("Calcular", key="atbash_btn", type="primary"):
            clean, out = cu.atbash(text)
            show_result(f"Texto limpio: {clean}\nResultado: {out}", "ATBASH: letra_i ↔ letra_(25−i)")

    elif sub.startswith("2.5"):
        text = st.text_input("Texto", "ATACAR AL AMANECER")
        key = st.text_input("Clave (palabra o dígitos, ej: 3142)", "CLAVE")
        mode = st.radio("Modo", ["Cifrar", "Descifrar"], horizontal=True, key="col_mode")
        if st.button("Calcular", key="col_btn", type="primary"):
            if mode == "Cifrar":
                padded, out, order, rows, cols = cu.columnar_encrypt(text, key)
                show_result(f"Texto (relleno con X): {padded}\nResultado: {out}",
                            f"Columnas: {cols} · Filas: {rows}\nOrden de lectura: {order}")
            else:
                cipher_clean = cu.only_letters(text, cu.A26)
                out, order, rows, cols = cu.columnar_decrypt(cipher_clean, key)
                show_result(f"Resultado: {out}",
                            f"Columnas: {cols} · Filas: {rows}\nOrden de lectura: {order}")

    elif sub.startswith("2.6"):
        text = st.text_input("Texto", "HOLA MUNDO", key="afin_text")
        a = st.number_input("a", value=5, step=1, key="afin_a")
        b = st.number_input("b", value=8, step=1, key="afin_b")
        mode = st.radio("Modo", ["Cifrar", "Descifrar"], horizontal=True, key="afin_mode")
        if st.button("Calcular", key="afin_btn", type="primary"):
            try:
                clean, out = cu.affine(text, int(a), int(b), cu.A26, decrypt=(mode == "Descifrar"))
                formula = "D(y) = a⁻¹·(y − b) mod 26" if mode == "Descifrar" else f"E(x) = ({int(a)}·x + {int(b)}) mod 26"
                show_result(f"Texto limpio: {clean}\nResultado: {out}", formula)
            except ValueError as e:
                st.error(str(e))

    elif sub.startswith("2.7"):
        text = st.text_input("Texto", "HOLA MUNDO", key="sub_text")
        key = st.text_input("Clave (palabra)", "CRIPTO")
        mode = st.radio("Modo", ["Cifrar", "Descifrar"], horizontal=True, key="sub_mode")
        if st.button("Calcular", key="sub_btn", type="primary"):
            clean, out, cipher_alpha = cu.substitution(text, key, decrypt=(mode == "Descifrar"))
            show_result(f"Texto limpio: {clean}\nResultado: {out}",
                        f"Alfabeto claro:   {cu.A26}\nAlfabeto cifrado: {cipher_alpha}")

# ===========================================================================
# 3. CRIPTOGRAFÍA MODERNA
# ===========================================================================
elif menu == MENU_3:
    sub = st.selectbox(
        "Submenú",
        [
            "3.1 Diffie-Hellman",
            "3.2 RSA",
            "3.3 Algoritmo de exponenciación rápida",
        ],
    )

    if sub.startswith("3.1"):
        p = st.number_input("p (primo)", value=23, step=1, min_value=2)
        g = st.number_input("g (generador)", value=5, step=1, min_value=1)
        a = st.number_input("a (privada de Alice)", value=6, step=1, min_value=1)
        b = st.number_input("b (privada de Bob)", value=15, step=1, min_value=1)
        if st.button("Calcular", type="primary"):
            A, B, sA, sB = cu.diffie_hellman(int(p), int(g), int(a), int(b))
            ok = "✔ Los secretos coinciden" if sA == sB else "✘ No coinciden (revisa los datos)"
            show_result(
                f"Clave pública Alice A = g^a mod p = {A}\n"
                f"Clave pública Bob   B = g^b mod p = {B}\n"
                f"Secreto (Alice) = B^a mod p = {sA}\n"
                f"Secreto (Bob)   = A^b mod p = {sB}\n{ok}",
                f"p={int(p)}, g={int(g)}, a={int(a)}, b={int(b)}",
            )

    elif sub.startswith("3.2"):
        p = st.number_input("p (primo)", value=61, step=1, min_value=2)
        q = st.number_input("q (primo)", value=53, step=1, min_value=2)
        e = st.number_input("e (exponente público)", value=17, step=1, min_value=2)
        m = st.number_input("Mensaje m (número < n)", value=65, step=1, min_value=0)
        if st.button("Calcular", type="primary"):
            try:
                n, phi, d, c, back = cu.rsa_demo(int(p), int(q), int(e), int(m))
                show_result(
                    f"n = p·q = {n}\n"
                    f"φ(n) = (p−1)(q−1) = {phi}\n"
                    f"d = e⁻¹ mod φ(n) = {d}\n"
                    f"Cifrado: c = m^e mod n = {c}\n"
                    f"Descifrado: m = c^d mod n = {back}",
                    f"Clave pública: (n={n}, e={int(e)})\nClave privada: (n={n}, d={d})",
                )
            except ValueError as err:
                st.error(str(err))

    elif sub.startswith("3.3"):
        base = st.number_input("Base", value=7, step=1)
        exp = st.number_input("Exponente", value=560, step=1, min_value=0)
        m = st.number_input("Módulo", value=561, step=1, min_value=1)
        if st.button("Calcular", type="primary"):
            result, binary, rows = cu.fast_pow_steps(int(base), int(exp), int(m))
            table = "bit | cuadrado | ×base si bit=1\n"
            for row in rows:
                table += f"{row['bit']} | {row['cuadrado']} | {row['tras_mult']}\n"
            show_result(
                f"{int(base)}^{int(exp)} mod {int(m)} = {result}",
                f"Exponente en binario: {binary}\n\n{table}",
            )

# ===========================================================================
# 4. ALGORITMOS HASH
# ===========================================================================
elif menu == MENU_4:
    sub = st.selectbox("Submenú", ["4.1 MD5", "4.2 SHA-256", "4.3 SHA-512"])
    text = st.text_input("Texto", "Universidad Autónoma de Bucaramanga")
    algo = {"4.1": "MD5", "4.2": "SHA256", "4.3": "SHA512"}[sub.split()[0]]
    if st.button("Calcular", type="primary"):
        show_result(f"{algo}: {cu.hash_text(text, algo)}")

# ===========================================================================
# 5. CODIFICACIÓN
# ===========================================================================
elif menu == MENU_5:
    sub = st.selectbox(
        "Submenú",
        ["5.1 ASCII", "5.2 Hexadecimal", "5.3 Binario", "5.4 Base64"],
    )
    text = st.text_input("Texto / valor a codificar o decodificar", "Hola")
    mode = st.radio("Modo", ["Codificar", "Decodificar"], horizontal=True)
    if st.button("Calcular", type="primary"):
        try:
            if sub.startswith("5.1"):
                out = cu.to_ascii(text) if mode == "Codificar" else cu.from_ascii(text)
            elif sub.startswith("5.2"):
                out = cu.to_hex(text) if mode == "Codificar" else cu.from_hex(text)
            elif sub.startswith("5.3"):
                out = cu.to_binary(text) if mode == "Codificar" else cu.from_binary(text)
            else:
                out = cu.to_b64(text) if mode == "Codificar" else cu.from_b64(text)
            show_result(out)
        except Exception as err:
            st.error(f"Entrada inválida para decodificar: {err}")

# ===========================================================================
# 6. USO DE SALT
# ===========================================================================
elif menu == MENU_6:
    sub = st.selectbox(
        "Submenú",
        ["6.1 Hash con SALT — MD5", "6.2 Hash con SALT — SHA-256", "6.3 Hash con SALT — SHA-512"],
    )
    algo = {"6.1": "MD5", "6.2": "SHA256", "6.3": "SHA512"}[sub.split()[0]]
    password = st.text_input("Contraseña", "MiClaveSecreta")
    if st.button("Generar hashes con SALT", type="primary"):
        results = cu.salted_hashes(password, algo)
        table = "Salt | Hash (" + algo + ")\n" + "\n".join(f"{s} | {h}" for s, h in results)
        show_result(f'Contraseña: "{password}" — 3 hashes con salts distintos:', table)
