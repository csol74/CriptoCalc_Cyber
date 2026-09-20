"""
crypto_utils.py
----------------
Funciones de matemática modular, criptografía clásica, criptografía moderna,
algoritmos hash, codificación y generación de hashes con SALT.

Todo el módulo usa únicamente la librería estándar de Python (hashlib, base64,
secrets, unicodedata, string) para que no haya dependencias adicionales
además de Streamlit.
"""

import hashlib
import base64
import secrets
import string
import unicodedata

A27 = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
A26 = string.ascii_uppercase


# ---------------------------------------------------------------------------
# 1. MATEMÁTICA MODULAR
# ---------------------------------------------------------------------------

def mod(a: int, n: int) -> int:
    """Residuo de a mod n, siempre no negativo."""
    return ((a % n) + n) % n


def gcd_steps(a: int, b: int):
    """Algoritmo de Euclides clásico, devuelve el MCD y la lista de pasos."""
    steps = []
    A, B = a, b
    while B != 0:
        q = A // B
        r = A - q * B
        steps.append(f"{A} = {q}·{B} + {r}")
        A, B = B, r
    return A, steps


def extended_euclid(a: int, n: int):
    """
    Algoritmo Extendido de Euclides (AEE).
    Devuelve gcd, x, y (tales que a*x + n*y = gcd) y la tabla de rondas.
    """
    old_r, r = a, n
    old_s, s = 1, 0
    old_t, t = 0, 1
    rows = []
    round_n = 0
    while r != 0:
        q = old_r // r
        round_n += 1
        rows.append({
            "ronda": round_n, "q": q, "r_ant": old_r, "r_act": r,
            "resto": old_r - q * r, "s": old_s, "t": old_t,
        })
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    return old_r, old_s, old_t, rows


def multiplicative_inverse_traditional(a: int, n: int):
    """Busca por tabla (x = 1..n-1) el inverso multiplicativo de a mod n."""
    rows = []
    found = None
    for x in range(1, n):
        r = mod(a * x, n)
        rows.append((x, r))
        if r == 1 and found is None:
            found = x
    return found, rows


def fast_pow_steps(base: int, exp: int, m: int):
    """Exponenciación rápida (cuadrado y multiplicación) con tabla de pasos."""
    base_b = base % m
    binary = bin(exp)[2:]
    acc = 1
    rows = []
    for bit in binary:
        acc = (acc * acc) % m
        sq = acc
        if bit == "1":
            acc = (acc * base_b) % m
        rows.append({"bit": bit, "cuadrado": sq, "tras_mult": acc})
    return acc, binary, rows


# ---------------------------------------------------------------------------
# 2. CRIPTOGRAFÍA CLÁSICA
# ---------------------------------------------------------------------------

def strip_accents(s: str) -> str:
    nfkd = unicodedata.normalize("NFD", s)
    return "".join(c for c in nfkd if unicodedata.category(c) != "Mn")


def only_letters(text: str, alphabet: str) -> str:
    text = text.upper()
    if alphabet == A26:
        text = strip_accents(text).replace("Ñ", "N")
    return "".join(c for c in text if c in alphabet)


def shift_cipher(text: str, key: int, alphabet: str, decrypt: bool = False):
    clean = only_letters(text, alphabet)
    n = len(alphabet)
    k = mod(-key, n) if decrypt else mod(key, n)
    out = "".join(alphabet[mod(alphabet.index(c) + k, n)] for c in clean)
    return clean, out


def atbash(text: str):
    clean = only_letters(text, A26)
    out = "".join(A26[25 - A26.index(c)] for c in clean)
    return clean, out


def affine(text: str, a: int, b: int, alphabet: str = A26, decrypt: bool = False):
    clean = only_letters(text, alphabet)
    n = len(alphabet)
    g, _ = gcd_steps(a, n)
    if g != 1:
        raise ValueError(f"gcd({a},{n}) = {g} ≠ 1 → 'a' no tiene inverso, elige otro valor.")
    if not decrypt:
        out = "".join(alphabet[mod(a * alphabet.index(c) + b, n)] for c in clean)
    else:
        _, a_inv, _, _ = extended_euclid(a, n)
        a_inv = mod(a_inv, n)
        out = "".join(alphabet[mod(a_inv * (alphabet.index(c) - b), n)] for c in clean)
    return clean, out


def build_substitution_alphabet(keyword: str) -> str:
    keyword = only_letters(keyword, A26)
    seen, seq = set(), ""
    for c in keyword:
        if c not in seen:
            seen.add(c)
            seq += c
    for c in A26:
        if c not in seen:
            seen.add(c)
            seq += c
    return seq


def substitution(text: str, keyword: str, decrypt: bool = False):
    cipher_alpha = build_substitution_alphabet(keyword)
    clean = only_letters(text, A26)
    if not decrypt:
        out = "".join(cipher_alpha[A26.index(c)] for c in clean)
    else:
        out = "".join(A26[cipher_alpha.index(c)] for c in clean)
    return clean, out, cipher_alpha


def vernam(text: str, key: str, decrypt: bool = False) -> str:
    """Cifrado/descifrado XOR (Vernam) con clave repetida."""
    if not decrypt:
        out_bytes = [
            ord(text[i]) ^ ord(key[i % len(key)])
            for i in range(len(text))
        ]
        return " ".join(f"{b:02x}" for b in out_bytes)
    else:
        parts = text.strip().split()
        byte_vals = [int(h, 16) for h in parts]
        return "".join(chr(byte_vals[i] ^ ord(key[i % len(key)])) for i in range(len(byte_vals)))


def column_order(key: str):
    if key.isdigit():
        return [int(d) for d in key]
    indexed = list(enumerate(key.upper()))
    ordered = sorted(indexed, key=lambda p: (p[1], p[0]))
    order = [0] * len(indexed)
    for rank, (i, _c) in enumerate(ordered, start=1):
        order[i] = rank
    return order


def columnar_encrypt(text: str, key: str):
    clean = only_letters(text, A26)
    cols = len(key)
    order = column_order(key)
    rows = -(-len(clean) // cols) or 1          # ceil division
    padded = clean.ljust(rows * cols, "X")
    grid = [list(padded[r * cols:(r + 1) * cols]) for r in range(rows)]
    out = []
    for rank in range(1, cols + 1):
        col_idx = order.index(rank)
        for r in range(rows):
            out.append(grid[r][col_idx])
    return padded, "".join(out), order, rows, cols


def columnar_decrypt(cipher: str, key: str):
    cols = len(key)
    order = column_order(key)
    rows = -(-len(cipher) // cols)
    grid = [[""] * cols for _ in range(rows)]
    idx = 0
    for rank in range(1, cols + 1):
        col_idx = order.index(rank)
        for r in range(rows):
            grid[r][col_idx] = cipher[idx]
            idx += 1
    out = "".join("".join(row) for row in grid)
    return out, order, rows, cols


# ---------------------------------------------------------------------------
# 3. CRIPTOGRAFÍA MODERNA
# ---------------------------------------------------------------------------

def diffie_hellman(p: int, g: int, a: int, b: int):
    A = pow(g, a, p)
    B = pow(g, b, p)
    secret_alice = pow(B, a, p)
    secret_bob = pow(A, b, p)
    return A, B, secret_alice, secret_bob


def rsa_demo(p: int, q: int, e: int, m: int):
    n = p * q
    phi = (p - 1) * (q - 1)
    g, x, _y, _rows = extended_euclid(e, phi)
    if g != 1:
        raise ValueError(f"e={e} no es coprimo con φ(n)={phi}. Elige otro e.")
    d = mod(x, phi)
    c = pow(m, e, n)
    back = pow(c, d, n)
    return n, phi, d, c, back


# ---------------------------------------------------------------------------
# 4. ALGORITMOS HASH
# ---------------------------------------------------------------------------

def hash_text(text: str, algo: str) -> str:
    data = text.encode("utf-8")
    if algo == "MD5":
        return hashlib.md5(data).hexdigest()
    if algo == "SHA256":
        return hashlib.sha256(data).hexdigest()
    if algo == "SHA512":
        return hashlib.sha512(data).hexdigest()
    raise ValueError("Algoritmo no soportado")


# ---------------------------------------------------------------------------
# 5. CODIFICACIÓN
# ---------------------------------------------------------------------------

def to_ascii(text: str) -> str:
    return " ".join(str(ord(c)) for c in text)


def from_ascii(codes: str) -> str:
    return "".join(chr(int(c)) for c in codes.split())


def to_hex(text: str) -> str:
    return " ".join(f"{b:02x}" for b in text.encode("utf-8"))


def from_hex(hex_str: str) -> str:
    b = bytes(int(h, 16) for h in hex_str.split())
    return b.decode("utf-8")


def to_binary(text: str) -> str:
    return " ".join(f"{b:08b}" for b in text.encode("utf-8"))


def from_binary(bin_str: str) -> str:
    b = bytes(int(chunk, 2) for chunk in bin_str.split())
    return b.decode("utf-8")


def to_b64(text: str) -> str:
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def from_b64(b64_str: str) -> str:
    return base64.b64decode(b64_str.strip()).decode("utf-8")


# ---------------------------------------------------------------------------
# 6. USO DE SALT
# ---------------------------------------------------------------------------

def random_salt(length: int = 8) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))


def salted_hashes(password: str, algo: str, n_salts: int = 3):
    """Genera n_salts salts aleatorios distintos y su hash correspondiente."""
    results = []
    for _ in range(n_salts):
        salt = random_salt()
        h = hash_text(password + salt, algo)
        results.append((salt, h))
    return results
