#!/usr/bin/env python3
import struct
from pwn import remote

HOST, PORT = "sunshinectf.games", 25401

# Load the given packet
with open("voyager.bin", "rb") as f:
    data = f.read()

iv, body = data[:16], data[16:]

# Candidates we know from VALID_DEVICES
candidates = {
    0x13371337: "Status Relay",
    0x1337babe: "Ground Station Alpha",
    0xdeadbeef: "Lunar Relay",
}

target_id = 0xdeadbabe

for old_id, name in candidates.items():
    print(f"[+] Trying as if old_id = {hex(old_id)} ({name})")

    old_bytes = struct.pack("<I", old_id)
    new_bytes = struct.pack("<I", target_id)

    iv_list = bytearray(iv)
    for i in range(4):  # patch only first 4 bytes
        iv_list[i] ^= old_bytes[i] ^ new_bytes[i]

    patched_packet = bytes(iv_list) + body

    # Connect and send
    io = remote(HOST, PORT)
    io.recvuntil(b"packet:\n")
    io.send(patched_packet)
    response = io.recvall(timeout=5).decode(errors="ignore")
    io.close()

    print(response)

    if "Restricted Relay" in response or "flag" in response.lower():
        print(f"[+] Got flag with old_id {hex(old_id)} ({name})!")
        break

