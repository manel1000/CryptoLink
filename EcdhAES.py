from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import hashlib
import os

print("Chiffrement hybride ECDH + AES")

# Génération des clés de B
B_private = ec.generate_private_key(
    ec.SECP256R1(),
    default_backend()
)

B_public = B_private.public_key()

print("\nB génère sa paire de clés ECC")

# A génère une clé éphémère
A_private = ec.generate_private_key(
    ec.SECP256R1(),
    default_backend()
)

A_public = A_private.public_key()

print("A génère une clé éphémère")

# Secret partagé ECDH
shared_secret_A = A_private.exchange(ec.ECDH(), B_public)

print("\nA calcule le secret partagé")

# Dérivation AES-256
AES_key = hashlib.sha256(shared_secret_A).digest()

print("Clé AES-256 dérivée")

# Message utilisateur
message = input("\nEntrer le message à chiffrer : ")

# Transformation en bytes
plaintext = message.encode()

# AES CBC
iv = os.urandom(16)

# padding simple
padding_length = 16 - (len(plaintext) % 16)
plaintext += bytes([padding_length]) * padding_length

cipher = Cipher(
    algorithms.AES(AES_key),
    modes.CBC(iv),
    backend=default_backend()
)

encryptor = cipher.encryptor()

ciphertext = encryptor.update(plaintext) + encryptor.finalize()

print("\nMessage chiffré :")
print(ciphertext.hex())

# B recalcule le secret
shared_secret_B = B_private.exchange(ec.ECDH(), A_public)

AES_key_B = hashlib.sha256(shared_secret_B).digest()

print("\nB recalcule la même clé AES")

# Déchiffrement
cipher2 = Cipher(
    algorithms.AES(AES_key_B),
    modes.CBC(iv),
    backend=default_backend()
)

decryptor = cipher2.decryptor()

decrypted = decryptor.update(ciphertext) + decryptor.finalize()

# retirer padding
padding_length = decrypted[-1]
decrypted = decrypted[:-padding_length]

print("\nMessage déchiffré par B :")
print(decrypted.decode())