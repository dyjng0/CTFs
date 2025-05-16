# key1 = int('a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313', 16)
# xor1 = int('37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e', 16)
# key2 = xor1 ^ key1
# xor2 = int('c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1', 16)
# key3 = key2 ^ xor2
# xor3 = int('04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf', 16)
# # flag = xor3 ^ key2 ^ key3 ^ key1
# flag = xor3 ^ xor2 ^ key1
# flag = hex(flag)[2:]
# flag = bytes.fromhex(flag)
# print(flag)

from pwn import xor
key1 = bytes.fromhex('a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313')
xor2 = bytes.fromhex('c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1')
flag = bytes.fromhex('04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf')
flag = xor(flag, key1, xor2)
print(flag)