from pwn import *
import json
import base64
from Crypto.Util.number import *
import codecs

HOST = "socket.cryptohack.org"
PORT = 13377

r = remote(HOST, PORT)

def json_send(hsh):
    request = json.dumps(hsh).encode()
    r.sendline(request)

def json_recv():
    line = r.readline()
    if not line:
        print("No more data received.")
        return None
    return json.loads(line.decode())

while True:
    response = json_recv()
    if response is None:
        break
    print(response)
    plaintext = ""
    type = response['type']
    ciphertext = response['encoded']
    
    if type == 'base64':
        plaintext = base64.b64decode(ciphertext).decode()
    elif type == 'hex':
        plaintext = bytes.fromhex(ciphertext).decode()
    elif type == 'utf-8':
        for n in ciphertext:
            plaintext += chr(n)
    elif type == 'bigint':
        plaintext = long_to_bytes(int(ciphertext, 16)).decode()
    else:
        plaintext = codecs.decode(ciphertext, 'rot_13')

    print(f"Decoded plaintext: {plaintext}")
    to_send = {
        "decoded": plaintext
    }
    
    json_send(to_send)