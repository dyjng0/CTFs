from pwn import remote
import json
import decrypt


def get_vals(io):
    io.recvuntil(b"Alice: ")
    pub_A = json.loads(io.recvline().decode())
    p, A = pub_A["p"], pub_A["A"]
    io.recvuntil(b"Alice: ")
    pub_AES = json.loads(io.recvline().decode())
    iv, ct = pub_AES["iv"], pub_AES["encrypted"]
    return p, A, iv, ct


def find_SK(io, p, A):
    io.recvuntil(b"parameters: ")
    public = json.dumps({"p": p, "g": A, "A": "0x01"})
    io.sendline(public.encode())
    io.recvuntil(b"Bob says to you: ")
    shared_key = json.loads(io.recvline().decode())["B"]
    return int(shared_key, 16)


def solve(io):
    p, A, iv, ct = get_vals(io)
    shared_secret = find_SK(io, p, A)
    print(decrypt.decrypt_flag(shared_secret, iv, ct))


io = remote("socket.cryptohack.org", 13373)
solve(io)
