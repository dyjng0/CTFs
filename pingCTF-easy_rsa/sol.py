from Crypto.Util.number import long_to_bytes
import socket
import re
from numpy import gcd

HOST = "localhost"
PORT = 1337

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    
    data = s.recv(4096).decode()
    match = re.search(r"(\d+)", data)
    flag_enc = int(match.group(1))
    
    s.sendall("2\n".encode())
    data = s.recv(4096).decode()
    match = re.search(r"(\d+)", data)
    c1 = int(match.group(1))
    
    s.sendall("4\n".encode())
    data = s.recv(4096).decode()
    match = re.search(r"(\d+)", data)
    c2 = int(match.group(1))
    
    s.sendall("16\n".encode())
    data = s.recv(4096).decode()
    match = re.search(r"(\d+)", data)
    c3 = int(match.group(1))
    
    c12 = c1 ** 2
    c22 = c2 ** 2
    print(gcd(c12 - c2, c22 - c3))