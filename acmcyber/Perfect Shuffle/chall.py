import random

def perfect_shuffle(deck):
    top = deck[:len(deck)//2]
    bottom = deck[len(deck)//2:]

    shuffled = ""

    for i in range(len(deck)//2):
        shuffled += bottom[i]
        shuffled += top[i]

    return shuffled

flag = "REDACTED"
shuffles = random.randint(1, 1000)

for i in range(shuffles):
    flag = perfect_shuffle(flag)

print(flag)
# fj_ros__cluu{rhoyyesndeurob_tdi}f_uem_od

