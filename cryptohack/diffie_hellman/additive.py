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


def solve(io):
    p, g, A = A_pubkey(io)
    B = B_pubkey(io)
    iv, ct = A_ciphertext(io)
    io.close()
    g_inv = pow(g, -1, p)
    a = (A * g_inv) % p
    b = (B * g_inv) % p
    shared_secret = g * (a * b) % p
    print(decrypt_flag(shared_secret, iv, ct))
    return


io = remote("socket.cryptohack.org", 13380)
solve(io)
