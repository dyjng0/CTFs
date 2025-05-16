string = 'label'
ret = ''.join(chr(ord(char) ^ 13) for char in string)
print(ret)