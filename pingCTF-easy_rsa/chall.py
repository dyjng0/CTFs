from Crypto.Util.number import getPrime, bytes_to_long
import os 

p = getPrime(1024)
q = getPrime(1024)
n = p*q
e = getPrime(512)
d = pow(e, -1, (p-1)*(q-1))

flag = bytes_to_long(bytes(os.environ["FLAG"], "utf-8"))
encrypted_flag = pow(flag, e, n)

print("Flag ciphertext: ", encrypted_flag)

for i in range(4):
    ciphertext = int(input("Enter ciphertext you want to decrypt: "))
    if ciphertext <= 0 or ciphertext >= n:
        print("0 < ciphertext < n is required!")
        break
    if ciphertext == encrypted_flag:
        print("You serious?")
        break
    print("Your decrypted text: ", pow(ciphertext, d, n))
print("Bye!")