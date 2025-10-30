from pwn import xor

ct = "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"
ct = bytes.fromhex(ct)

pt = "crypto{"

print(xor(ct, pt)) # myXORke+y

key = "myXORkey"
print(xor(ct, key))


# pt xor key = ct
# pt = ct xor key
# key = pt xor ct
