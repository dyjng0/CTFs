from Crypto.Cipher import AES
from collections import defaultdict

ciphertext = "41593455378fed8c3bd344827a193bde7ec2044a3f7a3ca6fb77448e9de55155"
ciphertext = bytes.fromhex(ciphertext)

fourth_powers = [x**4 for x in range(20000)]
LIMIT = 10000

def calculateAB():
    ab_pairs = defaultdict(list)
    for a in range(LIMIT):
        a4 = fourth_powers[a]
        for b in range(a): 
            sum_ab = a4 + fourth_powers[b]
            ab_pairs[sum_ab].append((a, b))
        if a % 1000 == 0:
            print(f"Processed a = {a}")
    return ab_pairs

def matchCD(ab_pairs):
    for c in range(LIMIT):
        c4 = fourth_powers[c]
        for d in range(c):
            sum_cd = c4 + fourth_powers[d] + 17
            if sum_cd in ab_pairs:
                for a, b in ab_pairs[sum_cd]:
                    return a, b, c, d
        if c % 1000 == 0:
            print(f"Processed c = {c}")
    return 0, 0, 0, 0

ab_pairs = calculateAB()
print("All values of ab calculated.")
a, b, c, d = matchCD(ab_pairs)
print(f"Found match: {a, b, c, d}")

cipher = AES.new(f"{a*b*c*d}".zfill(16).encode(), AES.MODE_ECB)
flag = cipher.decrypt(ciphertext)
print(flag)
