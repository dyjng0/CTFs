from Crypto.Util.number import long_to_bytes
from pwn import *
from json import *

HOST = "socket.cryptohack.org"
PORT = 13374

remote(HOST, PORT)

