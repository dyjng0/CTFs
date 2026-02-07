from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

key = get_random_bytes(16)

m1 = b"TEST"
m2 = b"flag" # REDACTED


cipher1 = AES.new(key, AES.MODE_CTR, initial_value = 4)
cipher2 = AES.new(key, AES.MODE_CTR, initial_value = 6)

