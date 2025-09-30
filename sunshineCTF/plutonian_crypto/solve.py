from pwn import remote
from binascii import unhexlify

HOST = "chal.sunshinectf.games"
PORT = 25403

BLOCK_SIZE = 16
MESSAGE_LEN = 592       # from ciphertext length
NUM_BLOCKS = MESSAGE_LEN // BLOCK_SIZE  # 37 blocks

# Known prefix
KNOWN_PLAINTEXT = b"Greetings, Earthlings."  # 22 bytes
PT_BLOCK0 = KNOWN_PLAINTEXT[:BLOCK_SIZE]     # "Greetings, Earth"
PT_BLOCK1_PART = KNOWN_PLAINTEXT[BLOCK_SIZE:]  # "lings."

def xor_bytes(a: bytes, b: bytes) -> bytes:
    return bytes(x ^ y for x, y in zip(a, b))

def main():
    r = remote(HOST, PORT)
    r.recvuntil(b"== BEGINNING TRANSMISSION ==\n\n")

    # Store keystream blocks
    keystream = [bytearray(BLOCK_SIZE) for _ in range(NUM_BLOCKS + 1)]
    known_mask = [bytearray([0]*BLOCK_SIZE) for _ in range(NUM_BLOCKS + 1)]

    ciphertexts = []

    rounds = 0
    while True:
        line = r.recvline().strip().decode()
        ct = unhexlify(line)
        ciphertexts.append(ct)

        # Split into 16-byte blocks
        blocks = [ct[i:i+BLOCK_SIZE] for i in range(0, len(ct), BLOCK_SIZE)]

        # Recover keystream[C] from first block
        ks0 = xor_bytes(blocks[0], PT_BLOCK0)
        keystream[rounds][:] = ks0
        known_mask[rounds][:] = bytearray([1]*BLOCK_SIZE)

        # Recover first 6 bytes of keystream[C+1]
        ks1_part = xor_bytes(blocks[1][:len(PT_BLOCK1_PART)], PT_BLOCK1_PART)
        keystream[rounds+1][:len(PT_BLOCK1_PART)] = ks1_part
        known_mask[rounds+1][:len(PT_BLOCK1_PART)] = bytearray([1]*len(PT_BLOCK1_PART))

        rounds += 1

        # Stop once we’ve filled all blocks
        if rounds >= NUM_BLOCKS:
            break

    r.close()

    # At this point we should have all keystream blocks filled
    # Decrypt the first ciphertext
    ct0 = ciphertexts[0]
    ct_blocks = [ct0[i:i+BLOCK_SIZE] for i in range(0, len(ct0), BLOCK_SIZE)]

    plaintext_blocks = []
    for i, block in enumerate(ct_blocks):
        ks = bytes(keystream[i])
        pt_block = xor_bytes(block, ks)
        plaintext_blocks.append(pt_block)

    message = b"".join(plaintext_blocks)
    print("[+] Recovered MESSAGE:")
    print(message.decode(errors="ignore"))

if __name__ == "__main__":
    main()

