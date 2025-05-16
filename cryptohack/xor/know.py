string = "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"
string = bytes.fromhex(string)
keys = []
crypto = ['c', 'r', 'y', 'p', 't', 'o', '{']
for i in range(len(crypto)):
    keys.append(chr(string[i] ^ ord(crypto[i])))
print(keys)

keys = ['m', 'y', 'X', 'O', 'R', 'k', 'e', 'y']
res = ""
count = 0
for o in string:
    res += chr(o ^ ord(keys[count % len(keys)]))
    count += 1
print(res)
