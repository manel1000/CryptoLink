import pycipher
import re
from math import gcd
from collections import defaultdict, Counter

def chiffrer_vigenere(texte, cle):
    """Chiffre un texte avec Vigenère (pycipher)."""
    # Garder uniquement les lettres, mettre en majuscules
    texte_propre = re.sub(r'[^A-Za-z]', '', texte).upper()
    return pycipher.Vigenere(cle.upper()).encipher(texte_propre)

def dechiffrer_vigenere(texte, cle):
    """Déchiffre un texte avec Vigenère (pycipher)."""
    texte_propre = re.sub(r'[^A-Za-z]', '', texte).upper()
    return pycipher.Vigenere(cle.upper()).decipher(texte_propre)
from math import gcd
from collections import defaultdict, Counter

def trouver_trigrammes_repetes(texte):
    """
    Cherche tous les trigrammes répétés dans le texte (uniquement lettres A-Z).
    Retourne {trigramme: [positions]} pour les trigrammes apparaissant ≥2 fois.
    """
    texte_propre = re.sub(r'[^A-Z]', '', texte.upper())
    trigrammes = defaultdict(list)
    for i in range(len(texte_propre) - 2):
        trig = texte_propre[i:i+3]
        trigrammes[trig].append(i)
    return {t: pos for t, pos in trigrammes.items() if len(pos) >= 2}

def calculer_distances(positions):
    """Retourne les différences entre positions successives."""
    return [positions[i+1] - positions[i] for i in range(len(positions)-1)]

def diviseurs(n):
    """Retourne l'ensemble des diviseurs de n (sauf 1 et n lui-même) jusqu'à une limite."""
    if n < 2:
        return set()
    result = set()
    for d in range(2, min(n//2, 31)):  # on limite à 30 pour les longueurs de clé raisonnables
        if n % d == 0:
            result.add(d)
            if d != n//d and n//d <= 30:
                result.add(n//d)
    return result

def test_kasiski(cryptogramme):
    """
    Applique le test de Kasiski et affiche les résultats.
    """
    print("\n=== TEST DE KASISKI ===")
    trigrammes = trouver_trigrammes_repetes(cryptogramme)
    if not trigrammes:
        print("Aucun trigramme répété trouvé. Impossible d'estimer la clé.")
        return

    print(f"Nombre de trigrammes répétés : {len(trigrammes)}")
    toutes_distances = []
    for trig, pos in trigrammes.items():
        distances = calculer_distances(pos)
        if distances:
            print(f"  '{trig}' : positions {pos} → distances {distances}")
            toutes_distances.extend(distances)

    if not toutes_distances:
        print("Aucune distance calculable.")
        return

    # PGCD de toutes les distances
    pgcd_total = toutes_distances[0]
    for d in toutes_distances[1:]:
        pgcd_total = gcd(pgcd_total, d)
        if pgcd_total == 1:
            break

    print(f"\nPGCD de toutes les distances : {pgcd_total}")

    if pgcd_total > 1:
        # Proposer les diviseurs comme longueurs possibles
        divs = diviseurs(pgcd_total)
        if divs:
            print(f"Longueur(s) de clé probable(s) : {sorted(divs)}")
        else:
            print(f"Longueur de clé probable : {pgcd_total}")
    else:
        # Si PGCD=1, compter la fréquence des diviseurs dans les distances
        compteur = Counter()
        for d in toutes_distances:
            for div in diviseurs(d):
                compteur[div] += 1
        if compteur:
            print("PGCD = 1 → recherche de diviseurs fréquents :")
            for div, freq in compteur.most_common(3):
                print(f"  - longueur {div} apparaît {freq} fois")
        else:
            print("Aucune longueur fiable détectée.")
    print("="*40)
    
    
    ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def indice_coincidence(texte):
    """
    Calcule l'indice de coïncidence d'un texte.
    """
    texte = re.sub(r'[^A-Z]', '', texte.upper())
    n = len(texte)

    if n <= 1:
        return 0

    frequences = Counter(texte)

    somme = sum(f * (f - 1) for f in frequences.values())

    return somme / (n * (n - 1))


def decouper_sous_sequences(texte, k):
    """
    Découpe le texte en k sous-séquences.
    """
    texte = re.sub(r'[^A-Z]', '', texte.upper())

    sous_sequences = ['' for _ in range(k)]

    for i, lettre in enumerate(texte):
        sous_sequences[i % k] += lettre

    return sous_sequences


def trouver_longueur_cle_ic(cryptogramme, max_cle=15):
    """
    Teste plusieurs longueurs de clé avec l'IC.
    """
    print("\n=== ANALYSE PAR IC ===")

    meilleurs = []

    for k in range(1, max_cle + 1):

        sous_seq = decouper_sous_sequences(cryptogramme, k)

        ic_moyen = sum(indice_coincidence(s) for s in sous_seq) / k

        meilleurs.append((k, ic_moyen))

        print(f"Longueur {k:2d} -> IC moyen = {ic_moyen:.4f}")

    meilleurs.sort(key=lambda x: abs(x[1] - 0.074))

    print("\nLongueurs les plus probables :")

    for k, ic in meilleurs[:5]:
        print(f"  - clé longueur {k} (IC={ic:.4f})")

    return meilleurs[0][0]


def lettre_la_plus_frequente(texte):
    """
    Retourne la lettre la plus fréquente.
    """
    freq = Counter(texte)
    return freq.most_common(1)[0][0]


def retrouver_cle_par_frequences(cryptogramme, longueur_cle):
    """
    Retrouve approximativement la clé.
    Hypothèse : la lettre la plus fréquente correspond à E.
    """

    sous_seq = decouper_sous_sequences(cryptogramme, longueur_cle)

    cle = ""

    for s in sous_seq:

        lettre_freq = lettre_la_plus_frequente(s)

        decalage = (ord(lettre_freq) - ord('E')) % 26

        lettre_cle = chr(decalage + ord('A'))

        cle += lettre_cle

    return cle
def main():
    while True:
        print("\n CHIFFRE DE VIGENÈRE ")
        print("1. Chiffrer un message")
        print("2. Déchiffrer un message")
        print("3. Test de Kasiski (estimer longueur de clé)")
        print("4. Analyse par IC")
        print("5. Quitter")
        choix = input("Votre choix : ").strip()

        if choix == '1':
            texte = input("Texte à chiffrer : ")
            cle = input("Clé : ")
            if not cle.isalpha():
                print("Erreur : la clé doit être alphabétique.")
                continue
            print("Résultat :", chiffrer_vigenere(texte, cle))
        elif choix == '2':
            texte = input("Texte à déchiffrer : ")
            cle = input("Clé : ")
            if not cle.isalpha():
                print("Erreur : la clé doit être alphabétique.")
                continue
            print("Résultat :", dechiffrer_vigenere(texte, cle))
        elif choix == '3':
            cryptogramme = input("Entrez le cryptogramme (texte chiffré) : ")
            test_kasiski(cryptogramme)
        elif choix == '4':
            cryptogramme = input("Entrez le cryptogramme : ")

            longueur = trouver_longueur_cle_ic(cryptogramme)

            print(f"\nLongueur probable de la clé : {longueur}")

            cle = retrouver_cle_par_frequences(cryptogramme, longueur)

            print(f"Clé probable : {cle}")

            try:
                texte = dechiffrer_vigenere(cryptogramme, cle)
                print("\nDéchiffrement probable :")
                print(texte)
            except:
                print("Impossible de déchiffrer.")

        elif choix == '5':
            break

    

if __name__ == "__main__":
    main()