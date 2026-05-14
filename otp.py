import os


def xor_bytes(data, key):
    return bytes([d ^ k for d, k in zip(data, key)])


def generate_key(length):
    return os.urandom(length)


def encrypt(message, key):
    return xor_bytes(message.encode(), key)


def decrypt(cipher, key):
    return xor_bytes(cipher, key).decode()


# ===== TEST OTP =====
msg = "voci une longue phrase pour tester le chiffrement de One-Time Pad."
key = generate_key(len(msg))
cipher = encrypt(msg, key)
plain = decrypt(cipher, key)
print("Message  :", msg)
print("Cipher   :", cipher.hex())
print("Decrypted:", plain)
print("OK       :", plain == msg)


# ===== VULNERABILITE : Réutilisation de clé =====
M1 = "attack at dawn, position nord"
M2 = "retreat to base, position sud"
K  = generate_key(len(M1))

C1 = encrypt(M1, K)
C2 = encrypt(M2, K)

xor_cc = xor_bytes(C1, C2)                             
xor_mm = xor_bytes(M1.encode(), M2.encode())             

print("\n--- Réutilisation de clé ---")
print("C1 XOR C2 :", xor_cc.hex())
print("M1 XOR M2 :", xor_mm.hex())
print("Égaux     :", xor_cc == xor_mm)
print("→ L'attaquant obtient M1 XOR M2 sans connaître la clé !")


# ===== CRIB DRAGGING =====
def crib_drag(xor_mm, crib):
    crib_b = crib.encode()
    results = []
    for i in range(len(xor_mm) - len(crib_b) + 1):
        fragment = xor_bytes(xor_mm[i:i+len(crib_b)], crib_b)
        if all(32 <= b < 127 for b in fragment):
            results.append((i, fragment.decode()))
    return results

print("\n--- Crib Dragging ---")
for crib in ["attack", "retreat", "position"]:
    found = crib_drag(xor_cc, crib)
    print(f"crib='{crib}' :", found[:3])




# ===== OBSTACLES PRATIQUES =====
obstacles = [
    "La clé doit être aussi longue que le message",
    "La clé ne doit être utilisée qu'une seule fois",
    "Distribution sécurisée de la clé est difficile",
    "Synchronisation parfaite entre émetteur et récepteur",
    "Stockage de grandes clés coûteux et risqué",
]
print("\n--- Pourquoi l'OTP est inutilisable en pratique ---")
for i, obs in enumerate(obstacles, 1):
    print(f"{i}. {obs}")