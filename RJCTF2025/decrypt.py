# Attempt to recover plaintext from the provided ciphertext using the known 23-char prefix
# (derived from the spec): "WGZLIVELABS PROPRIETARY".
# This implements the constraint/backtracking attack described earlier:
# - try block sizes B in {5,6,7,8,9}
# - for each block, search rot_b (0..94) and position permutations sigma (L! possibilities)
# - enforce a global pi_inv mapping (z -> y) consistency across blocks
# - backtrack to assign every block; accept a full solution if the first 23 chars match the known prefix
#
# Note: This is a general solver; it may take some seconds but should finish for the short ciphertext below.

from itertools import permutations
from collections import defaultdict

ALPH = ''.join(chr(i) for i in range(32, 127))  # 95 printable ASCII chars
def idx(ch): return ord(ch) - 32

ciphertext = "AGZAPRWb5jEh tM4qMLu.#.=xy__yZS_BAyILIl7LF                .L9I>gziKG*-e?VW[NSM"
ciphertext = ciphertext.rstrip('\n')
known_prefix = "th3 t0k3n y0u s33k 1s: "  # 23 chars

# helper: split into blocks of size B
def blocks_for_B(ct, B):
    return [ct[i:i+B] for i in range(0, len(ct), B)]

# Try B values
print("Ciphertext length:", len(ciphertext))
solutions = []

# Main solver: backtracking over blocks to assign consistent pi_inv mapping
def solve_for_B(B, timeout_blocks=None):
    blocks = blocks_for_B(ciphertext, B)
    n_blocks = len(blocks)
    # Which characters of each block correspond to known prefix?
    known_len = len(known_prefix)
    known_block_count = (known_len + B - 1) // B
    
    # We'll attempt to assign every block sequentially, but we require that the first known_len chars match the prefix.
    # State: pi_inv_map: dict z->y, and rev map y->z to prevent collisions.
    pi_inv_map = {}  # z -> y
    rev_map = {}     # y -> z
    
    # Precompute possible permutations for lengths up to B to avoid re-generating many times
    perm_cache = {}
    for L in range(1, B+1):
        perm_cache[L] = list(permutations(range(L)))
    
    # Recursively assign a block index
    def recurse(block_idx, pi_inv_map, rev_map):
        if block_idx >= n_blocks:
            # done; construct plaintext and verify prefix
            plain = []
            for b_idx, CT in enumerate(blocks):
                L = len(CT)
                # try all sigma and rot that are consistent with pi_inv_map to produce plaintext for this block
                assigned = False
                for rot in range(95):
                    for sigma in perm_cache[L]:
                        good = True
                        S = [''] * L
                        for j in range(L):
                            S[sigma[j]] = CT[j]
                        for i in range(L):
                            z = idx(S[i])
                            if z in pi_inv_map:
                                y = pi_inv_map[z]
                                x = (y - rot) % 95
                                # get plaintext char but no further check here
                            # else we could derive y = (idx(plaintext)+rot) but plaintext unknown now
                        # If consistent (we only keep pi_inv constraints), accept this sigma and rot
                        # We don't change mapping here; just accept
                        assigned = True
                        break
                    if assigned: break
                if not assigned:
                    return None  # fail
            # build plaintext using full search per block using current mapping (we may have incomplete mapping, so rebuild with extension)
            # We'll do a full blockwise search again but this time extend mapping greedily
            pi_map = dict(pi_inv_map)
            rev = dict(rev_map)
            plain = []
            for b_idx, CT in enumerate(blocks):
                L = len(CT)
                found = False
                for rot in range(95):
                    for sigma in perm_cache[L]:
                        S = [''] * L
                        for j in range(L):
                            S[sigma[j]] = CT[j]
                        local_new = {}
                        conflict = False
                        for i in range(L):
                            z = idx(S[i])
                            # If mapped already, compute plaintext char
                            if z in pi_map:
                                y = pi_map[z]
                                x = (y - rot) % 95
                                p = ALPH[x]
                            else:
                                # we must pick a y that is unused; but many choices -> try to infer from printable requirement
                                # Here we attempt to infer y by assuming plaintext is printable ascii (always true) -> cannot choose uniquely
                                # So instead we skip extension here unless mapping exists; in practice our earlier prefix assignment should yield full mapping.
                                conflict = True
                                break
                        if conflict:
                            continue
                        # All positions mapped
                        found = True
                        for i in range(L):
                            z = idx(S[i])
                            y = pi_map[z]
                            x = (y - rot) % 95
                            plain.append(ALPH[x])
                        break
                    if found: break
                if not found:
                    return None
            plaintext = ''.join(plain)
            if plaintext.startswith(known_prefix):
                return plaintext
            return None
        
        CT = blocks[block_idx]
        L = len(CT)
        is_known_block = (block_idx < known_block_count)
        # We'll enumerate rot and sigma and try to extend mapping using known plaintext where available.
        for rot in range(95):
            for sigma in perm_cache[L]:
                S = [''] * L
                for j in range(L):
                    S[sigma[j]] = CT[j]
                new_map = dict(pi_inv_map)
                new_rev = dict(rev_map)
                ok = True
                # For positions inside prefix, check mapping to known plaintext
                for i in range(L):
                    global_pos = block_idx * B + i
                    if global_pos < len(known_prefix):
                        p = known_prefix[global_pos]
                        z = idx(S[i])
                        y_needed = (idx(p) + rot) % 95  # since constraint: pi_inv[z] == (idx(p)+rot)%95
                        if z in new_map:
                            if new_map[z] != y_needed:
                                ok = False; break
                        if y_needed in new_rev:
                            if new_rev[y_needed] != z:
                                ok = False; break
                        new_map[z] = y_needed
                        new_rev[y_needed] = z
                if not ok:
                    continue
                # No contradictions for known positions; recurse
                res = recurse(block_idx + 1, new_map, new_rev)
                if res is not None:
                    return res
        return None
    
    return recurse(0, pi_inv_map, rev_map)

# Try each B
for B in range(5, 10):
    print(f"Trying B = {B} ...")
    plaintext = solve_for_B(B)
    if plaintext:
        print("Found plaintext for B =", B)
        print(plaintext)
        solutions.append((B, plaintext))
        break

if not solutions:
    print("No full decryption found that matches the known 23-char prefix for B in 5..9.")
else:
    for B, pt in solutions:
        print("\n=== Solution (B=%d) ===\n%s\n" % (B, pt))
