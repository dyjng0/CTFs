from random import randint
import json

a = 288260533169915 # (a/p) = 1
p = 1007621497415251 # 3 (mod 4) -> (-1/p) = -1

FLAG = b'crypto{????????????????????}'

def encrypt_flag(flag):
    ciphertext = []
    plaintext = ''.join([bin(i)[2:].zfill(8) for i in flag]) # converts letter to binary, pads to 8 bits
    for b in plaintext:
        e = randint(1, p)
        n = pow(a, e, p)
        if b == '1':
            ciphertext.append(n)
        else:
            n = -n % p
            ciphertext.append(n)
    return ciphertext

with open("output.txt", "r") as file:
    ciphertext = json.load(file)

def decrypt_flag(flag):
    plaintext_bin = ""
    plaintext = ""
    for text_enc in ciphertext:
        legendre = pow(text_enc, (p - 1)//2 ,p)
        if legendre == 1:
            plaintext_bin += "1"
        else:
            plaintext_bin += "0"
    for i in range(0, len(plaintext_bin), 8):
        bin_str = plaintext_bin[i:i+8]
        ascii_str = int(bin_str, 2)
        letter = chr(ascii_str)
        plaintext += letter
    return plaintext

print(decrypt_flag(ciphertext))