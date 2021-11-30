
#compression algorithm
def compression(msg):
    global x, M, T, n
    x = [y for y in msg]
    #np.array(x)
    M = min(x)
    T = max(x) - M + 2
    a = 0
    c = 0
    n = len(x)
    i = 0
    while (i < n):
        b = x[i]
        a = T * c +  b - M
        c = a
        i = i + 1
    return a


#decompression algorithm
def decompression(msg1):
    i = 0
    f = []
    d = msg1
    while (i < n):
        d = msg1 // T
        e = int(msg1 % T) + M
        f.append(e)
        msg1 = d
        i = i + 1
    return f[::-1]
