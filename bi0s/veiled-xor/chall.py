from Crypto.Util.number import bytes_to_long, getPrime

n = (p := getPrime(1024)) * (q := getPrime(1024))
print(
    f"n : {n}\nc : {pow(bytes_to_long(flag), 65537, n)}\nVeil XOR: {p ^ int(bin(q)[2:][::-1], 2)}"
)
