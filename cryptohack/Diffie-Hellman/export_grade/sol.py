from pwn import remote
from json import dumps
from decrypt import decrypt_flag

HOST = "socket.cryptohack.org"
PORT = 13379
r = remote(HOST, PORT)


def force_DH64():
    r.recvuntil(b"Send to Bob: ")
    option = dumps({"supported": ["DH64"]})
    r.sendline(option.encode())
    r.recvuntil(b"Send to Alice: ")
    chosen = dumps({"chosen": "DH64"})
    r.sendline(chosen.encode())
    results = r.recvall()
    return results

a = 1343962867716518639
b = 1423872905964669795
g = 0x2
p = 0xde26ab651b92a129
shared_secret = pow(g, a * b, p)
iv = "6a7e2ea8eb5af317eca6afc5370a41e3"
ciphertext = "502d5eb65736440b8f94a3097e1799f73fe21e43848bede5847c490a73eb91af"
print(decrypt_flag(shared_secret, iv, ciphertext))
