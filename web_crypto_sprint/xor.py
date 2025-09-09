from pwn import xor

msg = b"dukeCTF{x0r_15_v3ry_1mp0rt4nt_1n_crypt0}"
key = b"i_<3_x0r"

ct = bytes.hex(xor(msg, key))
print(f"Ciphertext: {ct}")

# Solution
ct = bytes.fromhex(ct)
tag = b"dukeCTF{"

def xor_it(ct, tag):
    key = ''
    for i in range(len(tag)):
        key += chr(ct[i] ^ tag[i])
    return key.encode()

key = xor_it(ct, tag)
print(f"Flag: {xor(ct, key).decode()}")
