from itertools import product

ciphertext = "zmafnzymkrgwffbqtmzhgntljxvlkx"
key_chars = "squirrelctf"
max_key_length = 5

def vigenere_decrypt(ciphertext, key):
    decrypted = []
    key_repeated = (key * (len(ciphertext) // len(key) + 1))[:len(ciphertext)]
    for c, k in zip(ciphertext, key_repeated):
        dec_char = (ord(c) - ord(k)) % 26
        decrypted.append(chr(dec_char + ord('a')))
    return ''.join(decrypted)

# Print all possible decryptions for keys of length 1 to max_key_length
for key_length in range(1, max_key_length + 1):
    print(f"\n--- Trying key length: {key_length} ---")
    for key_tuple in product(key_chars, repeat=key_length):
        key = ''.join(key_tuple)
        decrypted = vigenere_decrypt(ciphertext, key)
        if "rand" in decrypted:
            print(f"Key: {key}, Decrypted: {decrypted}")