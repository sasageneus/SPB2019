import sys
import random

random.seed()

#LST = [118, 289, 144, 12, 0, 11, 593]
#generator()
#LST = [8, 9, 4, 2, 0, 1, 3]

ANSWER = None

def add_all_members(ex, i):
    if i == len(LST) - 1:
        ex.append(str(LST[i]))
        val = eval(''.join(ex))
        ANSWER[val % 10] += 1
    else:
        ex.append(str(LST[i]) + '+')
        add_all_members(ex[:], i+1)
        ex[-1] = str(LST[i]) + '*'
        add_all_members(ex[:], i+1)        


def bruteforce():
    global ANSWER
    print(LST)
    ANSWER = [0 for i in range(10)]
    add_all_members([], 0)    
    print(ANSWER)
    assert(sum(ANSWER) == pow(2, len(LST) - 1))

def sample_generator(p_filename, p_len):    
    f = open(p_filename, 'w')
    f.write(str(p_len));f.write('\n')
    
    for i in range(p_len):
        f.write(str(random.randint(0, 1000000000)))
        f.write(' ')

    f.write('\n')


LST = [0,1,2,3,4,5,6,7,8,9, 10,11,12,13,14,15]
bruteforce()
#print([i for i in range(10)])
sample_generator('test100000', 100000)
