

import hashlib
import os
import random

#  1. Calcul MD5 
def md5_hash(message):
    return hashlib.md5(message).hexdigest()

# 2. Vérifier taille 128 bits 
def verify_size(md5_hex):
    size_bits = len(bytes.fromhex(md5_hex)) * 8
    return size_bits

# 3. Modifier 1 seul bit 
def flip_one_bit(message):

    data = bytearray(message)
    byte_index = random.randint(0, len(data)-1)
    bit_index = random.randint(0, 7)
    data[byte_index] ^= (1 << bit_index)

    return bytes(data)

# ── 4. Comparaison bit à bit ──────────────────────────────
def compare_hashes(h1, h2):

    b1 = bin(int(h1, 16))[2:].zfill(128)
    b2 = bin(int(h2, 16))[2:].zfill(128)
    different_bits = sum(bit1 != bit2 for bit1, bit2 in zip(b1, b2))
    rate = (different_bits / 128) * 100

    return different_bits, rate

# ── 5. Test complet ───────────────────────────────────────
def test_message(message, title):

    print(f"\n===== {title} =====")

    hash1 = md5_hash(message)
    modified_message = flip_one_bit(message)
    hash2 = md5_hash(modified_message)

    print("MD5 original :", hash1)
    print("MD5 modifié  :", hash2)

    print("Taille hash  :", verify_size(hash1), "bits")

    diff, rate = compare_hashes(hash1, hash2)

    print("Bits différents :", diff, "/ 128")
    print(f"Taux avalanche  : {rate:.2f}%")

# ─────────────────────────────────────────────────────────
if __name__ == "__main__":

    # 1. Chaîne vide
    msg1 = b""

    # 2. 1 octet
    msg2 = b"A"

    # 3. 1 Ko
    msg3 = os.urandom(1024)

    # 4. 1 Mo
    msg4 = os.urandom(1024 * 1024)

    # 5. Fichier binaire
    with open("binary_file.bin", "wb") as f:
        f.write(os.urandom(2048))

    with open("binary_file.bin", "rb") as f:
        msg5 = f.read()

    # ── Tests ───────────────────────────────────────────

    test_message(msg1 if len(msg1) > 0 else b"\x00",
                 "Chaîne vide")

    test_message(msg2,
                 "Message 1 octet")

    test_message(msg3,
                 "Message 1 Ko")

    test_message(msg4,
                 "Message 1 Mo")

    test_message(msg5,
                 "Fichier binaire")
