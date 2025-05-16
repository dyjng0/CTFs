characters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}~_"

flag_enc = "jlT84CKOAhxvdrPQWlWT6cEVD78z5QREBINSsU50FMhv662W"
bigram_enc = []
for i in range(0, len(flag_enc), 2):
    bigram_enc.append(flag_enc[i:i+2])

all = []

for bigram in bigram_enc:
    q1 = characters.find(bigram[0])
    q2 = characters.find(bigram[1])
    q1_inv = pow(q1 + 1, -1, 67)
    q2_inv = pow(q2 + 1, -1, 67)
    p2_cb = (q2 + 1) ** 2 * q1_inv % 67
    poss = []
    for p2 in range(1, 68):
        if (p2 ** 3 % 67 == p2_cb):
            p1 = (q1 + 1) * q2_inv * p2 % 67
            poss.append(characters[p1 - 1] + characters[p2 - 1])
    all.append(poss)

nah = []
not_the_flag = "mCtRNrPw_Ay9mytTR7ZpLJtrflqLS0BLpthi~2LgUY9cii7w"
also_not_the_flag = "PKRcu0l}D823P2R8c~H9DMc{NmxDF{hD3cB~i1Db}kpR77iU"
for i in range(0, len(flag_enc), 2):
    nah.append([not_the_flag[i:i+2], also_not_the_flag[i:i+2]])

flag = ""

for i in range(len(all)):
    for choice in all[i]:
        if (choice not in nah[i]):
            flag += choice

print(flag)