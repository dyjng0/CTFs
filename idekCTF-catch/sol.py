from pwn import process
from sage.all import matrix, vector, ZZ


def part_to_matrix(part):
    epart = [int.from_bytes(part[i : i + 2], "big") for i in range(0, len(part), 2)]
    return matrix(ZZ, [[epart[0], epart[1]], [epart[2], epart[3]]])


def find_steps(x, y, mind):
    new_pos = vector(ZZ, [x, y])
    step = [mind[i : i + 8] for i in range(0, 1000, 8)]
    our_mind = b""
    for _ in range(30):
        for part in step:
            part_matrix = part_to_matrix(part)
            try:
                new_pos = part_matrix.solve_right(new_pos, extend=False)
                our_mind = part + our_mind
                break
            except Exception:
                continue
    return our_mind


def solve(io):
    for i in range(20):
        io.recvuntil(b"Cat's hidden mind: ")
        mind = bytes.fromhex(io.recvn(2000).decode())
        io.recvuntil(b"Cat now at: (")
        x = int(io.recvuntil(b", ", drop=True))
        y = int(io.recvuntil(b")", drop=True))
        steps = find_steps(x, y, mind)
        print(f"Iteration: {i} | Steps found: {steps.hex()}")
        io.sendlineafter(b"Path to recall (hex): ", steps.hex().encode())
    io.interactive()


io = process(["python3", "./chall.py"])
solve(io)
