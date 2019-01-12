import sys

N = None
LST = None
RESULT = []
CACHE = []

MOD = pow(10, 9) + 7

def read_data():
    global LST, N
    N = int(input())
    LST = [int(e[-1]) for e in input().split(' ')]

def append_member(idx):
    value = LST[idx]
    #res_idx = [(e + value) % 10 for e in RESULT[idx-1]]
    res_idx = [0 for i in range(10)]
    for i in range(10):
        if RESULT[idx-1][i] > 0:
            res_idx[(i + value) % 10] += RESULT[idx-1][i]

    #print(res_idx)
    multiplier = (value * LST[idx - 1]) % 10
    mult_start = multiplier
    k = idx - 2
    res_mult = [0 for i in range(10)]    
    while k >= 0:
        if k < (idx - 2) and CACHE[k][0] == multiplier:
            #print('idx %d k=%d' % (idx, k))            
            cache_k = CACHE[k][1]
            #print(cache_k)
            for i in range(10):        
                res_mult[i] += cache_k[i]
            multiplier = CACHE[k][2]
            break
            
        res_k = RESULT[k]
        for i in range(10):
            if res_k[i] > 0:
                res_mult[(i + multiplier) % 10] += res_k[i]
        multiplier = (multiplier * LST[k]) % 10        
        k -= 1

    if idx - 2 >= 0:
        CACHE.append((mult_start, res_mult, multiplier))
        #print('append cache')

    res_idx[multiplier % 10] += 1
    
    for i in range(10):        
        res_idx[i] = (res_idx[i] + res_mult[i]) % MOD

    #print('cache')
    #print(res_mult)
        
    #print(res_idx)
    RESULT.append(res_idx)
    

def resolve_H():
    RESULT.append([0 for i in range(10)])
    RESULT[0][LST[0] % 10] = 1

    for i in range(1, N):
        append_member(i)
    
def print_result(res):
    print(' '.join([str(e) for e in res]) )

sys.stdin = open('test1000', 'r')
read_data()
#print(LST)
resolve_H()
print_result(RESULT[-1])
