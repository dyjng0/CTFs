import random

def faro_shuffle(deck):
    top = deck[:len(deck)//2]
    bottom = deck[len(deck)//2:]
    shuffled = ""
    for i in range(len(deck)//2):
        shuffled += bottom[i]
        shuffled += top[i]
    return shuffled

flag = "REDACTED"
shuffles = random.randint(1, 1000)
enc = flag
for i in range(shuffles):
    enc = faro_shuffle(enc)

# print(enc)
# ld1ukk3e_C9T4Fm{8dl01_nyg0?u}_
