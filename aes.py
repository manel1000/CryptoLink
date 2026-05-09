
import os, time
import numpy as np
import matplotlib.pyplot as plt
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

OUT = "/home/claude/tp_crypto/output"
os.makedirs(OUT, exist_ok=True)

# Image synthétique structurée (fuite ECB visible)
def make_image(n=256):
    img = np.zeros((n, n), dtype=np.uint8)
    for r in range(0, n, n//4):
        for c in range(0, n, n//4):
            img[r:r+n//4, c:c+n//4] = (r + c) % 256
    return img

# ── 1. Modes ECB / CBC / CTR ─────────────────────────────
def task1():
    img = make_image()
    raw = img.tobytes()
    k128, k256, iv, nonce = get_random_bytes(16), get_random_bytes(32), get_random_bytes(16), get_random_bytes(8)

    enc_ecb = AES.new(k128, AES.MODE_ECB).encrypt(pad(raw, 16))
    enc_cbc = AES.new(k256, AES.MODE_CBC, iv=iv).encrypt(pad(raw, 16))
    enc_ctr = AES.new(k256, AES.MODE_CTR, nonce=nonce).encrypt(raw)

    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    for ax, data, title in zip(axes,
        [img, enc_ecb, enc_cbc, enc_ctr],
        ["Original", "AES-128-ECB\n(fuite visible !)", "AES-256-CBC", "AES-256-CTR"]):
        ax.imshow(np.frombuffer(data, np.uint8)[:256*256].reshape(256,256), cmap="gray")
        ax.set_title(title); ax.axis("off")
    plt.tight_layout()
    plt.savefig(f"{OUT}/task1_modes.png", dpi=120); plt.close()
    print("Tâche 1 ✔  →", f"{OUT}/task1_modes.png")
    print("  ECB : blocs identiques → chiffrés identiques → motif révélé.")
    print("  CBC / CTR : sortie aléatoire, aucune structure visible.")

# ── 2. Avalanche CBC (flip 1 bit IV) ─────────────────────
def task2():
    key = get_random_bytes(32)
    pt  = os.urandom(256)
    iv  = get_random_bytes(16)
    iv2 = bytes([iv[0] ^ 1]) + iv[1:]     # 1 bit flippé

    c1 = AES.new(key, AES.MODE_CBC, iv=iv ).encrypt(pad(pt, 16))
    c2 = AES.new(key, AES.MODE_CBC, iv=iv2).encrypt(pad(pt, 16))

    rates = [sum(bin(a^b).count('1') for a,b in zip(c1[i*16:(i+1)*16], c2[i*16:(i+1)*16])) / 128 * 100
             for i in range(len(c1)//16)]

    plt.figure(figsize=(9, 4))
    plt.bar(range(len(rates)), rates)
    plt.axhline(50, color='r', linestyle='--', label='~50% attendu')
    plt.xlabel("Bloc"); plt.ylabel("Bits différents (%)"); plt.legend()
    plt.title("Avalanche CBC — 1 bit flippé dans IV")
    plt.tight_layout()
    plt.savefig(f"{OUT}/task2_avalanche.png", dpi=120); plt.close()
    print(f"Tâche 2 ✔  moyenne={sum(rates)/len(rates):.1f}%  →  {OUT}/task2_avalanche.png")
    print("  1 bit modifié dans IV propage l'erreur sur tous les blocs (~50%).")

# ── 3. Nonce-reuse CTR ────────────────────────────────────
def task3():
    key, nonce = get_random_bytes(32), get_random_bytes(8)
    M1 = b"Message secret numero un!!!!!!"
    M2 = b"Autre message aussi confidentiel"

    C1 = AES.new(key, AES.MODE_CTR, nonce=nonce).encrypt(M1)
    C2 = AES.new(key, AES.MODE_CTR, nonce=nonce).encrypt(M2)

    xor_cc = bytes(a^b for a,b in zip(C1, C2))
    xor_mm = bytes(a^b for a,b in zip(M1, M2))
    print(f"Tâche 3 : C1⊕C2 == M1⊕M2 → {xor_cc == xor_mm}")
    # Récupérer M2 en connaissant M1
    M2_rec = bytes(a^b for a,b in zip(xor_cc, M1))
    print(f"  M2 récupéré : {M2_rec}")
    print(f"  Correct      : {M2_rec == M2}")
    print("  → Réutiliser un nonce expose le XOR des clairs. JAMAIS de nonce identique !")

# ── 4. Performance AES-128/192/256 sur 10 Mo ─────────────
def task4():
    data = os.urandom(10 * 1024 * 1024)
    iv   = get_random_bytes(16)
    results = []
    for bits, klen in [(128,16),(192,24),(256,32)]:
        key = get_random_bytes(klen)
        t   = time.perf_counter()
        AES.new(key, AES.MODE_CBC, iv=iv).encrypt(pad(data, 16))
        dt  = time.perf_counter() - t
        results.append((f"AES-{bits}", 10/dt))
        print(f"  AES-{bits}: {dt*1000:.0f} ms  →  {10/dt:.1f} Mo/s")

    plt.bar([r[0] for r in results], [r[1] for r in results])
    plt.ylabel("Mo/s"); plt.title("Débit AES-128/192/256 sur 10 Mo")
    plt.tight_layout()
    plt.savefig(f"{OUT}/task4_perf.png", dpi=120); plt.close()
    print(f"Tâche 4 ✔  →  {OUT}/task4_perf.png")
    print("  AES-128 plus rapide (10 tours vs 14). Sécurité suffisante en pratique.")

# ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Tâche 1 : Modes ECB/CBC/CTR ==="); task1()
    print("\n=== Tâche 2 : Avalanche CBC ===");    task2()
    print("\n=== Tâche 3 : Nonce-reuse CTR ===");  task3()
    print("\n=== Tâche 4 : Performances ===");     task4()