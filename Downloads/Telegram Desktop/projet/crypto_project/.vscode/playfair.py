import re

class ChiffrePlayfair:
    """Chiffrement et déchiffrement Playfair (5×5, I=J, X pour doublons/impair)"""
    
    def __init__(self, cle):
        #Étape 1 : nettoyer la clégit remote remove origin
        cle_propre = []
        for c in cle.upper():
            if c == 'J':
                c = 'I'
            if 'A' <= c <= 'Z' and c not in cle_propre:
                cle_propre.append(c)
        
        #Étape 2 : construire la grille 5×5 (25 lettres) 
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"  # sans J
        self.grille = []
        for c in cle_propre:
            self.grille.append(c)
        for c in alphabet:
            if c not in self.grille:
                self.grille.append(c)
        
        # Dictionnaire de recherche rapide des positions
        self.position = {}
        for idx, lettre in enumerate(self.grille):
            ligne = idx // 5
            colonne = idx % 5
            self.position[lettre] = (ligne, colonne)
    
    def _nettoyer_texte(self, texte):
        """Met en majuscules, remplace J par I, enlève tout ce qui n'est pas A-Z"""
        propre = []
        for c in texte.upper():
            if c == 'J':
                c = 'I'
            if 'A' <= c <= 'Z':
                propre.append(c)
        return propre
    
    def _preparer_blocs(self, texte_propre):
        """Insère des 'X' entre lettres doubles et ajoute X si longueur impaire"""
        blocs = []
        i = 0
        while i < len(texte_propre):
            a = texte_propre[i]
            if i + 1 < len(texte_propre):
                b = texte_propre[i + 1]
                if a == b:
                    blocs.append((a, 'X'))
                    i += 1
                else:
                    blocs.append((a, b))
                    i += 2
            else:
                blocs.append((a, 'X'))
                i += 1
        return blocs
    
    def _chiffrer_paire(self, a, b):
        l1, c1 = self.position[a]
        l2, c2 = self.position[b]
        if l1 == l2:
            return (self.grille[l1*5 + (c1+1)%5],
                    self.grille[l2*5 + (c2+1)%5])
        elif c1 == c2:
            return (self.grille[((l1+1)%5)*5 + c1],
                    self.grille[((l2+1)%5)*5 + c2])
        else:
            return (self.grille[l1*5 + c2],
                    self.grille[l2*5 + c1])
    
    def _dechiffrer_paire(self, a, b):
        l1, c1 = self.position[a]
        l2, c2 = self.position[b]
        if l1 == l2:
            return (self.grille[l1*5 + (c1-1)%5],
                    self.grille[l2*5 + (c2-1)%5])
        elif c1 == c2:
            return (self.grille[((l1-1)%5)*5 + c1],
                    self.grille[((l2-1)%5)*5 + c2])
        else:
            return (self.grille[l1*5 + c2],
                    self.grille[l2*5 + c1])
    
    def chiffrer(self, texte_clair):
        propre = self._nettoyer_texte(texte_clair)
        paires = self._preparer_blocs(propre)
        resultat = []
        for a, b in paires:
            ca, cb = self._chiffrer_paire(a, b)
            resultat.append(ca)
            resultat.append(cb)
        return ''.join(resultat)
    
    def dechiffrer(self, texte_chiffre):
        propre = self._nettoyer_texte(texte_chiffre)
        if len(propre) % 2 != 0:
            propre = propre[:-1]  # sécurité
        resultat = []
        for i in range(0, len(propre), 2):
            a = propre[i]
            b = propre[i+1]
            da, db = self._dechiffrer_paire(a, b)
            resultat.append(da)
            resultat.append(db)
        return ''.join(resultat)


# ---------- INTERFACE UTILISATEUR AVEC CHOIX ----------
if __name__ == "__main__":
    print("=== PLAYFAIR - CHIFFREMENT / DÉCHIFFREMENT ===")
    
    while True:
        mode = input("Voulez-vous (c)hiffrer ou (d)échiffrer ? (c/d) : ").lower()
        if mode in ('c', 'd'):
            break
        print("Choix invalide. Entrez 'c' ou 'd'.")
    
    cle = input("Entrez la clé (lettres uniquement) : ")
    
    play = ChiffrePlayfair(cle)   # ← la classe est bien définie ici
    
    if mode == 'c':
        message = input("Entrez le message clair à chiffrer : ")
        resultat = play.chiffrer(message)
        print(f"\nMessage original : {message}")
        print(f"Message chiffré   : {resultat}")
    else:
        texte_chiffre = input("Entrez le texte chiffré à déchiffrer : ")
        resultat = play.dechiffrer(texte_chiffre)
        print(f"\nTexte chiffré : {texte_chiffre}")
        print(f"Texte déchiffré : {resultat}")