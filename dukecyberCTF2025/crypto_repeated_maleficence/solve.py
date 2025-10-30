from string import printable
from pwn import xor

ct = bytes.fromhex(
    "720c4103880a2a5c49a3652f304c9b652f324d9865336d488754077349c40b36364b880f25"
)
flag = "HTB{"

for c in printable:
    test_flag = (flag + c).encode()
    key = xor(test_flag, ct[:5])
    decrypted = xor(key, ct)
    print(f"Key: {key} solves for {decrypted}")
