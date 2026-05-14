from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

message = input("Entrez le message : ").encode()

key = DES3.adjust_key_parity(get_random_bytes(24))

iv = get_random_bytes(8)

cipher = DES3.new(key, DES3.MODE_CBC, iv)

padded_message = pad(message, DES3.block_size)

encrypted_message = cipher.encrypt(padded_message)

print("Clé :", key.hex())
print("IV :", iv.hex())
print("Message chiffré :", encrypted_message.hex())