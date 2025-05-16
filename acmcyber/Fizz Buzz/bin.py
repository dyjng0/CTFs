f = open("fizzbuzz.txt", "r")
ret1 = ""
for line in f:
    for word in line.split():
        if (word == "fizz"):
            ret1 += "0"
        else:
            ret1 += "1"
print(ret1)