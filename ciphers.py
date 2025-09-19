# ciphers.py
"""
Collection de chiffrements classiques :
- César
- Vigenère
- Atbash
- Playfair
- Hill (2x2)

Conserver ce fichier à la racine du repo CryptoApp/.
Requis: numpy pour Hill.
"""
import string
from typing import List
import numpy as np

ALPHABET = string.ascii_uppercase


# ---------- César ----------
def caesar_encrypt(text: str, shift: int) -> str:
    """Chiffre César — préserve les caractères non alphabétiques."""
    res = []
    for ch in text:
        up = ch.upper()
        if up in ALPHABET:
            idx = (ALPHABET.index(up) + shift) % 26
            # conserve la casse initiale
            res_char = ALPHABET[idx]
            res.append(res_char if ch.isupper() else res_char.lower())
        else:
            res.append(ch)
    return "".join(res)


def caesar_decrypt(text: str, shift: int) -> str:
    return caesar_encrypt(text, -shift)


# ---------- Vigenère ----------
def vigenere_encrypt(text: str, key: str) -> str:
    """Vigenère — la clé/text peuvent contenir lettres; la casse est préservée."""
    if not key:
        raise ValueError("Clé Vigenère vide")
    key_up = "".join([c for c in key.upper() if c.isalpha()])
    if not key_up:
        raise ValueError("Clé Vigenère doit contenir des lettres")
    res = []
    ki = 0
    for ch in text:
        up = ch.upper()
        if up in ALPHABET:
            shift = ALPHABET.index(key_up[ki % len(key_up)])
            idx = (ALPHABET.index(up) + shift) % 26
            out = ALPHABET[idx]
            res.append(out if ch.isupper() else out.lower())
            ki += 1
        else:
            res.append(ch)
    return "".join(res)


def vigenere_decrypt(text: str, key: str) -> str:
    if not key:
        raise ValueError("Clé Vigenère vide")
    key_up = "".join([c for c in key.upper() if c.isalpha()])
    if not key_up:
        raise ValueError("Clé Vigenère doit contenir des lettres")
    res = []
    ki = 0
    for ch in text:
        up = ch.upper()
        if up in ALPHABET:
            shift = ALPHABET.index(key_up[ki % len(key_up)])
            idx = (ALPHABET.index(up) - shift) % 26
            out = ALPHABET[idx]
            res.append(out if ch.isupper() else out.lower())
            ki += 1
        else:
            res.append(ch)
    return "".join(res)


# ---------- Atbash ----------
def atbash_cipher(text: str) -> str:
    res = []
    for ch in text:
        up = ch.upper()
        if up in ALPHABET:
            out = ALPHABET[25 - ALPHABET.index(up)]
            res.append(out if ch.isupper() else out.lower())
        else:
            res.append(ch)
    return "".join(res)


def atbash_encrypt(text: str) -> str:
    return atbash_cipher(text)


def atbash_decrypt(text: str) -> str:
    return atbash_cipher(text)


# ---------- Playfair ----------
def generate_playfair_square(key: str) -> List[str]:
    """
    Retourne la grille 5x5 sous forme de liste de 5 chaînes.
    Remplace J par I (convention classique).
    """
    key_up = "".join(dict.fromkeys((key or "").upper().replace("J", "I")))
    alphabet = "".join([c for c in ALPHABET if c != "J"])
    square = key_up + "".join([c for c in alphabet if c not in key_up])
    return [square[i:i + 5] for i in range(0, 25, 5)]


def playfair_process(text: str) -> str:
    """Prépare le texte (lettres seulement), remplace J->I, insère X si digramme doublon, pad avec X."""
    s = "".join([c for c in (text or "").upper() if c.isalpha()]).replace("J", "I")
    out = ""
    i = 0
    while i < len(s):
        a = s[i]
        b = s[i + 1] if i + 1 < len(s) else "X"
        if a == b:
            out += a + "X"
            i += 1
        else:
            out += a + b
            i += 2
    if len(out) % 2 == 1:
        out += "X"
    return out


def _find_position(square: List[str], ch: str):
    for r, row in enumerate(square):
        if ch in row:
            return r, row.index(ch)
    raise ValueError(f"Char {ch} not in playfair square")


def playfair_encrypt(text: str, key: str) -> str:
    sq = generate_playfair_square(key or "KEY")
    proc = playfair_process(text)
    res = ""
    for i in range(0, len(proc), 2):
        a, b = proc[i], proc[i + 1]
        ra, ca = _find_position(sq, a)
        rb, cb = _find_position(sq, b)
        if ra == rb:
            res += sq[ra][(ca + 1) % 5] + sq[rb][(cb + 1) % 5]
        elif ca == cb:
            res += sq[(ra + 1) % 5][ca] + sq[(rb + 1) % 5][cb]
        else:
            res += sq[ra][cb] + sq[rb][ca]
    return res


def playfair_decrypt(text: str, key: str) -> str:
    sq = generate_playfair_square(key or "KEY")
    s = "".join([c for c in (text or "").upper() if c.isalpha()])
    res = ""
    for i in range(0, len(s), 2):
        a, b = s[i], s[i + 1]
        ra, ca = _find_position(sq, a)
        rb, cb = _find_position(sq, b)
        if ra == rb:
            res += sq[ra][(ca - 1) % 5] + sq[rb][(cb - 1) % 5]
        elif ca == cb:
            res += sq[(ra - 1) % 5][ca] + sq[(rb - 1) % 5][cb]
        else:
            res += sq[ra][cb] + sq[rb][ca]
    return res


# ---------- Hill (2x2) ----------
def _egcd(a: int, b: int):
    if a == 0:
        return (0, 1, b)
    x1, y1, g = _egcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return (x, y, g)


def mod_inverse(a: int, m: int) -> int | None:
    """Inverse modulo m (retourne None si pas inverse)."""
    a = a % m
    x, y, g = _egcd(a, m)
    if g != 1:
        return None
    return x % m


def hill_encrypt(text: str, key_matrix: List[List[int]]) -> str:
    """Hill 2x2 (texte — lettres uniquement). Clé : [[a,b],[c,d]]."""
    mat = np.array(key_matrix, dtype=int) % 26
    if mat.shape != (2, 2):
        raise ValueError("La matrice clé doit être 2x2")
    s = "".join([c for c in (text or "").upper() if c.isalpha()])
    if len(s) % 2 == 1:
        s += "X"
    res = ""
    for i in range(0, len(s), 2):
        vec = np.array([ALPHABET.index(s[i]), ALPHABET.index(s[i + 1])], dtype=int)
        out = mat.dot(vec) % 26
        res += ALPHABET[int(out[0])] + ALPHABET[int(out[1])]
    return res


def hill_decrypt(text: str, key_matrix: List[List[int]]) -> str:
    mat = np.array(key_matrix, dtype=int)
    if mat.shape != (2, 2):
        raise ValueError("La matrice clé doit être 2x2")
    # det entier
    a, b = int(mat[0, 0]), int(mat[0, 1])
    c, d = int(mat[1, 0]), int(mat[1, 1])
    det = (a * d - b * c) % 26
    inv_det = mod_inverse(det, 26)
    if inv_det is None:
        return "Matrice non inversible modulo 26"
    # adjugate for 2x2
    adj = np.array([[d, -b], [-c, a]], dtype=int) % 26
    inv_mat = (inv_det * adj) % 26
    s = "".join([c for c in (text or "").upper() if c.isalpha()])
    if len(s) % 2 == 1:
        s += "X"
    res = ""
    for i in range(0, len(s), 2):
        vec = np.array([ALPHABET.index(s[i]), ALPHABET.index(s[i + 1])], dtype=int)
        out = inv_mat.dot(vec) % 26
        res += ALPHABET[int(out[0])] + ALPHABET[int(out[1])]
    return res
