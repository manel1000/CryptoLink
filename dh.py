import random
from sympy import isprime

print("Diffie-Hellman")

# Entrée de p
p = int(input("Entrer un grand nombre premier p : "))

while not isprime(p):
    p = int(input("p n'est pas premier. Entrer un autre p : "))

# Entrée de g
g = int(input("Entrer le générateur g : "))

# Secrets privés
a = int(input("Entrer le secret privé de A : "))
b = int(input("Entrer le secret privé de B : "))

# Clés publiques
A = pow(g, a, p)
B = pow(g, b, p)

print("\nClé publique de A :", A)
print("Clé publique de B :", B)

# Clé partagée
K_A = pow(B, a, p)
K_B = pow(A, b, p)

print("\nClé calculée par A :", K_A)
print("Clé calculée par B :", K_B)

if K_A == K_B:
    print("\nLa clé partagée K est :", K_A)
else:
    print("\nErreur dans le calcul.")