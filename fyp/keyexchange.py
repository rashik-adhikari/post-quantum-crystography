import params
import constants
import reduce
import os


#combines g(x) function within it

def ldDecode(xi):
    t = 0
    for i in range(0,4):
        t += g(xi[i])
    t -= 8 * params.Q
    t >>= 31
    return t & 1

def abs(a):
    mask = a >> 31
    return (a ^ mask) - mask


def f(a):
    y = a * 2730
    t = y >> 25
    y = a - t * 12289
    y = 12288 - y
    y >>= 31
    t -= y
    r = t & 1
    xit = t >> 1
    v0 = xit + r
    t -= 1
    r = t & 1
    v1 = (t >> 1) + r
    return (v0, v1, abs(a - v0 * 2 * params.Q))


def g(a):
    y = a * 2730
    t = y >> 27
    y = a - t * 49156
    y = 49155 - y
    y >>= 31
    t -= y
    c = t & 1
    t = (t >> 1) + c
    t *= 8 * params.Q
    return abs(t - a)


def helprec(coeffs):
    output = [0 for i in range(0, 1024)]
    v0 = [0,0,0,0]
    v1 = [0,0,0,0]
    tmp_v = [0,0,0,0]
    rand = [int.from_bytes(os.urandom(4), byteorder='little') for i in range(0, 32)]
    for i in range(0, 256):
        rbit = rand[i >> 3] >> (i & 7) & 1
        (v0[0], v1[0], k) = f(8 * coeffs[0 + i] + 4 * rbit)
        (v0[1], v1[1], a) = f(8 * coeffs[256 + i] + 4 * rbit)
        k += a
        (v0[2], v1[2], a) = f(8 * coeffs[512 + i] + 4 * rbit)
        k += a
        (v0[3], v1[3], a) = f(8 * coeffs[768 + i] + 4 * rbit)
        k += a
        k = 2 * params.Q - 1 - k >> 31
        tmp_v[0] = ((~k) & v0[0]) ^ (k & v1[0])
        tmp_v[1] = ((~k) & v0[1]) ^ (k & v1[1])
        tmp_v[2] = ((~k) & v0[2]) ^ (k & v1[2])
        tmp_v[3] = ((~k) & v0[3]) ^ (k & v1[3])
        output[0 + i] = (tmp_v[0] - tmp_v[3]) & 3
        output[256 + i] = (tmp_v[1] - tmp_v[3]) & 3
        output[512 + i] = (tmp_v[2] - tmp_v[3]) & 3
        output[768 + i] = (-k + 2 * tmp_v[3]) & 3
    return output



def received(v_coeffs, c_coeffs):
    tmp = [0, 0, 0, 0]
    key = [0 for i in range(0, 32)]
    for i in range(0, 256):
        tmp[0] = (
            16 * params.Q
            + 8 * v_coeffs[0 + i]
            - params.Q * (2 * c_coeffs[0 + i] + c_coeffs[768 + i]))
        tmp[1] = (
            16 * params.Q
            + 8 * v_coeffs[256 + i]
            - params.Q * (2 * c_coeffs[256 + i] + c_coeffs[768 + i]))
        tmp[2] = (
            16 * params.Q
            + 8 * v_coeffs[512 + i]
            - params.Q * (2 * c_coeffs[512 + i] + c_coeffs[768 + i]))
        tmp[3] = (
            16 * params.Q
            + 8 * v_coeffs[768 + i]
            - params.Q * (c_coeffs[768 + i]))
        key[i >> 3] |= ldDecode(tmp) << (i & 7)
    return key


def bitrevVector(coeffs):
    for i in range(0, params.N):
        r = constants.bitrevTable[i]
        if i < r:
            tmp = coeffs[i]
            coeffs[i] = coeffs[r]
            coeffs[r] = tmp
    return coeffs


def invntt(coeffs):
    coeffs = bitrevVector(coeffs)
    coeffs = ntt(coeffs, constants.omegasInvMontgomery)
    coeffs = multiplyCoeffs(coeffs, constants.psisInvMontgomery)
    return coeffs


# Get a random sampling of integers from a normal distribution around parameter Q.
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
    return coefficients

"""
performs number theoretic transforming.

An interesting feature of the number theory transform is that all computations are
exact (integer multiplication and addition modulo a prime integer).

There is no round-off error. This feature has been used to do fast
convolutions to multiply extremely large numbers, such as are needed when
computing pi to millions of digits of precision.
"""
def ntt(coeffs, omega):
    for i in range(0, 10, 2):
        distance = 1 << i
        for start in range(0, distance):
            jTwiddle = 0
            for j in range(start, params.N - 1, 2 * distance):
                W = omega[jTwiddle]
                jTwiddle += 1
                temp = coeffs[j]
                coeffs[j] = temp + coeffs[j + distance]
                coeffs[j + distance] = reduce.montgomeryReduce(
                    W * (temp + 3 * params.Q - coeffs[j + distance]))
        distance <<= 1
        for start in range(0, distance):
            jTwiddle = 0
            for j in range(start, params.N - 1, 2 * distance):
                W = omega[jTwiddle]
                jTwiddle += 1
                temp = coeffs[j]
                coeffs[j] = reduce.barrettReduce(temp + coeffs[j + distance])
                coeffs[j + distance] = reduce.montgomeryReduce(
                    W * (temp + 3 * params.Q - coeffs[j + distance]))
    return coeffs


def poly_ntt(coeffs):
    coeffs = multiplyCoeffs(coeffs, constants.psisBitrevMontgomery)
    coeffs = ntt(coeffs, constants.omegasMontgomery)
    return coeffs

# x and y are the coefficients of these polys as lists
#Returns coeffs[i] in normal domain after performing montgomeryReduce

def pointwise(x, y):
    coeffs = [reduce.montgomeryReduce(x[i] * reduce.montgomeryReduce(3186 * y[i])) for i in range(0, params.N)]
    return coeffs


# x and y are the coefficients of these polys as lists
#Returns coeffs[i] in normal domain after performing barrettReduce

def add(x, y):
    coeffs = [reduce.barrettReduce(x[i] + y[i]) for i in range(0, params.N)]
    return coeffs


# coeffs and factors are multiplied with each other and then montgomeryReduce function is applied
#Returns coeffs[i] in normal domain

def multiplyCoeffs(coeffs, factors):
    coeffs = [reduce.montgomeryReduce(coeffs[i] * factors[i]) for i in range(0, params.N)]
    return coeffs
