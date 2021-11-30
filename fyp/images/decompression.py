

#decompression algorithm
def decompression(msg1):
    M = 2000000
    T = 502
    i = 0
    n = 30
    f = []
    d = msg1
    while (i < n):
        d = msg1 // T
        e = int(msg1 % T) + M
        f.append(e)
        msg1 = d
        i = i + 1
    print(f[::-1])

decompression(42491710882414189364933428606715892188754459893269385240727095009059497309170)
