
# import sympy 
from sympy import intt
  
# sequence 
seq = [15, 21, 13, 44]
  
prime_no = 3 * 2**8 + 1
  
# intt
transform = intt(seq, prime_no)
print ("Inverse NTT : ", transform)
