from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

with open("ciphertext.txt", "r") as f:
    ciphertext = f.read().strip()
ciphertext = bytes.fromhex(ciphertext)

with open("key.pem", "rb") as f:
    key = f.read()
key = RSA.import_key(key)
n = key.n
e = key.e

p = 51894141255108267693828471848483688186015845988173648228318286999011443419469
q = 77342270837753916396402614215980760127245056504361515489809293852222206596161
phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)
key = RSA.construct((n, e, d))
cipher = PKCS1_OAEP.new(key)
plaintext = cipher.decrypt(ciphertext)

print(plaintext)
