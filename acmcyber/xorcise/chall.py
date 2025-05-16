import random

FLAG = "cyber{REDACTED}"
KEY = "??????"

def enc(data: str, key: str) -> str:
    output = []
    for i, ch in enumerate(data):
        output.append(ord(ch) ^ ord(key[i % len(key)]))
    return bytes(output).hex()

ciphertext = enc(FLAG, KEY)
# print(ciphertext)  # 5c465d5a4d44530f4b4c605059604d5a4f0a42

def dec(hex_data: str, key: str) -> str:
    # Convert the hex string back to bytes
    encrypted_bytes = bytes.fromhex(hex_data)
    output = []
    
    # XOR each byte with the key to recover the original characters
    for i, byte in enumerate(encrypted_bytes):
        output.append(chr(byte ^ ord(key[i % len(key)])))
    
    return ''.join(output)

key = "cyber{"
msg = "5c465d5a4d44530f4b4c605059604d5a4f0a42"
print(dec(msg, key))