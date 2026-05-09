

import math
import numpy as np
from itertools import product as iproduct

MODULO = 26   




def pgcd_etendu(a: int, b: int):
    
    """Retourne le pgcd de a et b, ainsi que les coefficients x, y de Bézout."""
    if b == 0:
        return a, 1, 0
    g, x, y = pgcd_etendu(b, a % b)
    return g, y, x - (a // b) * y


def inverse_modulaire(a: int, m: int = MODULO) -> int:

    """calculer inverse de a mod m via pgcd étendu"""
    g, x, _ = pgcd_etendu(a % m, m)
    if g != 1:
        raise ValueError(f"Pas d'inverse pour {a} mod {m} (pgcd={g})")
    return x % m


def determinant_mod(matrice: list[list[int]], m: int = MODULO) -> int:
    """
    Calcule le déterminant d'une matrice carrée (2×2 ou 3×3) modulo m.
    """
    n = len(matrice)
    if n == 2:
        det = matrice[0][0] * matrice[1][1] - matrice[0][1] * matrice[1][0]
    elif n == 3:
        a = matrice
        det = (
            a[0][0] * (a[1][1]*a[2][2] - a[1][2]*a[2][1])
          - a[0][1] * (a[1][0]*a[2][2] - a[1][2]*a[2][0])
          + a[0][2] * (a[1][0]*a[2][1] - a[1][1]*a[2][0])
        )
    else:
        raise ValueError("Seules les matrices 2×2 et 3×3 sont supportées.")
    return det % m


def matrice_adjointe(matrice: list[list[int]], m: int = MODULO) -> list[list[int]]:
    """
    calcul de la matrice adjointe  d'une matrice carrée 2×2 ou 3×3
    """
    n = len(matrice)
    a = matrice

    if n == 2:
        return [
            [ a[1][1] % m, (-a[0][1]) % m],
            [(-a[1][0]) % m,  a[0][0] % m]
        ]
    elif n == 3:
        adj = [[0]*3 for _ in range(3)]
        for i in range(3):
            for j in range(3):
                
                sous = [
                    [a[r][c] for c in range(3) if c != j]
                    for r in range(3) if r != i
                ]
                mineur = sous[0][0]*sous[1][1] - sous[0][1]*sous[1][0]
                adj[j][i] = ((-1)**(i+j) * mineur) % m
        return adj
    else:
        raise ValueError("Taille non supportée.")


def inverser_matrice_mod(matrice: list[list[int]], m: int = MODULO) -> list[list[int]]:
    """
    Calcule K⁻¹ mod m = det⁻¹ × adj(K) mod m.
    
    """
    det = determinant_mod(matrice, m)
    inv_det = inverse_modulaire(det, m)   
    adj = matrice_adjointe(matrice, m)
    n = len(matrice)
    return [
        [(inv_det * adj[i][j]) % m for j in range(n)]
        for i in range(n)
    ]


def verifier_matrice(matrice: list[list[int]], m: int = MODULO) -> bool:
    """
    Vérifie que la matrice est inversible modulo m en calculant son déterminant
    """
    n = len(matrice)
    det = determinant_mod(matrice, m)
    g = math.gcd(int(det), m)

    print(f"  Vérification matrice {n}×{n} :")
    print(f"    det(K) mod {m} = {det}")
    print(f"    pgcd({det}, {m}) = {g}")

    if g == 1:
        print(f"      Matrice inversible — chiffrement Hill valide.\n")
        return True
    else:
        print(f"      Matrice NON inversible mod {m} — clé invalide !\n")
        return False


# ---------------------------------------------------------------------------
# Conversion texte ↔ blocs numériques
# ---------------------------------------------------------------------------

def texte_vers_blocs(texte: str, taille: int) -> list[list[int]]:
    """
    Nettoie le texte 
    """
    propre = "".join(c.lower() for c in texte if c.isalpha())
    # Compléter (padding) avec 'x' si le dernier bloc est incomplet
    reste = len(propre) % taille
    if reste:
        propre += "x" * (taille - reste)
    return [
        [ord(propre[i+j]) - ord('a') for j in range(taille)]
        for i in range(0, len(propre), taille)
    ]


def blocs_vers_texte(blocs: list[list[int]]) -> str:
    """Reconstruit une chaîne de lettres majuscules depuis les blocs numériques."""
    return "".join(chr(val % MODULO + ord('A')) for bloc in blocs for val in bloc)


# ---------------------------------------------------------------------------
# Chiffrement et déchiffrement Hill
# ---------------------------------------------------------------------------

def _multiplier_bloc(matrice: list[list[int]], bloc: list[int], m: int = MODULO) -> list[int]:
    """Multiplie une matrice n×n par un vecteur de taille n, modulo m."""
    n = len(matrice)
    return [sum(matrice[i][j] * bloc[j] for j in range(n)) % m for i in range(n)]


def chiffrer_hill(texte: str, cle: list[list[int]]) -> str:
    """
    Chiffre `texte` par blocs avec la matrice clé .
    """
    n = len(cle)
    if not verifier_matrice(cle):
        raise ValueError("La matrice clé est invalide (non inversible mod 26).")
    blocs = texte_vers_blocs(texte, n)
    blocs_chiffres = [_multiplier_bloc(cle, bloc) for bloc in blocs]
    return blocs_vers_texte(blocs_chiffres)


def dechiffrer_hill(cryptogramme: str, cle: list[list[int]]) -> str:
    """
    Déchiffre `cryptogramme` en calculant K⁻¹ mod 26 puis en appliquant Hill.
    """
    n = len(cle)
    cle_inverse = inverser_matrice_mod(cle)
    blocs = texte_vers_blocs(cryptogramme, n)
    blocs_clairs = [_multiplier_bloc(cle_inverse, bloc) for bloc in blocs]
    return blocs_vers_texte(blocs_clairs)



# Attaque à clair connu


def attaque_clair_connu_2x2(clair: str, crypto: str) -> list[list[int]]:
    """
    Retrouve la matrice clé 2×2 par attaque à clair connu.
    en va utiliser la nature linéaire du chiffre de Hill : si on connaît deux blocs de clair et leurs correspondants chiffrés,
      on peut former les matrices P et C, puis calculer K = C · P⁻¹ (mod 26).

    """
    print("=" * 65)
    print("  ATTAQUE À CLAIR CONNU — HILL 2×2")
    print("=" * 65)

    blocs_p = texte_vers_blocs(clair, 2)
    blocs_c = texte_vers_blocs(crypto, 2)

    # On prend les deux premiers blocs
    P = [blocs_p[0], blocs_p[1]]   
    C = [blocs_c[0], blocs_c[1]]

    # Transpose : on veut des matrices où chaque colonne est un vecteur
    P_mat = [[P[0][0], P[1][0]], [P[0][1], P[1][1]]]
    C_mat = [[C[0][0], C[1][0]], [C[0][1], C[1][1]]]

    print(f"  Blocs clairs   P : {P}")
    print(f"  Blocs chiffrés C : {C}")

    det_p = determinant_mod(P_mat)
    g = math.gcd(int(det_p), MODULO)
    if g != 1:
        raise ValueError(
            f"La matrice des clairs n'est pas inversible (det={det_p}, pgcd={g}).\n"
            "Choisissez d'autres paires clair/chiffré."
        )

    P_inv = inverser_matrice_mod(P_mat)
    print(f"\n  P_mat  = {P_mat}")
    print(f"  P_inv  = {P_inv}")

    # K = C_mat · P_inv  mod 26
    n = 2
    K_retrouvee = [
        [sum(C_mat[i][k] * P_inv[k][j] for k in range(n)) % MODULO for j in range(n)]
        for i in range(n)
    ]

    print(f"\n  ✔  Clé retrouvée K = {K_retrouvee}")
    print("=" * 65 + "\n")
    return K_retrouvee


def attaque_clair_connu_3x3(clair: str, crypto: str) -> list[list[int]]:
    
    print("=" * 65)
    print("  ATTAQUE À CLAIR CONNU — HILL 3×3")
    print("=" * 65)

    blocs_p = texte_vers_blocs(clair, 3)
    blocs_c = texte_vers_blocs(crypto, 3)

    P = [blocs_p[i] for i in range(3)]
    C = [blocs_c[i] for i in range(3)]

    # Construction des matrices colonnes
    P_mat = [[P[j][i] for j in range(3)] for i in range(3)]
    C_mat = [[C[j][i] for j in range(3)] for i in range(3)]

    print(f"  Blocs clairs P   : {P}")
    print(f"  Blocs chiffrés C : {C}")

    det_p = determinant_mod(P_mat)
    g = math.gcd(int(det_p), MODULO)
    if g != 1:
        raise ValueError(
            f"La matrice des clairs n'est pas inversible (det={det_p}, pgcd={g})."
        )

    P_inv = inverser_matrice_mod(P_mat)

    n = 3
    K_retrouvee = [
        [sum(C_mat[i][k] * P_inv[k][j] for k in range(n)) % MODULO for j in range(n)]
        for i in range(n)
    ]

    print(f"\n  P_mat = {P_mat}")
    print(f"  P_inv = {P_inv}")
    print(f"\n  ✔  Clé retrouvée K = {K_retrouvee}")
    print("=" * 65 + "\n")
    return K_retrouvee




def demo():
    print("\n" + "█" * 65)
    print("  DÉMONSTRATION — CHIFFRE DE HILL")
    print("█" * 65 + "\n")

    # ── Message de 256 octets ───────────────────────────────────────────────
    message = (
        "La cryptographie de Hill utilise des matrices pour chiffrer "
        "des blocs de lettres simultanément ce qui la rend plus robuste "
        "que le chiffre de César face à une analyse de fréquences simple "
        "mais vulnérable à l attaque à clair connu comme nous allons "
        "le démontrer maintenant avec des exemples concrets et détaillés."
    )
    while len(message.encode("utf-8")) < 256:
        message += " x"
    message = message.encode("utf-8")[:256].decode("utf-8", errors="ignore")

    print(f"  Message ({len(message.encode())} octets) :\n  {message}\n")

    # ── Clé 2×2 ─────────────────────────────────────────────────────────────
    cle_2x2 = [[3, 3], [2, 5]]
    print("─" * 65)
    print("  Hill 2×2")
    print("─" * 65)

    crypto_2 = chiffrer_hill(message, cle_2x2)
    print(f"  Cryptogramme : {crypto_2[:60]}...\n")

    clair_2 = dechiffrer_hill(crypto_2, cle_2x2)
    print(f"  Déchiffré    : {clair_2[:60]}...\n")

    original_propre = "".join(c.upper() for c in message if c.isalpha())
    clair_2_propre  = "".join(c for c in clair_2 if c.isalpha())
    assert original_propre == clair_2_propre[:len(original_propre)], \
        "Erreur Hill 2×2 !"
    print("  ✔  Vérification Hill 2×2 OK\n")

    # ── Clé 3×3 ─────────────────────────────────────────────────────────────
    cle_3x3 = [[6, 24, 1], [13, 16, 10], [20, 17, 15]]
    print("─" * 65)
    print("  Hill 3×3")
    print("─" * 65)

    crypto_3 = chiffrer_hill(message, cle_3x3)
    print(f"  Cryptogramme : {crypto_3[:60]}...\n")

    clair_3 = dechiffrer_hill(crypto_3, cle_3x3)
    print(f"  Déchiffré    : {clair_3[:60]}...\n")

    clair_3_propre = "".join(c for c in clair_3 if c.isalpha())
    assert original_propre == clair_3_propre[:len(original_propre)], \
        "Erreur Hill 3×3 !"
    print("  ✔  Vérification Hill 3×3 OK\n")

    # ── Attaque à clair connu 2×2 ────────────────────────────────────────────
    print("─" * 65)
    clair_connu = message[:20]   # Les 20 premières lettres suffisent (≥ 2 blocs)
    K_trouve = attaque_clair_connu_2x2(clair_connu, crypto_2)
    assert K_trouve == cle_2x2, f"Attaque 2×2 échouée : {K_trouve} ≠ {cle_2x2}"
    print("  ✔  Attaque 2×2 : clé originale retrouvée exactement.\n")

    # ── Attaque à clair connu 3×3 ────────────────────────────────────────────
    print("─" * 65)
    K_trouve_3 = attaque_clair_connu_3x3(clair_connu, crypto_3)
    assert K_trouve_3 == cle_3x3, f"Attaque 3×3 échouée : {K_trouve_3} ≠ {cle_3x3}"
    print("  ✔  Attaque 3×3 : clé originale retrouvée exactement.\n")

    

if __name__ == "__main__":
    demo()