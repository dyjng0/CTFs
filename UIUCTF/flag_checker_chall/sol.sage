modulus = 0xffffff2f
F = GF(modulus)
test_pt = [F(x) for x in [0x2265b1f5, 0x91b7584a, 0xd8f16adf, 0xcd613e30, 0xc386bbc4, 0x1027c4d1, 0x414c343c, 0x1e2feb89]]
test_ct = [F(x) for x in [0xdc44bf5e, 0x5aff1cec, 0xe1e9b4c2, 0x01329b92, 0x8f9ca92a, 0x0e45c5b4, 0x604a4b91, 0x7081eb59]]

for i in range(len(test_pt)):
    print(discrete_log(test_ct[i], test_pt[i]))
