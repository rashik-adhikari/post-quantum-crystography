import params
import os
def getNoise():
    coefficients = []
    for i in range(0, params.N):
        t = int.from_bytes(os.urandom(4), byteorder='little')
        d = 0
        for j in range(0, 8):
            d += (t >> j) & 0x01010101
        x = ((d >> 8) & 0xff) + (d & 0xff)
        y = (d >> 24) + ((d >> 16) & 0xff)
        coefficients.append(x + params.Q - y)
    print(coefficients)
getNoise()
