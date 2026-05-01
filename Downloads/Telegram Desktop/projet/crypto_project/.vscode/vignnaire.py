from pycipher import Vigenere

# ============================================================
# Chiffre de Vigenère classique avec pycipher
# - Uniquement des lettres A-Z
# - Les espaces et chiffres sont supprimés automatiquement
# - La clé doit contenir uniquement des lettres
# ============================================================

# --- Saisie utilisateur ---
print("=== Chiffre de Vigenère classique ===\n")

print("Que voulez-vous faire ?")
print("1 - Chiffrer")
print("2 - Déchiffrer")
choix = input("Votre choix (1 ou 2) : ").strip()

message = input("Entrez le message : ")
cle     = input("Entrez la clé (lettres uniquement) : ")

# --- Validation de la clé ---
if not cle.isalpha():
    print("❌ Erreur : la clé doit contenir uniquement des lettres.")

else:
    if choix == '1':
        resultat = Vigenere(cle).encipher(message)
        print(f"\n✅ Message chiffré   : {resultat}")

    elif choix == '2':
        resultat = Vigenere(cle).decipher(message)
        print(f"\n✅ Message déchiffré : {resultat}")

    else:
        print("❌ Choix invalide, entrez 1 ou 2.")

