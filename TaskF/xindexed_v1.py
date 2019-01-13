
CACHE1 = []
CACHE10 = []
CACHE100 = []
CACHE1000 = []

CACHE_LEVEL = ((1, CACHE1), (10, CACHE10), (100, CACHE100), (1000, CACHE1000))

FACTOR = None

def sieveOfEratosthenes(n):
    sieve = list(range(n + 1))
    factor = list(range(n + 1))
    for i in sieve:
        if i > 1:
            for j in range(i + i, len(sieve), i):
                sieve[j] = 0
                factor[j] = i

    return factor


def razl_na_mn(ch):
    mas = []
    if ch == 1:
        return mas

    d = FACTOR[ch]
    cntr = 0
    while ch != 1:
        if d != FACTOR[ch]:
            mas.append(cntr)
            d = FACTOR[ch]
            cntr = 0
        ch //=  d
        cntr +=1
    mas.append(cntr)    

    return mas


def create_cache_div(ch):
    cache_div = []
    
    def divide(multiplier, divcount):
        try: 
            divide(multiplier * divcount, next(mas_iter)+1)
        except StopIteration:
            pass
        
        while divcount > 1:
            cache_div.append(multiplier * divcount)
            divcount -= 1
       
    mas = razl_na_mn(ch)
    
    if len(mas) > 0:
        mas.sort(reverse = True)
        mas_iter = iter(mas)
        divide(1, next(mas_iter)+1)
        
    cache_div.append(1)
    
    return cache_div


def create_x_index(ch):
    cache_div = create_cache_div(ch)
    x_index = []
    x_index.append(cache_div[0])
    
    answer = len(cache_div)
    div_iter = iter(reversed(cache_div))
    x1 = next(div_iter)    
    while answer > 1:
        x2 = next(div_iter)        
        for i in range(x1, x2):
            x_index.append(answer-1)
        answer -=1
        x1=x2

    assert(len(x_index) == x_index[0])
    return x_index


def get_cache_answer(a, b, x, level):
    assert(x > 0)
    if level == 0:
        ot = 0
        for j in range(a, b + 1):
            if x < CACHE1[j][0]:
                ot += CACHE1[j][x]
        return ot
        
    mod, cache = CACHE_LEVEL[level]
    ra = (a + (mod - 1))// mod
    rb = (b + 1)// mod - 1
    if rb - ra >= 0:
        ot = 0
        for i in range(ra, rb + 1):
            if x < cache[i][0]:
                ot += cache[i][x]
                
        left_b = ra * mod - 1
        if left_b - a >= 0:
            assert(level > 0)
            ot+=get_cache_answer(a, left_b, x, level-1)

        right_a = (rb + 1) * mod
        if b - right_a >= 0:
            assert(level > 0)
            ot+=get_cache_answer(right_a, b, x, level-1)
        
        return ot        
    else:
        return get_cache_answer(a, b, x, level-1)


import time, sys

sys.stdin = open("C:\\HDDs\\ST500DM002\\Part1\\PROJECTS\\MISHA\\SPB2019\\TaskF\\test62.txt", "r")

def merge_cache(to_cache, from_cache):
    
    r = len(from_cache) - len(to_cache)
    if r > 0:
        for i in range(r):
            to_cache.append(0)

    for i in range(1, len(from_cache)):
        to_cache[i] += from_cache[i]

    to_cache[0] = len(to_cache)

def fill_high_cache(cache_high, cache_low):
    for i in range(len(cache_low)//10):
        cache_high.append([])
        
    for i in range(len(cache_low)//10*10):
        merge_cache(cache_high[i//10], cache_low[i])

def test():
    global FACTOR
    omg = int(input())
    mask = [int(e) for e in input().split(" ")]
    con = int(input())

    max_ch = max(mask)
    FACTOR = sieveOfEratosthenes(max_ch)        
    print(max_ch)

    check_sum = 0
    for ch in mask:
        #check_sum += sum(create_cache_div(ch))
        CACHE1.append(create_x_index(ch))     

    print(check_sum)

    total_ot = 0
    for i in range(con):
        a, b, x = map(int,input().split(" "))

        ot = 0
        for j in range(a-1, b):
            if x < CACHE1[j][0]:
                ot += CACHE1[j][x]
                
        total_ot += ot
        #print(ot)
        
    print(total_ot)

def test_cache_level():
    global FACTOR
    omg = int(input())
    mask = [int(e) for e in input().split(" ")]
    con = int(input())

    max_ch = max(mask)
    FACTOR = sieveOfEratosthenes(max_ch)        
    print(max_ch)

    check_sum = 0
    for ch in mask:
        CACHE1.append(create_x_index(ch))     

    print(check_sum)

    fill_high_cache(CACHE10, CACHE1)
    fill_high_cache(CACHE100, CACHE10)
    fill_high_cache(CACHE1000, CACHE100)

    total_ot = 0
    for i in range(con):
        a, b, x = map(int,input().split(" "))

        ot = get_cache_answer(a-1, b-1, x, level=3)
               
        total_ot += ot
        #sys.stdout.write(str(ot));sys.stdout.write('\n');
        
    print(total_ot)



def test_fill_high_cache():
    global FACTOR
    
    def find_answer(a,b,x,lvl):
        ot = 0
        for i in range(a,b):
            ot = get_cache_answer(a, b, x, level=lvl)
        return ot

    print('test_fill_high_cache')
    
    omg = int(input())
    mask = [int(e) for e in input().split(" ")]
    con = int(input())

    max_ch = max(mask)
    FACTOR = sieveOfEratosthenes(max_ch)        
    print(max_ch)

    check_sum = 0
    for ch in mask:
        CACHE1.append(create_x_index(ch))     

    print(check_sum)

    fill_high_cache(CACHE10, CACHE1)

    print(find_answer(0,9,1,1))
    print(find_answer(0,9,1,0))
    assert(find_answer(0,9,1,1) == find_answer(0,9,1,0))
    assert(find_answer(9,19,1,1) == find_answer(9,19,1,0))
    
def test_create_x_index(num):
    global FACTOR
    FACTOR = sieveOfEratosthenes(200000)
    print(create_cache_div(num))
    print(create_x_index(num))
    

def test_razl_na_mn():
    global FACTOR
    FACTOR = sieveOfEratosthenes(1000000)
    print(razl_na_mn(2))
    pass
    
if __name__ == "__main__":
    test_cache_level()
    #test_fill_high_cache()
    

