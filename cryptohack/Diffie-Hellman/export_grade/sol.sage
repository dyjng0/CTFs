modulus = 0xde26ab651b92a129
F = GF(modulus)
g = F(0x2)
A = F(0xbd1d620e0990e4af)
B = F(0x67d8c1bcd4232375)

print(discrete_log(A, g))
print(discrete_log(B, g))
