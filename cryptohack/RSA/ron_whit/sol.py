from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from gmpy2 import gcd

with open("keys_and_messages/21.pem", "r") as f:
    key = RSA.importKey(f.read())
    N = key.n
    E = key.e

with open("keys_and_messages/21.ciphertext", "r") as f:
    CT = f.read()


def readKeys():
    keys = []
    for i in range(1, 51):
        with open(f"keys_and_messages/{i}.pem", "r") as f:
            pub_key = RSA.importKey(f.read()).n
        keys.append(pub_key)
    return keys


def findPrimes(keys):
    primes = set()
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            d = gcd(keys[i], keys[j])
            if d != 1:
                primes.add(d)
                primes.add(keys[i] // d)
                primes.add(keys[j] // d)
    return primes


def factorKey(n, primes):
    for prime in primes:
        if gcd(n, prime) != 1:
            return prime, n // prime
    return n, 1


def decrypt(n, e, p, q, ct):
    phi = (p - 1) * (q - 1)
    d = pow(e, -1, phi)
    key = RSA.construct((n, e, int(d)))
    assert key.has_private()
    cipher = PKCS1_OAEP.new(key)
    plaintext = cipher.decrypt(bytes.fromhex(ct))
    return plaintext


keys = readKeys()
primes = findPrimes(keys)
p, q = factorKey(N, primes)
assert N == p * q
flag = decrypt(N, E, p, q, CT)
print(flag)
