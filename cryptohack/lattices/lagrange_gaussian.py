import numpy as np


def division(v1, v2):
    return int(np.round(np.dot(v1, v2) / np.dot(v1, v1)))


def reduction(v1, v2):
    if np.linalg.norm(v2) < np.linalg.norm(v1):
        v1, v2 = v2, v1
    m = division(v1, v2)
    if m == 0:
        return (v1, v2)
    return reduction(v1, v2 - m * v1)


v1 = np.array([846835985, 9834798552])
v2 = np.array([87502093, 123094980])
r1, r2 = reduction(v1, v2)
print(np.dot(r1, r2))
