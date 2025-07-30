from Crypto.Util.number import bytes_to_long
import json
from pwn import remote
from pkcs1 import emsa_pkcs1_v15

HOST = "socket.cryptohack.org"
PORT = 13391
r = remote(HOST, PORT)
r.recvline()


def get_signature():
    message = json.dumps({"option": "get_signature"})
    r.sendline(message.encode())
    signature_json = json.loads(r.recvline().decode("utf8"))
    return int(signature_json["signature"], 16)


def verify(msg, n, e):
    message = json.dumps({"option": "verify", "msg": msg, "N": n, "e": e})
    r.sendline(message.encode())
    verify_json = json.loads(r.recvline().decode("utf8"))
    return verify_json["msg"]


message = "I am Mallory and I own CryptoHack.org"
message_long = bytes_to_long(emsa_pkcs1_v15.encode(message.encode(), 256))
signature = get_signature()
n = signature - message_long

print(verify(message, hex(n), hex(1)))
