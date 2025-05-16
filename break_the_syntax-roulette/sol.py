from pwn import *
import json

# server seeds database
with open("sol-server_seeds.json", "r") as f:
    winning_seeds = json.load(f)

HOST = "localhost"
PORT = 1337

r = remote(HOST, PORT)

streak = 0

while True:
    try:
        # Read server seed hash
        r.recvuntil(b"Server seed hash (verify later): ")
        server_seed_hash = r.recvline().strip().decode()
        print(f"[+] Server seed hash: {server_seed_hash}")

        # Send number from database
        client_seed = winning_seeds[server_seed_hash]
        print(f"[+] Sending: {client_seed}")
        r.recvuntil(b"Enter your client seed (press enter to generate): ")
        r.sendline(str(client_seed).encode())

        # Send 13
        print(f"[+] Sending: 13")
        r.recvuntil(b"Place your bet (number 0-36 or color red/black/green): ")
        r.sendline(b"13")
        
        # Check response
        response = r.recvuntil(b"Verification Details:").decode()
        streak += 1
        print(f"[+] Win #{streak}")
        
        if streak == 37:
                print("[+] Receiving final message:")
                final_output = r.recv().decode()
                print(final_output)
                r.close()
                break

    except EOFError:
        print("[!] Connection closed unexpectedly.")
        break