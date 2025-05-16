from Crypto.Util.number import getPrime, bytes_to_long


def egcd(a, b):
    if b == 0:
        return (a, 1, 0)
    g, y, x = egcd(b, a % b)
    return (g, x, y - (a // b) * x)

def modinv(a, m):
    g, x, _ = egcd(a, m)
    return x % m

flag = "cyber{REDACTED}"
m = bytes_to_long(flag.encode()) 

primes = [?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?]
n = 1
for p in primes:
    n *= p

e = 65537

phi = 1
for p in primes:
    phi *= (p - 1)
d = modinv(e, phi)
c = pow(m, e, n)

print(n)  # 137245185820916084981576187422355231591596471653486503458000808298446161941793009
print(e)  # 65537
print(c)  # 1?222704042040446853044429207188278408939894360823122837186120194600874985169

