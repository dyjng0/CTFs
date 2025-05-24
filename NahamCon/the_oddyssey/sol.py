from pwn import *

HOST = "challenge.nahamcon.com"
PORT = 31240

r = remote(HOST, PORT)

while True:
    print("[*] Waiting for prompt...")
    output = r.recvuntil(b"Press enter to continue...", timeout=5)
    print("[<] Received:")
    print(output.decode(errors='ignore'))

    if b"flag{" in output:
        print("[!] Flag found!")
        print(output.decode(errors='ignore'))
        break

    print("[>] Sending enter...")
    r.sendline(b"")
