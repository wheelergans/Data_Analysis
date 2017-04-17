hexString = '8058C977F1C3000C0200DC00B90477C0A887AA248C07895D856F4E6FE180001D2E1170FC5917FA1773FD97212BB09DE9CE04'

scale = 16 ## equals to hexadecimal

num_of_bits = 8

binStr = bin(int(hexString, scale))[2:].zfill(num_of_bits)
header = int(binStr[0:8],2)
epoch = int(binStr[8:40],2)
battV = int(binStr[40:48],2)
stat = int(binStr[48:56],2)
count_0 = int(binStr[56:62],2)
hs_0 = int(binStr[62:71],2)
