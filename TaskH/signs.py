import sys

N = None
LST = None
RESULT = []

MOD = pow(10, 16)

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
    k = idx - 2
    while k >= 0:
        res_k = RESULT[k]
        for i in range(10):
            if res_k[i] > 0:
                res_idx[(i + multiplier) % 10] += res_k[i]
                res_idx[(i + multiplier) % 10]%=MOD
        multiplier = (multiplier * LST[k]) % 10        
        k -= 1
        
    res_idx[multiplier % 10] += 1
    
    RESULT.append(res_idx)
    #print(RESULT[idx])

def resolve_H():
    RESULT.append([0 for i in range(10)])
    RESULT[0][LST[0] % 10] = 1

    for i in range(1, N):
        append_member(i)
    
def print_result(res):
    print(' '.join([str(e) for e in res]) )

sys.stdin = open('test1000', 'r')
read_data()
print(LST)
resolve_H()
print_result(RESULT[-1])
