from pwn import xor

txt = "3b623a0a0f316f16791a0c6f1927440f6f0521340c6f113b0d080742161d0b6f4316174c5e2d791a14492d2a06016f462c4c4d020f"
ct = bytes.fromhex(txt)
tag = b"CRHC{"

def xor_it(ct, tag):
    key = ''
    for i in range(len(tag)):
        key += chr(ct[i] ^ tag[i])
    return key.encode()

key = xor_it(ct, tag)
print(xor(ct, key))
