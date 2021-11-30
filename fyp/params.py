#Paramters of the proposed algorithm
Q = 12289  #prime number
N = 1024   # power of 2
K = 16     # key size
RecBytes = 256 #length of reconcilation data in bytes
PolyBytes = 192 #PolyBytes is the length of an encoded polynomial in bytes.
SeedBytes = 16
Send_A_Bytes = PolyBytes + SeedBytes #size of Alice public key in bytes
Send_B_Bytes = PolyBytes + RecBytes #size of Bob public key in bytes
