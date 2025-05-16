from pwn import *
import hashlib
import binascii
import os

def PRG(s: bytes) -> bytes:
    """ Pseudo-random generator function using SHA3-256. """
    h = hashlib.new("sha3_256")
    h.update(s)
    return h.digest()[:4]  # Output 4 bytes

def xor_bytes(bytes1: bytes, bytes2: bytes) -> bytes:
    """ XOR two byte sequences. """
    return bytes(b1 ^ b2 for b1, b2 in zip(bytes1, bytes2))

# Connect to the challenge server
conn = remote("chall.lac.tf", 31173)

# Read the initial introduction lines
while True:
    line = conn.recvline().decode().strip()
    print(line)
    if "Crypto test #1" in line:
        break  # Stop when the first test begins

number_correct = 0

for i in range(200):
    print(f"\n=== Round {i+1} ===")

    # Read `y` value for this round
    while True:
        line = conn.recvline().decode().strip()
        print(line)
        if "Here's y:" in line:
            y_hex = line.split("Here's y: ")[1].strip()
            y = binascii.unhexlify(y_hex)  # Convert hex to bytes
            break  # Stop when `y` is received

    # Generate a random 2-byte secret
    s = os.urandom(2)
    prg_s = PRG(s)  # Compute PRG output
    prg_s_xor_y = xor_bytes(prg_s, y)  # Compute XOR for beef case

    # Choose the commitment at random
    choice = os.urandom(1)[0] % 2 
    if choice == 0:
        com = prg_s
    else:
        com = prg_s_xor_y

    # Send commitment
    conn.sendline(binascii.hexlify(com).decode())

    # Receive challenge choice (chicken or beef)
    while True:
        line = conn.recvline().decode().strip()
        print(line)
        if "chicken" in line:
            actual_choice = 0
            break
        elif "beef" in line:
            actual_choice = 1
            break

    # Send `s` as decommitment
    conn.sendline(binascii.hexlify(s).decode())

    # Debugging beef cases
    expected_com = PRG(s) if actual_choice == 0 else xor_bytes(PRG(s), y)
    
    print(f"[DEBUG] s: {s.hex()}")
    print(f"[DEBUG] PRG(s): {PRG(s).hex()}")
    print(f"[DEBUG] y: {y.hex()}")
    print(f"[DEBUG] PRG(s) ⊕ y: {xor_bytes(PRG(s), y).hex()}")
    print(f"[DEBUG] com (Sent): {com.hex()}")

    if expected_com != com:
        print("[ERROR] Commitment does not match expected value!")

    # Read result of the round
    while True:
        line = conn.recvline().decode().strip()
        print(line)
        if "Good work" in line:
            number_correct += 1
            break
        elif "Ouch" in line:
            break

# Check final output
final_output = conn.recvall().decode()
print(final_output)

# Print final score
print(f"Final score: {number_correct}/200")
