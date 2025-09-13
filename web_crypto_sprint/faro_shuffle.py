import random

def perfect_shuffle(deck):
    top = deck[:len(deck)//2]
    bottom = deck[len(deck)//2:]
    shuffled = ""
    for i in range(len(deck)//2):
        shuffled += bottom[i]
        shuffled += top[i]
    return shuffled

def inverse_shuffle(deck):
    # Undo the perfect shuffle
    top = []
    bottom = []
    for i in range(0, len(deck), 2):
        bottom.append(deck[i])
        top.append(deck[i+1])
    return "".join(top + bottom)

# Encryption
flag = "dukeCTF{d0_y0u_l1k3_94m8l1ng?}"
shuffles = random.randint(1, 1000)
enc = flag
for i in range(shuffles):
    enc = perfect_shuffle(enc)

print("Encrypted:", enc, "after", shuffles, "shuffles")
:# ld1ukk3e_C9T4Fm{8dl01_nyg0?u}_


# Decryption
dec = enc
for i in range(shuffles):
    dec = inverse_shuffle(dec)

print("Decrypted:", dec)

