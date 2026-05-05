import math


def inverse_logistic_interval(y_min, y_max):
    """
    Returns the valid [x_min, x_max] intervals that map into [y_min, y_max]
    when applying the logistic map f(x) = 3.9 * x * (1 - x).
    """
    intervals = []
    r = 3.9

    # The absolute peak of the parabola is at y = 0.975
    max_y = 0.25 * r
    if y_min > max_y:
        return intervals

    y_max = min(y_max, max_y)

    # Microscopic epsilon to absorb IEEE-754 float rounding errors
    eps = 1e-14

    # Left curve branch (x <= 0.5)
    try:
        v_min = max(0, 0.25 - y_min / r)
        v_max = max(0, 0.25 - y_max / r)
        x_min = 0.5 - math.sqrt(v_min) - eps
        x_max = 0.5 - math.sqrt(v_max) + eps
        intervals.append((x_min, x_max))
    except ValueError:
        pass

    # Right curve branch (x >= 0.5)
    try:
        v_min = max(0, 0.25 - y_max / r)
        v_max = max(0, 0.25 - y_min / r)
        x_min = 0.5 + math.sqrt(v_min) - eps
        x_max = 0.5 + math.sqrt(v_max) + eps
        intervals.append((x_min, x_max))
    except ValueError:
        pass

    return intervals


def intersect(int1, int2):
    """Finds the overlapping region of two intervals."""
    new_min = max(int1[0], int2[0])
    new_max = min(int1[1], int2[1])
    if new_min <= new_max:
        return (new_min, new_max)
    return None


def solve(ciphertext_file, prefix=b"THJCC{"):
    try:
        with open(ciphertext_file, "rb") as f:
            ciphertext = f.read()
    except FileNotFoundError:
        print(f"[-] Could not find {ciphertext_file}")
        return None

    N = len(prefix)
    K = [ciphertext[i] ^ prefix[i] for i in range(N)]
    print(f"[*] Target keystream prefix: {K}")

    # 1. Start with the interval for the LAST known keystream byte
    valid_intervals = [(K[-1] / 256.0, (K[-1] + 1) / 256.0)]

    # 2. Iterate strictly backwards, projecting the intervals
    for i in range(N - 2, -1, -1):
        target_min = K[i] / 256.0
        target_max = (K[i] + 1) / 256.0

        next_intervals = []
        for y_min, y_max in valid_intervals:
            preimages = inverse_logistic_interval(y_min, y_max)

            # Intersect mathematical preimages with the known byte requirement
            for p_min, p_max in preimages:
                overlap = intersect((p_min, p_max), (target_min, target_max))
                if overlap:
                    next_intervals.append(overlap)

        valid_intervals = next_intervals
        print(f"[*] Step {i}: {len(valid_intervals)} valid interval(s) overlapping.")

        if not valid_intervals:
            print("[-] Interval collapsed! The chaotic map has diverged completely.")
            return None

    print("\n[+] Backward intersection complete!")

    # We now have the tightest possible bounds for x_1. Select the midpoint.
    best_interval = valid_intervals[0]
    best_x1 = (best_interval[0] + best_interval[1]) / 2.0

    print(f"[+] Recovered tight interval for x_1: {best_interval}")
    print(f"[+] Selected precise state x_1: {best_x1}")

    return decrypt_with_x1(ciphertext, best_x1)


def decrypt_with_x1(ciphertext, x1):
    plaintext = bytearray()
    x = x1

    for i, byte in enumerate(ciphertext):
        if i > 0:
            x = 3.9 * x * (1 - x)
        key_byte = int(x * 256) % 256
        plaintext.append(byte ^ key_byte)

    return plaintext


if __name__ == "__main__":
    decrypted = solve("flag.txt.enc", b"THJCC{")
    if decrypted:
        print(f"\n[+] Decrypted Content:\n{decrypted.decode('utf-8', errors='ignore')}")
