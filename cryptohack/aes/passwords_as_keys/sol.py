from Crypto.Cipher import AES
import hashlib

ciphertext = 'c92b7734070205bdf6c0087a751466ec13ae15e6f1bcdd3f3a535ec0f4bbae66'
ciphertext = bytes.fromhex(ciphertext)

with open('words.txt') as f:
    words = [w.strip() for w in f.readlines()]
keys = [hashlib.md5(word.encode()).digest() for word in words]


for key in keys:
    cipher = AES.new(key, AES.MODE_ECB)
    try:
        decrypted = cipher.decrypt(ciphertext)
        if decrypted.startswith(b'crypto{'):
            print(decrypted)
            break
    except ValueError as e:
        print(f"error: {str(e)}")
