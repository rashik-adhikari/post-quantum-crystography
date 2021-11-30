#This is the main function
import keyexchange
import params
import os
import compress
import hashlib
import steg
import struct
import ast
"""
Desscription:keygen is a server-side function that generates the private key s_hat and
returns a message in the form of a tuple. This message should be encoded using
JSON or another portable format and transmitted (over an open channel) to the
client.
"""
def keygen():
    seed = os.urandom(params.SeedBytes)
    x_coefficients = genX(seed)
    s_coefficients = get_noise()
    e_coefficients = get_noise()
    r_coefficients = keyexchange.pointwise(s_coefficients, x_coefficients)
    p_coefficients = keyexchange.add(e_coefficients, r_coefficients)
    p_coefficients = compress.compression(p_coefficients)
    p_coefficients = steg.hide(p_coefficients)
    return s_coefficients, (p_coefficients, seed)


#Returns a random sampling from a normal distribution in the NTT domain.

def get_noise():
    noise = keyexchange.getNoise()
    coeffs = keyexchange.poly_ntt(noise)
    return coeffs


"""
sharedBob is a client-side function that takes the (decoded) message received
from the server as an argument. It generates the shared key bob_key and returns
a message in the form of a tuple. This message should be encoded using JSON or
another portable format and transmitted (over an open channel) to the server.
"""
def sharedBob(rec):
    (pka, seed) = rec
    pka = int(steg.unhide(pka))
    pka = compress.decompression(pka)
    x_coefficients = genX(seed)
    s_coefficients = get_noise()
    e_coefficients = get_noise()
    y_coefficients = keyexchange.pointwise(x_coefficients, s_coefficients)
    y_coefficients = keyexchange.add(y_coefficients, e_coefficients)
    v_coefficients = keyexchange.pointwise(pka, s_coefficients)
    v_coefficients = keyexchange.invntt(v_coefficients)
    e_prime = keyexchange.getNoise()
    v_coefficients = keyexchange.add(v_coefficients, e_prime)
    c_coefficients = keyexchange.helprec(v_coefficients)
    bob_key = keyexchange.received(v_coefficients, c_coefficients)
    bob_key = compress.compression(bob_key)
    c_coefficients = steg.hide(c_coefficients)
    y_coefficients = compress.compression(y_coefficients)
    y_coefficients = steg.hide(y_coefficients)
    return bob_key, (c_coefficients, y_coefficients)


def genX(seed):
    hashingAlgorithm = hashlib.shake_128()
    hashingAlgorithm.update(seed)
    # 2200 bytes from SHAKE-128 function is enough data to get 1024 coefficients
    shake_output = hashingAlgorithm.digest(3072)
    output = []
    j = 0
    for i in range(0,params.N):
        coeff = 5 * params.Q
        # Reject coefficients that are greater than or equal to 5q
        while coeff >= 5 * params.Q:
            coeff = int.from_bytes(
                shake_output[j * 2 : j * 2 + 2], byteorder = 'little')
            j += 1
            if j * 2 >= len(shake_output):
                print('Error: Not enough data from SHAKE-128')
                exit(1)
        output.append(coeff)
    return output


"""
sharedAlice is a server-side function that takes the (decoded) message received
from the client as an argument. It generates the shared key alice_key.
"""
def sharedAlice(rec, privKey):
    (c_coefficients, y_coefficients) = rec
    c_coefficients = steg.unhide(c_coefficients)
    c_coefficients = ast.literal_eval(c_coefficients)
    y_coefficients = int(steg.unhide(y_coefficients))
    y_coefficients = compress.decompression(y_coefficients)
    v_coefficients = keyexchange.pointwise(privKey, y_coefficients)
    v_coefficients = keyexchange.invntt(v_coefficients)
    alice_key = keyexchange.received(v_coefficients, c_coefficients)
    alice_key = compress.compression(alice_key)
    return alice_key
