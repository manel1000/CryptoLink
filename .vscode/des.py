from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


# CHIFFREMENT 
def chiffrer_ecb(message, key):
    cipher = DES.new(key, DES.MODE_ECB)
    return cipher.encrypt(pad(message, DES.block_size))


def chiffrer_cbc(message, key, iv):
    cipher = DES.new(key, DES.MODE_CBC, iv)
    return cipher.encrypt(pad(message, DES.block_size))


#  DÉCHIFFREMENT
def dechiffrer_ecb(ciphertext, key):
    cipher = DES.new(key, DES.MODE_ECB)
    return unpad(cipher.decrypt(ciphertext), DES.block_size)


def dechiffrer_cbc(ciphertext, key, iv):
    cipher = DES.new(key, DES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), DES.block_size)


# CLÉ 
def saisir_cle():
    while True:
        key = input("Entrez la clé (8 caractères) : ")
        if len(key) == 8:
            return key.encode()
        print(" La clé doit faire exactement 8 caractères")


#  PROGRAMME 
def main():

    print(" DES ECB / CBC (sans fichier) ")

    mode = input("Choisir mode (ecb / cbc) : ").lower()
    action = input("Action (c = chiffrer / d = déchiffrer) : ").lower()
    key = saisir_cle()

    #  ECB 
    if mode == "ecb":

        if action == "c":
            message = input("Message : ").encode()

            ciphertext = chiffrer_ecb(message, key)

            print("\n Chiffrement ECB :")
            print(ciphertext.hex())

        elif action == "d":
            data = bytes.fromhex(input("Ciphertext (hex) : "))

            plaintext = dechiffrer_ecb(data, key)

            print("\n Déchiffrement ECB :")
            print(plaintext.decode())

    #  CBC 
    elif mode == "cbc":

        if action == "c":
            message = input("Message : ").encode()

            iv = get_random_bytes(8)
            ciphertext = chiffrer_cbc(message, key, iv)

            print("\n Chiffrement CBC :")
            print("IV         :", iv.hex())
            print("Ciphertext :", ciphertext.hex())

        elif action == "d":
            iv = bytes.fromhex(input("IV (hex) : "))
            data = bytes.fromhex(input("Ciphertext (hex) : "))

            plaintext = dechiffrer_cbc(data, key, iv)

            print("\n Déchiffrement CBC :")
            print(plaintext.decode())

    else:
        print(" Mode invalide")


if __name__ == "__main__":
    main()