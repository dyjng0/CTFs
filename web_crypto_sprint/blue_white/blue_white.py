msg = "dukeCTF{duK3_c0l0r5_4r3_blu3_4nd_wh1t3}"
binary = ""
ct = ""
for s in msg:
    binary += format(ord(s), "08b")

for c in binary:
    if c == "1":
        ct += "blue "
    else:
        ct += "white "
# with open("blue_white.txt", "w") as f:
#     f.write(ct)

# Solution
with open("blue_white.txt", "r") as f:
    ct = f.read()
binary = ""
for word in ct.split():
    if word == "white":
        binary += "0"
    else:
        binary += "1"
print(binary)
def binary_to_ascii(binary_str):
    chars = [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]
    text = ''.join(chr(int(c, 2)) for c in chars)
    return text

print(binary_to_ascii(binary))
