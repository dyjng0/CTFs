import requests
from string import printable

flag = "crypto{p3n6u1n5"


def encrypt(plaintext):
    r = requests.get(
        f"https://aes.cryptohack.org/ecb_oracle/encrypt/{plaintext.encode().hex()}/"
    )
    ct = r.json()["ciphertext"]
    return ct


def solve(flag):
    block_size = 16
    while True:
        if flag[-1] == "}":
            return flag
        block_index = (len(flag) + 1) // block_size
        pad_len = block_size - (len(flag) % block_size + 1)
        if pad_len == 0:
            offset = "0" * block_size
        else:
            offset = "0" * pad_len
        offset_ct = encrypt(offset)[: 2 * block_size * (block_index + 1)]
        for char in printable:
            guess = flag + char
            print(f"Guessing {guess}...")
            padded_guess = offset + guess
            guess_ct = encrypt(padded_guess)[: 2 * block_size * (block_index + 1)]
            if offset_ct == guess_ct:
                flag = guess
                print(f"Current flag: {flag}")
                break


flag = solve(flag)
print(flag)
