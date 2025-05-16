def checksum(msg):
    c = 0
    for char in msg:
        c += ord(char)
        c = c % 128
    return c

flag = "REDACTED"

my_checksums = []
for i in range(len(flag)):
    my_checksums.append(checksum(flag[:i+1]))

# print(my_checksums)
checked = [99, 92, 62, 35, 21, 16, 89, 56, 47, 20, 2, 118, 85, 68, 58, 31, 17, 115, 98, 67, 53, 25, 120, 103, 85, 52, 40, 16, 117, 84, 55, 31, 4, 103, 82, 69, 58, 39, 26, 121, 93, 70, 42, 24, 12, 107, 52, 49]
msg = ""
total = 0
for num in checked:
    val = num - total
    while val < 0:
        val = val + 128
    msg += chr(val)
    total += val
print(msg)