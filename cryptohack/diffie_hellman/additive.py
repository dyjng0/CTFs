from pwn import remote
import json
from decrypt import decrypt_flag


def A_pubkey(io):
    io.recvuntil(b"Alice: ")
    pub_A = json.loads(io.recvline().decode())
    p, g, A = pub_A["p"], pub_A["g"], pub_A["A"]
    return int(p, 16), int(g, 16), int(A, 16)


def B_pubkey(io):
    io.recvuntil(b"Bob: ")
    pub_B = json.loads(io.recvline().decode())
    B = pub_B["B"]
    return int(B, 16)


def A_ciphertext(io):
    io.recvuntil(b"Alice: ")
    pub_AES = json.loads(io.recvline().decode())
    iv, ct = pub_AES["iv"], pub_AES["encrypted"]
    return iv, ct


def diophantine(a, b, c):
    q = a // b
    r = a % b
    if r == 0:
        return [0, c // b]
    else:
        sol = diophantine(b, r, c)
        u = sol[0]
        v = sol[1]
        return [v, u - q * v]


def solve(io):
    p, g, A = A_pubkey(io)
    B = B_pubkey(io)
    iv, ct = A_ciphertext(io)
    io.close()
    a = diophantine(g, p, A)[0]
    b = diophantine(g, p, B)[0]
    print(a, b)
    shared_secret = g * (a + b) % p
    print(decrypt_flag(shared_secret, iv, ct))
    return


io = remote("socket.cryptohack.org", 13380)
solve(io)
