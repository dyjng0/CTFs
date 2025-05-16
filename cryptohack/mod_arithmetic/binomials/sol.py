from math import gcd

data = {}

# Read and parse "data.txt"
with open("data.txt", "r") as file:
    for line in file:
        key, value = line.strip().split("=")
        data[key.strip()] = int(value.strip())

# Compute matrix elements with modular exponentiation
a = pow(2, data["e1"] * data["e2"], data["N"])
b = pow(3, data["e1"] * data["e2"], data["N"])
x = pow(5, data["e1"] * data["e2"], data["N"])
y = pow(7, data["e1"] * data["e2"], data["N"])

# Compute vector B
c1 = pow(data["c1"], data["e2"], data["N"])
c2 = pow(data["c2"], data["e1"], data["N"])

# Define A and B as lists (no NumPy needed)
A = [[a, b], [x, y]]
B = [c1, c2]

def determinant_2x2(A, N):
    """Computes determinant of a 2x2 matrix modulo N."""
    return (A[0][0] * A[1][1] - A[0][1] * A[1][0]) % N

def cramers_modular(A, B, N):
    """Solves Ax = B using Cramer's rule modulo N."""
    
    det_A = determinant_2x2(A, N)

    det_A_inv = pow(det_A, -1, N)  # Compute modular inverse of determinant

    # Compute determinant of A with first column replaced by B
    A1 = [[B[0], A[0][1]], [B[1], A[1][1]]]
    det_A1 = determinant_2x2(A1, N)

    # Compute determinant of A with second column replaced by B
    A2 = [[A[0][0], B[0]], [A[1][0], B[1]]]
    det_A2 = determinant_2x2(A2, N)

    # Compute solution x1 and x2 using modular arithmetic
    x1 = (det_A1 * det_A_inv) % N
    x2 = (det_A2 * det_A_inv) % N

    return [x1, x2]
 
x1, x2 = cramers_modular(A, B, data["N"])
p = gcd(x1, data["N"])
print(p)
print(data["N"] // p)