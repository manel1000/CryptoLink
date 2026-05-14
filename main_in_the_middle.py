from sympy import isprime

print("Attaque Man-in-the-Middle sur Diffie-Hellman")

p = int(input("Entrer un nombre premier p : "))

while not isprime(p):
    p = int(input("p n'est pas premier. Entrer un autre p : "))

g = int(input("Entrer le générateur g : "))

# Secrets privés
a = int(input("Secret privé de A : "))
b = int(input("Secret privé de B : "))
m = int(input("Secret privé de l'attaquant M : "))

# Clés publiques originales
A = pow(g, a, p)
B = pow(g, b, p)

# Clé publique de l'attaquant
M = pow(g, m, p)

print("\nClé publique de A :", A)
print("Clé publique de B :", B)
print("Clé publique de M :", M)

print("\nM intercepte les échanges...")

# M remplace les clés publiques
fake_for_A = M
fake_for_B = M

print("M envoie", fake_for_A, "à A à la place de B")
print("M envoie", fake_for_B, "à B à la place de A")

# Calcul des clés secrètes
K_A = pow(fake_for_A, a, p)
K_B = pow(fake_for_B, b, p)

# L'attaquant calcule aussi les clés
K_MA = pow(A, m, p)
K_MB = pow(B, m, p)

print("\nClé calculée par A :", K_A)
print("Clé calculée par B :", K_B)

print("\nClé de M avec A :", K_MA)
print("Clé de M avec B :", K_MB)

if K_A == K_MA:
    print("\nM partage bien la même clé avec A")

if K_B == K_MB:
    print("M partage bien la même clé avec B")