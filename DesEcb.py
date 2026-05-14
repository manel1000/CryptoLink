from Crypto.Cipher import DES
from PIL import Image
import numpy as np

# clé DES
key = b"12345678"

# ouvrir image en noir et blanc (64x64)
img = Image.open(r"C:\Users\manel\OneDrive\Images\Screenshots\Capture d'écran 2025-10-27 105451.png").convert("L").resize((64, 64))

pixels = np.array(img).flatten()

cipher = DES.new(key, DES.MODE_ECB)

# DES travaille par blocs de 8 bytes
encrypted = b""

for i in range(0, len(pixels), 8):
    block = bytes(pixels[i:i+8])
    encrypted += cipher.encrypt(block)

# reconstruire image
encrypted_pixels = np.frombuffer(encrypted, dtype=np.uint8)
encrypted_img = encrypted_pixels.reshape((64, 64))

Image.fromarray(encrypted_img).save("ecb_result.png")
Image.fromarray(encrypted_img).show()