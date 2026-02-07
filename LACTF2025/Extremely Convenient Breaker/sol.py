from pwn import *

# Connect to the remote challenge
conn = remote("chall.lac.tf", 31180)

# Read the encrypted flag
conn.recvuntil("Here's the encrypted flag in hex: \n")
flag_enc = conn.recvline().strip().decode()

print(f"Encrypted Flag: {flag_enc}")

# Split into 16-byte (32 hex chars) blocks
flag_blocks = [flag_enc[i:i+32] for i in range(0, len(flag_enc), 32)]

decrypted_flag = ""

for block in flag_blocks:
    # Send the same block 4 times
    crafted_payload = (block * 4).encode()

    conn.recvuntil("Enter as hex: ")
    conn.sendline(crafted_payload)
    
    # Receive and extract the first 16 bytes of decrypted text
    decrypted_block = conn.recvline().strip()
    
    # Convert to bytes if needed
    if isinstance(decrypted_block, bytes):
        decrypted_block = decrypted_block[:16]  # Get only the first block
    else:
        decrypted_block = decrypted_block[:16].encode()

    decrypted_flag += decrypted_block.decode(errors="ignore")

print(f"\nDecrypted Flag: {decrypted_flag}")

# Close connection
conn.close()