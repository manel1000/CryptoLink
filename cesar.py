

from collections import Counter

# ---------------------------------------------------------------------------
# Dictionnaire de mots français courants pour validation automatique
# ---------------------------------------------------------------------------
MOTS_FRANCAIS = [
    "le", "la", "les", "de", "du", "des", "un", "une", "et", "en",
    "est", "que", "qui", "dans", "il", "elle", "on", "nous", "vous",
    "pas", "plus", "par", "sur", "avec", "pour", "mais", "bien",
    "tout", "comme", "faire", "avoir", "etre", "message", "secret",
    "texte", "clair", "cryptographie", "information", "securite",
    "proteger", "science", "lettres", "entite", "grace", "entre",
]

# Fréquences des lettres en français 
FREQ_FRANCAIS = {
    'a': 8.15, 'b': 0.97, 'c': 3.15, 'd': 3.73, 'e': 17.39,
    'f': 1.12, 'g': 1.21, 'h': 1.11, 'i': 7.31, 'j': 0.34,
    'k': 0.29, 'l': 5.68, 'm': 2.87, 'n': 7.12, 'o': 5.28,
    'p': 3.02, 'q': 0.99, 'r': 6.64, 's': 8.10, 't': 7.22,
    'u': 6.38, 'v': 1.64, 'w': 0.03, 'x': 0.41, 'y': 0.28, 'z': 0.15
}

IC_FRANCAIS = 0.074
ALPHABET_SIZE = 26




def nettoyer_texte(texte: str) -> str:
    """Garde uniquement les lettres minuscules, ignore espaces et ponctuation."""
    return "".join(c.lower() for c in texte if c.isalpha())


def chiffrer_cesar(texte: str, k: int) -> str:
    """Chiffre texte avec décalage k — ignore espaces et casse."""
    k = k % ALPHABET_SIZE
    propre = nettoyer_texte(texte)
    return "".join(
        chr((ord(c) - ord('a') + k) % ALPHABET_SIZE + ord('A'))
        for c in propre
    )


def dechiffrer_cesar(texte: str, k: int) -> str:
    """Déchiffre texte avec la clé k. Équivalent à chiffrer avec (26 - k)."""
    return chiffrer_cesar(texte, ALPHABET_SIZE - k % ALPHABET_SIZE)


# ---------------------------------------------------------------------------
# 2.  Attaque par force brute
# ---------------------------------------------------------------------------

def score_francais(texte: str) -> int:
    """Compte combien de mots du dictionnaire apparaissent dans le texte."""
    t = texte.lower()
    return sum(t.count(mot) for mot in MOTS_FRANCAIS)


def attaque_force_brute(cryptogramme: str):
    """
    Teste les 26 clés possibles et affiche toutes les déclinaisons.
    Identifie automatiquement la clé la plus probable via le dictionnaire.
    """
    print("=" * 65)
    print("  ATTAQUE PAR FORCE BRUTE — CHIFFRE DE CESAR")
    print("=" * 65)
    print(f"  Cryptogramme : {cryptogramme}\n")

    resultats = []
    for k in range(ALPHABET_SIZE):
        clair = dechiffrer_cesar(cryptogramme, k)
        score = score_francais(clair)
        resultats.append((k, clair, score))
        print(f"  k={k:2d}  ->  {clair[:50]:<50}  [score={score}]")

    resultats.sort(key=lambda x: x[2], reverse=True)
    meilleur_k, meilleur_clair, meilleur_score = resultats[0]

    print("\n" + "-" * 65)
    print(f"  [OK] Cle identifiee automatiquement : k = {meilleur_k}")
    print(f"       Texte dechiffre : {meilleur_clair}")
    print(f"       Score dictionnaire : {meilleur_score}")
    print("=" * 65 + "\n")
    return meilleur_k


# ---------------------------------------------------------------------------
# 3.  Analyse de fréquences — Indice de coïncidence
# ---------------------------------------------------------------------------

def calculer_ic(texte: str) -> float:
    """
    calculer indice de coïncidence d'un texte : IC = sum(n_i*(n_i-1)) / (N*(N-1))
    """
    propre = nettoyer_texte(texte)
    n = len(propre)
    if n < 2:
        return 0.0
    compteur = Counter(propre)
    numerateur = sum(freq * (freq - 1) for freq in compteur.values())
    return numerateur / (n * (n - 1))


def deduire_cle_par_ic(cryptogramme: str) -> int:
    """
    Déduit la clé de César par corrélation des fréquences observées
    avec les fréquences théoriques du français, sans force brute.
    """
    print("=" * 65)
    print("  ANALYSE DE FREQUENCES — INDICE DE COINCIDENCE")
    print("=" * 65)

    propre = nettoyer_texte(cryptogramme)
    ic_crypto = calculer_ic(propre)

    print(f"  IC du cryptogramme  : {ic_crypto:.4f}")
    print(f"  IC du francais (ref): {IC_FRANCAIS:.4f}")
    print(f"  (IC invariant par decalage => on utilise la correlation)\n")

    n = len(propre)
    compteur = Counter(propre)
    freq_obs = [compteur.get(chr(ord('a') + i), 0) / n for i in range(ALPHABET_SIZE)]
    freq_ref = [FREQ_FRANCAIS[chr(ord('a') + i)] for i in range(ALPHABET_SIZE)]

    print(f"  {'k':>4}   {'Correlation':>14}   {'Remarque'}")
    print("  " + "-" * 45)

    meilleur_k = 0
    meilleur_corr = -1

    for k in range(ALPHABET_SIZE):
        corr = sum(freq_obs[(i + k) % ALPHABET_SIZE] * freq_ref[i]
                   for i in range(ALPHABET_SIZE))
        marker = "  <-- meilleur" if corr > meilleur_corr else ""
        if corr > meilleur_corr:
            meilleur_corr = corr
            meilleur_k = k
        print(f"  k={k:2d}   corr={corr:.4f}        {marker}")

    clair_final = dechiffrer_cesar(propre, meilleur_k)
    print("\n" + "-" * 65)
    print(f"  [OK] Cle deduite par IC : k = {meilleur_k}")
    print(f"       Texte dechiffre   : {clair_final}")
    print("=" * 65 + "\n")
    return meilleur_k


# ---------------------------------------------------------------------------
# 4.  Démonstration complète
# ---------------------------------------------------------------------------

def demo():
    print("\n" + "=" * 65)
    print("  DEMONSTRATION — CHIFFRE DE CESAR")
    print("=" * 65 + "\n")

    # Message de 256 octets
    message = (
        "La cryptographie est une science fascinante qui permet de "
        "proteger les informations sensibles contre les regards "
        "indiscrets en transformant un texte clair en cryptogramme "
        "illisible grace a une cle secrete partagee entre les deux "
        "entites qui communiquent de facon securisee et confidentielle."
    )
    while len(message.encode("utf-8")) < 256:
        message += " x"
    message = message.encode("utf-8")[:256].decode("utf-8", errors="ignore")

    k = 13  # ROT13 comme exemple classique

    print(f"  Message original ({len(message.encode())} octets) :")
    print(f"  {message}\n")

    crypto = chiffrer_cesar(message, k)
    print(f"  Cryptogramme (k={k}) :")
    print(f"  {crypto}\n")

    clair = dechiffrer_cesar(crypto, k)
    print(f"  Dechiffre (k={k}) :")
    print(f"  {clair}\n")

    assert nettoyer_texte(message) == clair.lower(), "Erreur : dechiffrement incorrect !"
    print("  [OK] Verification : dechiffrement == message original\n")

    # Force brute
    attaque_force_brute(crypto)

    # Analyse de fréquences
    deduire_cle_par_ic(crypto)


if __name__ == "__main__":
    demo()