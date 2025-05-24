with open("free_flags.txt", "r") as f:
    for line in f:
        flags = line.split()
        for flag in flags:
            content = flag[5:-1]
            print(f"Trying {content}...")
            try:
                hex_int = int(content, 16)
                print("Valid hex flag:", flag)
                exit()
            except ValueError:
                print("Not proper flag", flag)
