import numpy as np


def calc_mu(v1, v2):
    return np.dot(v1, v2) / np.dot(v1, v1)


def proj(v1, v2):
    return calc_mu(v1, v2) * v1


def gs(vectors):
    u = [vectors[0]]
    for i in range(1, len(vectors)):
        temp_v = vectors[i]
        for temp_u in u:
            temp_v = temp_v - proj(temp_u, temp_v)
        u.append(temp_v)
    return u


v = [
    np.array([4, 1, 3, -1]),
    np.array([2, 1, -3, 4]),
    np.array([1, 0, -2, 7]),
    np.array([6, 2, 9, -5]),
]
print(np.array(gs(v)))
