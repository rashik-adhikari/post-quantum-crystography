import params

QINV = 12287   # calculate the quaternion inverse(p, 2^18)/ inverse of modulus
RLOG = 18      # transforms the count data to the log2 scale

"""
it is the process to speed up back-to-back modular multiplication by
transforming the numbers in special forms.
"""

def montgomeryReduce(x):
    u = x * QINV
    u &= (1 << RLOG) - 1
    u *= params.Q
    x += u
    print(x >> 18)
#montgomeryReduce(10)

#it is a fast division algorithm introduced by P.D. Barret in 1998.

def barrettReduce(x):
    u = (x * 5) >> 16
    u *= params.Q
    x -= u
    print(x)
barrettReduce(112)
