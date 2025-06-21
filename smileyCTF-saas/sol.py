from gmpy2 import gcd
from pwn import remote

HOST = "localhost"
PORT = 5000

roots = [1]

r = remote(HOST, PORT)

while len(roots) != 4:
    r.recvuntil(b">>> ")
    print("[+] Sending 1...")
    r.sendline(b"1")
    root = int(r.recvline().decode().strip())
    if root not in roots:
        roots.append(root)
        roots.sort()

e = 0x10001
n = roots[3] + 1
print(f"n = {n}")

p = gcd(n, roots[1] - 1)
q = n // p
print(f"p = {p}")
print(f"q = {q}")

phi = (p - 1) * (q - 1)
d = pow(e, -1, phi)

print("[+] Sending new line...")
r.recvuntil(b">>> ")
r.sendline()
r.recvuntil(b"m = ")

m = int(r.recvline().decode())
print(f"m = {m}")

s = pow(m, d, n)
print(f"[+] Sending {s}...")
r.recvuntil(b">>> ")
r.sendline(str(s).encode())

print("[+] Receiving flag...")
flag = r.recvline().decode()
print(flag)

r.close()
