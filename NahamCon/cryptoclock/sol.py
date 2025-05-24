from pwn import *

HOST = "challenge.nahamcon.com"
PORT = "32377"

r = remote(HOST, PORT)

r.recvuntil(b"The encrypted flag is: ")
encrypted_flag = bytes.fromhex(r.recvline().strip().decode())
flag_length = len(encrypted_flag)

print(f"Encrypted Flag: {encrypted_flag}")
print(f"Flag Length: {flag_length}")

byte_str = b"\x00" * flag_length
print(f"Sending byte string of length {flag_length}...")
r.sendline(byte_str)

r.recvuntil(b"Encrypted: ")
encrypted_bytes = bytes.fromhex(r.recvline().strip().decode())
print(f"Encrypted Byte String: {encrypted_bytes}")

key = xor(byte_str, encrypted_bytes)
print(f"Flag Key: {key}")
r.close()

print("Decrypting flag...")
flag = xor(key, encrypted_flag)
print(flag)
