# import sympy 
from sympy import ntt
  
# sequence 
seq = [15, 21, 13, 44]
  
prime_no = 3 * 2**8 + 1
  
# ntt
transform = ntt(seq, prime_no)
print ("NTT : ", transform)
