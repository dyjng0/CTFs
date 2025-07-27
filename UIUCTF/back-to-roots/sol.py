from Crypto.Cipher import AES
from hashlib import md5
from gmpy2 import isqrt, square

leak = 0.4336282047950153046404
ct = "7863c63a4bb2c782eb67f32928a1deceaee0259d096b192976615fba644558b2ef62e48740f7f28da587846a81697745"
ct = bytes.fromhex(ct)

lower_bound = isqrt(10 ** 10)
upper_bound = isqrt(10 ** 11)

for i in range(lower_bound, upper_bound):
    K = int(square(i + leak))
    cipher = AES.new(md5(f"{K}".encode()).digest(), AES.MODE_ECB)
    pt_candidate = cipher.decrypt(ct)
    if pt_candidate.startswith(b"uiuctf{"):
        print(pt_candidate)
        break
    if i % 1000 == 0:
          print(f"Testing K = {K}")


