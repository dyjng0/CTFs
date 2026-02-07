from math import gcd
from sage.all import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from hashlib import md5

# --- Data ---
APUB = (
    13109366899209289301676180036151662757744653412475893615415990437597518621948,
    5214723011482927364940019305510447986283757364508376959496938374504175747801,
)
BPUB = (
    1970812974353385315040605739189121087177682987805959975185933521200533840941,
    12973039444480670818762166333866292061530850590498312261363790018126209960024,
)
base_point = (
    13187661168110324954294058945757101408527953727379258599969622948218380874617,
    5650730937120921351586377003219139165467571376033493483369229779706160055207,
)
ciphertext_hex = "d345a465538e3babd495cd89b43a224ac93614e987dfb4a6d3196e2d0b3b57d9"


def norm(a, b):
    return a**2 + b**2


def find_p():
    v_a = norm(*APUB) - 1
    v_b = norm(*BPUB) - 1
    v_base = norm(*base_point) - 1
    return gcd(v_a, gcd(v_base, v_b))


if __name__ == "__main__":
    # 1. Recover Prime
    p = find_p()
    print(f"[+] Recovered p: {p}")
    print(f"[+] p bit length: {p.bit_length()}")

    # 2. Setup Field in Sage
    R = PolynomialRing(GF(p), "x")
    x = R.gen()
    K = GF(p**2, modulus=x**2 + 1, names="i")
    i = K.gen()

    # Helper to map (x, y) -> y + x*i (challenge convention)
    def to_complex(coords):
        x_coord, y_coord = coords
        return K(y_coord) + K(x_coord) * i

    # Helper to map back: y + x*i -> (x, y)
    def from_complex(elem):
        poly = elem.polynomial()
        y_coord = int(poly[0])  # Constant term = y
        x_coord = int(poly[1]) if poly.degree() >= 1 else 0  # Coefficient of i = x
        return (x_coord, y_coord)

    G = to_complex(base_point)
    A = to_complex(APUB)
    B = to_complex(BPUB)

    # Verify the mapping works
    print("[*] Verifying mapping...")
    print(f"    Base point: {base_point}")
    print(f"    G in K: {G}")
    G2 = G * G
    G2_coords = from_complex(G2)
    print(f"    2*G back to coords: {G2_coords}")

    # 3. Solve Discrete Log (Alice's Secret)
    print("[*] Solving Discrete Log...")
    try:
        alice_secret = discrete_log(A, G)
        print(f"[+] Alice's Secret: {alice_secret}")
    except Exception as e:
        print(f"[-] DLog failed: {e}")
        exit(1)

    # 4. Calculate Shared Secret
    S_element = B**alice_secret
    S_x, S_y = from_complex(S_element)

    print(f"[+] Shared Secret: ({S_x}, {S_y})")

    # 5. Decrypt
    key_str = f"{S_x},{S_y}"
    key = md5(key_str.encode()).digest()
    cipher = AES.new(key, AES.MODE_ECB)

    try:
        flag = unpad(cipher.decrypt(bytes.fromhex(ciphertext_hex)), 16)
        print(f"\n[SUCCESS] FLAG: {flag.decode()}")
    except Exception as e:
        print(f"[-] Decryption failed: {e}")
