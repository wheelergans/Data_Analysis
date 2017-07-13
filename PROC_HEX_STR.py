hexString = 'C0 58 F5 62 02 02 12 BB 0A DE 9C E8 44 AE C2 B7 A7 39 61 2B B0 AD E9 CE 38 4A EC 2F 7A 73 87 12 BB 0C 5E 9C E1 C4 AE C3 17 A7 38 A0 00 00 00 00 00 00'

hexString.replace(' ','')
for 

binStr = bin(int(hexString, scale))[2:].zfill(num_of_bits)
header = int(binStr[0:8],2)
epoch = int(binStr[8:40],2)
battV = int(binStr[40:48],2)
stat = int(binStr[48:56],2)
count_0 = int(binStr[56:62],2)
hs_0 = int(binStr[62:71],2)
