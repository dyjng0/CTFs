from Crypto.Util.number import long_to_bytes
from pwn import remote
import json

HOST = "socket.cryptohack.org"
PORT = 13374
r = remote(HOST, PORT)
r.recvline()


def get_pubkey():
    message = json.dumps({"option": "get_pubkey"})
    r.sendline(message.encode())
    pubkey = json.loads(r.recvline().decode("utf8"))
    return int(pubkey["N"], 16), int(pubkey["e"], 16)


def get_secret():
    message = json.dumps({"option": "get_secret"})
    r.sendline(message.encode())
    secret_json = json.loads(r.recvline().decode("utf8"))
    return secret_json["secret"]


def sign(msg):
    message = json.dumps({"option": "sign", "msg": msg})
    r.sendline(message.encode())
    msg_json = json.loads(r.recvline().decode("utf8"))
    return int(msg_json["signature"], 16)


secret = get_secret()
print(long_to_bytes(sign(secret)))
