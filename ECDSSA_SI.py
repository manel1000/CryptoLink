from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization

print("Simulation échange sécurisé avec ECDH et ECDSA")

A_private = ec.generate_private_key(ec.SECP256R1())
B_private = ec.generate_private_key(ec.SECP256R1())

A_public = A_private.public_key()
B_public = B_private.public_key()

A_bytes = A_public.public_bytes(
    encoding=serialization.Encoding.X962,
    format=serialization.PublicFormat.UncompressedPoint
)

B_bytes = B_public.public_bytes(
    encoding=serialization.Encoding.X962,
    format=serialization.PublicFormat.UncompressedPoint
)

print("\nA envoie sa clé publique :", A_bytes)
print("B envoie sa clé publique :", B_bytes)

print("\nTransmission des clés")
print("A ---> B :", A_bytes)
print("B ---> A :", B_bytes)

A_shared = A_private.exchange(ec.ECDH(), B_public)
B_shared = B_private.exchange(ec.ECDH(), A_public)

print("\nClé partagée de A :", A_shared)
print("Clé partagée de B :", B_shared)

if A_shared == B_shared:
    print("\nÉchange sécurisé réussi")
else:
    print("\nÉchec de l'échange")