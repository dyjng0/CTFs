import pwn
from Crypto.Util.number import bytes_to_long
import ecdsa

CURVE = ecdsa.curves.BRAINPOOLP512r1
GEN = CURVE.generator
N = CURVE.order


def recover_private_key(z1, z2, s1, s2, r):
    k = ((z1 - z2) * pow(s1 - s2, -1, N)) % N
    priv = (((s1 * k) - z1) * pow(r, -1, N)) % N
    return priv, k


def forge_signature(priv, k, msg):
    z = bytes_to_long(msg)
    rpoint = k * GEN
    r = rpoint.x() % N
    s = (pow(k, -1, N) * (z + r * priv)) % N
    return r, s


def get_challenge(io):
    io.recvuntil(b"Challenge hex:")
    challenge_hex = io.recvline().strip().decode()
    return bytes.fromhex(challenge_hex)


def get_signature(io, msg):
    io.sendlineafter(b"Choose an option:", b"1")
    io.sendlineafter(b"Input hex of message to sign:", msg.hex().encode())
    line = io.recvline().decode()
    r, s = map(int, line.strip().split(": ")[1].split())
    return r, s


def verify_signature(io, msg, r, s):
    io.sendlineafter(b"Choose an option:", b"2")
    io.sendlineafter(b"Input hex of message to verify:", msg.hex().encode())
    io.sendlineafter(
        b"Input the two integers of the signature seperated by a space:",
        f"{r} {s}".encode(),
    )
    return io.recvall().decode()


def perform_nonce_reuse_attack(io, msg1=b"hello", msg2=b"goodbye"):
    print("[+] Requesting signatures for nonce reuse attack...")

    r1, s1 = get_signature(io, msg1)
    r2, s2 = get_signature(io, msg2)

    print("[+] Got signatures:")
    print(f"    (r1, s1) = ({r1}, {s1})")
    print(f"    (r2, s2) = ({r2}, {s2})")

    if r1 != r2:
        raise ValueError("[-] No nonce reuse detected - r values are different")

    print("[+] Nonce reuse detected! Recovering private key...")

    z1 = bytes_to_long(msg1)
    z2 = bytes_to_long(msg2)

    priv, k = recover_private_key(z1, z2, s1, s2, r1)

    print(f"[+] Recovered private key = {priv}")
    print(f"[+] Recovered nonce k = {k}")

    return priv, k


def main(io):
    try:
        challenge = get_challenge(io)
        print(f"[+] Challenge = {challenge.hex()}")

        priv, k = perform_nonce_reuse_attack(io)

        r, s = forge_signature(priv, k, challenge)
        print(f"[+] Forged signature for challenge: (r, s) = ({r}, {s})")

        result = verify_signature(io, challenge, r, s)
        print(result)

    except Exception as e:
        print(f"[-] Attack failed: {e}")
    finally:
        io.interactive()


if __name__ == "__main__":
    io = pwn.remote("challs.watctf.org", 3788)
    main(io)

