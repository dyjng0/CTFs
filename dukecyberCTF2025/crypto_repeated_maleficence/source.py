import os
from secret import FLAG


class XOR:

    def __init__(self):
        self.key = os.urandom(5)

    def encrypt(self, msg):
        xored = b''
        for i in range(len(msg)):
            xored += bytes([msg[i] ^ self.key[i % len(self.key)]])
        return xored

    def decrypt(self, data):
        return self.encrypt(data)


if __name__ == '__main__':
    crypto = XOR()
    enc = crypto.encrypt(FLAG)

    with open('encrypted.txt', 'w') as f:
        f.write(enc.hex())
