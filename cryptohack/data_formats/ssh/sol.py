# ssh-keygen -f bruce_rsa.pub -e -m pem > bruce_rsa.pem

from Crypto.PublicKey import RSA

with open("bruce_rsa.pem", "rb") as f:
    key = RSA.import_key(f.read())
print("Modulus:", key.n)
