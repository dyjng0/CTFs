import base64

data_bytes = bytes.fromhex('72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf')
b64 = base64.b64encode(data_bytes)
print(b64)