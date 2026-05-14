import random
import hashlib
from typing import Tuple, Dict

# --- ElGamal Implementation ---

def tester_premier(n: int, k: int = 5) -> bool:
    if n < 2: return False
    if n in (2, 3): return True
    if n % 2 == 0: return False
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def creer_premier(bits: int) -> int:
    while True:
        n = random.getrandbits(bits)
        n |= (1 << (bits - 1)) | 1
        if tester_premier(n):
            return n

def chercher_generateur(p: int) -> int:
    
    facteurs = []
    n = p - 1
    d = 2
    while d * d <= n:
        while n % d == 0:
            facteurs.append(d)
            n //= d
        d += 1
    if n > 1:
        facteurs.append(n)

    facteurs_uniques = list(set(facteurs))

    nb_essais = min(1000, p - 2)
    for _ in range(nb_essais):
        g = random.randrange(2, p)
        est_generateur = True
        for f in facteurs_uniques:
            if pow(g, (p - 1) // f, p) == 1:
                est_generateur = False
                break
        if est_generateur:
            return g

    return 2

def creer_premier_sur(bits: int) -> int:
   
    while True:
        q = creer_premier(bits - 1)
        p = 2 * q + 1
        if tester_premier(p):
            return p

def chercher_generateur_premier_sur(p: int) -> int:
    """Pour un premier sur p = 2q+1, tout g tel que g^2 != 1 et g^q != 1 (mod p) est generateur."""
    q = (p - 1) // 2
    for g in range(2, min(100, p)):
        if pow(g, 2, p) != 1 and pow(g, q, p) != 1:
            return g
    return 2

def algorithme_euclide_etendu(a: int, b: int) -> Tuple[int, int, int]:
   
    if a == 0:
        return b, 0, 1
    pgcd, x1, y1 = algorithme_euclide_etendu(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return pgcd, x, y

def inverse_modulaire(a: int, m: int) -> int:
    """Calcule l'inverse de a modulo m"""
    pgcd, x, _ = algorithme_euclide_etendu(a, m)
    if pgcd != 1:
        raise ValueError(f"L'inverse de {a} mod {m} n'existe pas")
    return (x % m + m) % m

def creer_cles(taille_bits: int = 512) -> Tuple[Dict[str, int], Dict[str, int]]:
    """Genere les cles ElGamal (publique et privee)"""
    print(f"Generation d'un premier de {taille_bits} bits...")

    if taille_bits >= 512:
        p = creer_premier_sur(taille_bits)
        g = chercher_generateur_premier_sur(p)
    else:
        p = creer_premier(taille_bits)
        g = chercher_generateur(p)

    print(f"Premier p ({p.bit_length()} bits): {p}")
    print(f"Generateur g: {g}")

    x = random.randrange(2, p - 1)
    y = pow(g, x, p)

    cle_publique = {'p': p, 'g': g, 'y': y}
    cle_privee   = {'p': p, 'g': g, 'x': x}

    return cle_publique, cle_privee

def chiffrer(message: int, cle_publique: Dict[str, int]) -> Tuple[int, int]:
    """Chiffre un entier avec ElGamal"""
    p, g, y = cle_publique['p'], cle_publique['g'], cle_publique['y']

    if message >= p:
        raise ValueError(f"Le message {message} doit etre inferieur a p={p}")

    k  = random.randrange(2, p - 1)
    c1 = pow(g, k, p)
    c2 = (message * pow(y, k, p)) % p
    return c1, c2

def dechiffrer(chiffre: Tuple[int, int], cle_privee: Dict[str, int]) -> int:
    """Dechiffre un chiffre ElGamal"""
    c1, c2 = chiffre
    p, x   = cle_privee['p'], cle_privee['x']

    s     = pow(c1, x, p)
    s_inv = pow(s, p - 2, p)   # Petit theoreme de Fermat
    return (c2 * s_inv) % p

def chiffrer_texte(texte: str, cle_publique: Dict[str, int]) -> list:
    """Chiffre une chaine caractere par caractere"""
    resultat = []
    for car in texte:
        val = ord(car)
        if val >= cle_publique['p']:
            raise ValueError(f"Caractere '{car}' (valeur {val}) trop grand pour la cle")
        resultat.append(chiffrer(val, cle_publique))
    return resultat

def dechiffrer_texte(chiffres: list, cle_privee: Dict[str, int]) -> str:
    """Dechiffre une liste de chiffres en chaine de caracteres"""
    texte = ""
    for c in chiffres:
        texte += chr(dechiffrer(c, cle_privee))
    return texte

# --- Fonctions de signature numerique ElGamal ---

def hacher_message(message: str) -> int:
    """Hache un message et retourne un entier"""
    return int(hashlib.sha256(message.encode()).hexdigest(), 16)

def signer_texte(message: str, cle_privee: Dict[str, int]) -> Tuple[int, int]:
    """Signe un message texte avec ElGamal. Retourne la paire (r, s)."""
    p, g, x = cle_privee['p'], cle_privee['g'], cle_privee['x']
    m = hacher_message(message) % (p - 1)

    while True:
        k = random.randrange(2, p - 1)
        try:
            r = pow(g, k, p)
            if r == 0:
                continue
            k_inv = inverse_modulaire(k, p - 1)
            s = (k_inv * (m - x * r)) % (p - 1)
            if s != 0:
                return r, s
        except ValueError:
            continue

def verifier_signature_texte(message: str, signature: Tuple[int, int], cle_publique: Dict[str, int]) -> bool:
    """Verifie une signature ElGamal sur un message texte."""
    r, s = signature
    p, g, y = cle_publique['p'], cle_publique['g'], cle_publique['y']

    if not (1 <= r < p) or not (1 <= s < p - 1):
        return False

    m      = hacher_message(message) % (p - 1)
    gauche = pow(g, m, p)
    droite = (pow(y, r, p) * pow(r, s, p)) % p
    return gauche == droite

def signer_entier(message: int, cle_privee: Dict[str, int]) -> Tuple[int, int]:
    """Signe directement un entier (sans hachage). Retourne (r, s)."""
    p, g, x = cle_privee['p'], cle_privee['g'], cle_privee['x']
    m = message % (p - 1)

    while True:
        k = random.randrange(2, p - 1)
        try:
            r = pow(g, k, p)
            if r == 0:
                continue
            k_inv = inverse_modulaire(k, p - 1)
            s = (k_inv * (m - x * r)) % (p - 1)
            if s != 0:
                return r, s
        except ValueError:
            continue

def verifier_signature_entier(message: int, signature: Tuple[int, int], cle_publique: Dict[str, int]) -> bool:
    """Verifie une signature ElGamal sur un entier."""
    r, s = signature
    p, g, y = cle_publique['p'], cle_publique['g'], cle_publique['y']

    if not (1 <= r < p) or not (1 <= s < p - 1):
        return False

    m      = message % (p - 1)
    gauche = pow(g, m, p)
    droite = (pow(y, r, p) * pow(r, s, p)) % p
    return gauche == droite

# Malleabilite ElGamal


def montrer_malleabilite(M1: int, M2: int, cle_publique: Dict[str, int], cle_privee: Dict[str, int]) -> None:
    
    p = cle_publique['p']

    print("\n--- Propriete : E(M1).E(M2) = E(M1*M2 mod p) ---")
    Ca = chiffrer(M1, cle_publique)
    Cb = chiffrer(M2, cle_publique)

    C_produit = ((Ca[0] * Cb[0]) % p, (Ca[1] * Cb[1]) % p)
    resultat  = dechiffrer(C_produit, cle_privee)
    attendu   = (M1 * M2) % p

    print(f"  M1 = {M1}, M2 = {M2}")
    print(f"  M1 * M2 mod p             = {attendu}")
    print(f"  Dechiffrement E(M1).E(M2) = {resultat}")
    print(f"  Verification              : {resultat == attendu}")

    print("\n--- Attaque : forger E(2M) sans connaitre M ni x ---")
    M_secret = 12345
    C        = chiffrer(M_secret, cle_publique)
    print(f"  Chiffre recu : C1={C[0]}, C2={C[1]}")

    C_forge        = (C[0], (2 * C[1]) % p)
    resultat_forge = dechiffrer(C_forge, cle_privee)

    print(f"  Chiffre forge (2*C2 mod p) : C1={C_forge[0]}, C2={C_forge[1]}")
    print(f"  Dechiffrement du forge     = {resultat_forge}")
    print(f"  2 * M_secret mod p         = {(2 * M_secret) % p}")
    print(f"  Forgerie reussie           : {resultat_forge == (2 * M_secret) % p}")




def comparer_tailles() -> None:
    """ RSA-2048 vs ElGamal-2048 — tailles des cles et des chiffres."""
    B = 2048 // 8   # 256 octets

    print(f"\n  RSA-2048     : cle publique ~{B} o | chiffre = {B} o")
    print(f"  ElGamal-2048 : cle publique ~{3*B} o | chiffre = {2*B} o (C1+C2, double de RSA)")
    print(f"\n  => ElGamal produit des chiffres 2x plus grands.")
    print(f"     En pratique on l'utilise pour chiffrer une cle AES, pas les donnees brutes.")



if __name__ == "__main__":
    print("=== Demo ElGamal ===\n")

   
    #                verification D(E(M))=M et non-determinisme
    print("--- Generation des cles & Chiffrement ---")

    TAILLE_CLE = 512
    cle_pub, cle_priv = creer_cles(TAILLE_CLE)

    M = 12345
    print(f"\nMessage original : M = {M}")

    # Premier chiffrement
    c1_a, c2_a = chiffrer(M, cle_pub)
    dechiffre_a = dechiffrer((c1_a, c2_a), cle_priv)
    print(f"\nChiffrement #1 : C1={c1_a}\n                 C2={c2_a}")
    print(f"Dechiffrement  : {dechiffre_a}")
    print(f"D(E(M)) = M    : {M == dechiffre_a}")

    # Deuxieme chiffrement du meme M -> resultat different (non-determinisme)
    c1_b, c2_b = chiffrer(M, cle_pub)
    dechiffre_b = dechiffrer((c1_b, c2_b), cle_priv)
    print(f"\nChiffrement #2 : C1={c1_b}\n                 C2={c2_b}")
    print(f"Dechiffrement  : {dechiffre_b}")
    print(f"D(E(M)) = M    : {M == dechiffre_b}")

    print(f"\nNon-determinisme — chiffres differents : {(c1_a, c2_a) != (c1_b, c2_b)}")
    print("(ElGamal choisit un k aleatoire a chaque appel => chiffres differents)")

    print("\n--- Malleabilite ---")
    montrer_malleabilite(M1=12345, M2=67890, cle_publique=cle_pub, cle_privee=cle_priv)

    print("\n--- Tailles RSA vs ElGamal ---")
    comparer_tailles()

    print("\n--- Signature ---")

    message = 12345
    sig_r, sig_s = signer_entier(message, cle_priv)
    print(f"\nSignature de M={message} : r={sig_r}, s={sig_s}")

    valide = verifier_signature_entier(message, (sig_r, sig_s), cle_pub)
    print(f"Verification signature   : {valide}")

    falsifie = message + 1
    valide_falsifie = verifier_signature_entier(falsifie, (sig_r, sig_s), cle_pub)
    print(f"Message falsifie ({falsifie}) : {valide_falsifie}")

    print("\n--- Signature de chaine ---")
    msg_str = "This is a secret message!"
    print(f"Message : '{msg_str}'")
    str_sig_r, str_sig_s = signer_texte(msg_str, cle_priv)
    valide_str = verifier_signature_texte(msg_str, (str_sig_r, str_sig_s), cle_pub)
    print(f"Verification : {valide_str}")

    chaine_falsifiee = msg_str + "!"
    valide_falsifie_str = verifier_signature_texte(chaine_falsifiee, (str_sig_r, str_sig_s), cle_pub)
    print(f"Chaine falsifiee : {valide_falsifie_str}")
