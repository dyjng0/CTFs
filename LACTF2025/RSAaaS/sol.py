from Crypto.Util.number import isPrime
e = 65537
val = 9223372036859527241

# while True:
#     if (val % e == 0):
#         print(val)
#         break
#     val += 1

while True:
    print(val)
    if (isPrime((val + 1))):
        break
    val += e

# while True:
#     val += 1
#     if (isPrime(val)):
#         print(val)
#         break