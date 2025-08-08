from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import hashlib


def is_pkcs7_padded(message):
    padding = message[-message[-1] :]
    return all(padding[i] == len(padding) for i in range(0, len(padding)))


def decrypt_flag(shared_secret: int, iv: str, ciphertext: str):
    # Derive AES key from shared secret
    sha1 = hashlib.sha1()
    sha1.update(str(shared_secret).encode("ascii"))
    key = sha1.digest()[:16]
    # Decrypt flag
    ciphertext = bytes.fromhex(ciphertext)
    iv = bytes.fromhex(iv)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(ciphertext)

    if is_pkcs7_padded(plaintext):
        return unpad(plaintext, 16).decode("ascii")
    else:
        return plaintext.decode("ascii")


# shared_secret = 0x929cca8
# iv = "4377f94f9624b9c35fcb5eae214a3002" 
# ciphertext = "abcfc4f926c20aa1d18303e5de7d8b20144c5afd3d3df89f5219d9b32f283a7823832b79cc45cc34d1f93183a872bdf854da25082375d0ffe7c71e1be69d55b4138451d7dfd7db7ad59d5453be1fc908"
# 
# print(decrypt_flag(shared_secret, iv, ciphertext))
