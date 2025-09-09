def checksum(msg):
    c = 0
    for char in msg:
        c += ord(char)
        c = c % 128
    return c

flag = "dukeCTF{why_15_7here_50_much_m47h}"

my_checksums = []
for i in range(len(flag)):
    my_checksums.append(checksum(flag[:i+1]))

# print(my_checksums)
checked = [100, 89, 68, 41, 108, 64, 6, 1, 120, 96, 89, 56, 105, 30, 125, 52, 28, 1, 115, 88, 55, 108, 28, 123, 104, 93, 64, 40, 7, 116, 40, 95, 71, 68]

# solution
msg = ""
total = 0
for num in checked:
    val = num - total
    while val < 0:
        val = val + 128
    msg += chr(val)
    total += val
print(msg)
