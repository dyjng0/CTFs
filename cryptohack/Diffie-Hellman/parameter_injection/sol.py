import decrypt
from pwn import remote
from json import loads, dumps

HOST = 'socket.cryptohack.org'
PORT = 13371
r = remote(HOST, PORT)


def recv_A():
    r.recvuntil(b'Intercepted from Alice: ')
    pub_A = loads(r.recvline().decode())
    return int(pub_A['p'], 16), int(pub_A['g'], 16), int(pub_A['A'], 16)


def sendrec_B(p, g, A):
    r.recvuntil(b'Send to Bob: ')
    hij_A = dumps({"p": hex(p), "g": hex(g), "A": hex(A)})
    r.sendline(hij_A.encode())
    r.recvuntil(b'Intercepted from Bob: ')
    pub_B = loads(r.recvline().decode())
    return int(pub_B['B'], 16)


def sendrec_A(B):
    r.recvuntil(b'Send to Alice: ')
    hij_B = dumps({'B': hex(B)})
    r.sendline(hij_B.encode())
    r.recvuntil(b'Intercepted from Alice: ')
    ct = loads(r.recvline().decode())
    return ct['iv'], ct['encrypted_flag']


recv_A()
sendrec_B(2, 1, 1)
iv, ciphertext = sendrec_A(1)
shared_secret = 1
print(decrypt.decrypt_flag(shared_secret, iv, ciphertext))
