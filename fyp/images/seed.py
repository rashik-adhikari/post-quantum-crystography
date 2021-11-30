import os
import params
def keygen():
    seed = os.urandom(params.SeedBytes)
    print(seed)
keygen()
