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


def shift_and_copy(vect, value):
    if value == 0:
        return vect[:]
    else:
        #shift right
        return vect[-value:] + vect[:-value]

def append_member(idx):
    value = LST[idx]
    res_idx = shift_and_copy(RESULT[idx-1], value)
    
    #print(res_idx)
    multiplier = (value * LST[idx - 1]) % 10
    mult_for_cache = multiplier
    k = idx - 2
    res_mult = [0 for i in range(10)]    
    while k >= 0:
        if k < (idx - 2):
            cache_mult, cache_k, mult_at_end = CACHE[k]
            if cache_mult == multiplier:
                #print('idx %d k=%d' % (idx, k))            
                #print(cache_k)
                for i in range(10):        
                    res_mult[i] += cache_k[i]
                multiplier = mult_at_end
                break

        i = 0
        for e in shift_and_copy(RESULT[k], multiplier):
            res_mult[i]+=e
            i+=1                
        
        multiplier = (multiplier * LST[k]) % 10        
        k -= 1

    if idx - 2 >= 0:
        CACHE.append((mult_for_cache, res_mult, multiplier))
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

sys.stdin = open('test100000', 'r')
read_data()
#print(LST)
resolve_H()
print_result(RESULT[-1])
