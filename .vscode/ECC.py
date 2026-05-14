from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
import hashlib

print("Simulation ECDH sur P-256")

# Génération des clés privées
A_private = ec.generate_private_key(
    ec.SECP256R1(),
    default_backend()
)

B_private = ec.generate_private_key(
    ec.SECP256R1(),
    default_backend()
)

print("\nA génère sa clé privée")
print("B génère sa clé privée")

# Génération des clés publiques
A_public = A_private.public_key()
B_public = B_private.public_key()

print("\nA génère sa clé publique")
print("B génère sa clé publique")

# Simulation des échanges
print("\nTransmission des clés publiques")
print("A -----> B : clé publique de A")
print("B -----> A : clé publique de B")

# Calcul du secret partagé
A_shared = A_private.exchange(ec.ECDH(), B_public)
B_shared = B_private.exchange(ec.ECDH(), A_public)

print("\nA calcule le secret partagé")
print(A_shared.hex())

print("\nB calcule le secret partagé")
print(B_shared.hex())

# Vérification
if A_shared == B_shared:
    print("\nLes deux secrets sont identiques")
else:
    print("\nErreur dans le calcul")

# Dérivation AES-256
AES_key = hashlib.sha256(A_shared).digest()

print("\nSHA256 est appliqué au secret partagé")

print("\nClé AES-256 finale")
print(AES_key.hex())