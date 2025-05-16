# string = '73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d'
# data = bytes.fromhex(string)
# for i in range(256):
#     decrypted = bytes(b ^ i for b in data)
#     try:
#         text = decrypted.decode('ascii')
#         print(text)
#     except UnicodeDecodeError:
#         pass

string = '73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d'
data = bytes.fromhex(string)
for i in range(256):
    ret = "".join(chr(o ^ i) for o in data)
    if (ret.startswith("crypto")):
        print(ret)