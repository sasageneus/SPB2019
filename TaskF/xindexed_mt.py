import sys

CACHE_LEVEL = []


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
    if level == 0:
        cache1 = CACHE_LEVEL[0][1]
        ot = 0
        for j in range(a, b + 1):
            if x < cache1[j][0]:
                ot += cache1[j][x]
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
            ot+=get_cache_answer(a, left_b, x, level-1)

        right_a = (rb + 1) * mod
        if b - right_a >= 0:
            ot+=get_cache_answer(right_a, b, x, level-1)
        
        return ot        
    else:
        return get_cache_answer(a, b, x, level-1)


def merge_cache(to_cache, from_cache):
    
    r = len(from_cache) - len(to_cache)
    if r > 0:
        for i in range(r):
            to_cache.append(0)

    for i in range(1, len(from_cache)):
        to_cache[i] += from_cache[i]

    to_cache[0] = len(to_cache)

def fill_high_cache(cache_high, cache_low, k):
    for i in range(len(cache_low)//k):
        cache_high.append([])
        
    for i in range(len(cache_low)//k*k):
        merge_cache(cache_high[i//k], cache_low[i])

def fill_multilevel_cache(n, k):
    prev_level_cache = CACHE_LEVEL[0][1]
    for i in range(1, n):
        next_level_cache = []
        fill_high_cache(next_level_cache, prev_level_cache, k)
        CACHE_LEVEL.append((pow(k, i), next_level_cache))
        prev_level_cache = next_level_cache

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

    cache1 = []
    CACHE_LEVEL.append((1, cache1))
    
    check_sum = 0
    for ch in mask:
        cache1.append(create_x_index(ch))     

    print(check_sum)

    fill_multilevel_cache(5, k=8)

    total_ot = 0
    for i in range(con):
        a, b, x = map(int,input().split(" "))

        ot = get_cache_answer(a-1, b-1, x, level=4)
               
        total_ot += ot
        #sys.stdout.write(str(ot));sys.stdout.write('\n');
        
    print(total_ot)


def create_x_index_worker(q):
    cache1 = CACHE_LEVEL[0][1]
    total_div = 0
    
    while True:
        i, ch = q.get_nowait()
        if ch is None:
            break
        cache1[i] = create_x_index(ch)
        total_div += cache1[i][0]
        #q.task_done()

    return total_div


def task_F_mt():
    global FACTOR

    import queue
    from  concurrent.futures import ThreadPoolExecutor    

    
    def read_number_worker():
        i = 0
        for e in input().split(" "):
            input_queue.put((i, int(e)))
            i += 1
        input_queue.put((-1, None))
        input_queue.put((-1, None))

    
    executor = ThreadPoolExecutor(max_workers=8)
    factor_fea = executor.submit(sieveOfEratosthenes, 1000000)

    omg = int(input())

    print(omg)
    
    input_queue = queue.Queue(10000) #
        
    read_number_fea = executor.submit(read_number_worker)
            
    cache1 = [None for i in range(omg)]
    CACHE_LEVEL.append((1, cache1));
        
    FACTOR = factor_fea.result()

    print('FACTOR')

    total_fut1 = executor.submit(create_x_index_worker, input_queue)
    total_fut2 = executor.submit(create_x_index_worker, input_queue)

    read_number_fea.result()

    #while not input_queue.empty(): pass

    print('Success!!! total diveders= %d' % (total_fut1.result() + total_fut2.result() ))
    
    con = int(input())


def task_F_mt2():
    global FACTOR
    
    import collections
    from  concurrent.futures import ThreadPoolExecutor    

    num_workers = 2
    
    def read_number_worker():
        i = 0
        for e in input().split(" "):
            input_queue.append((i, int(e)))
            i += 1

        #flag stop work
        for i in range(num_workers):
            input_queue.append((-1, None))


    def create_x_index_worker(q):
        cache1 = CACHE_LEVEL[0][1]
        total_div = 0
        
        while True:
            try:
                i, ch = q.popleft()
            except IndexError:
                continue            
                
            if ch is None:
                break
            cache1[i] = create_x_index(ch)
            total_div += cache1[i][0]            
            
        return total_div

    
    executor = ThreadPoolExecutor(max_workers=8)
    factor_fut = executor.submit(sieveOfEratosthenes, 1000000)

    omg = int(input())

    print(omg)
    
    input_queue = collections.deque() #
        
    read_number_fut = executor.submit(read_number_worker)
            
    cache1 = [None for i in range(omg)]
    CACHE_LEVEL.append((1, cache1));
        
    FACTOR = factor_fut.result()

    print('FACTOR')
    
    workers = [executor.submit(create_x_index_worker, input_queue) for i in range(num_workers)]

    read_number_fut.result()

    #while not input_queue.empty(): pass

    print('Success!!! total diveders= %d' % (sum([w.result() for w in workers])))

    fill_multilevel_cache(4, k=8)
    
    con = int(input())

    import time

    ttt = 0
    
    def find_answer_worker(num):
        print('num')
        while 1:
            ttt += 1
            print('ttt')
            try:
                i, a, b, x = task_queue.popleft()
                print('iabx')               
            except IndexError:
                continue
                
            if x is None:
                break
            
            answer_list[i] = get_cache_answer(a-1, b-1, x, level=3)
        return ttt
            

    task_queue = collections.deque() #
    
    workers = [executor.submit(find_answer_worker, i) for i in range(num_workers)]

    answer_list = [None for i in range(con)]
    
    total_ot = 0
    for i in range(con):
        a, b, x = map(int,input().split(" "))
        task_queue.append((i,a,b,x))

    #stop flag
    for i in range(num_workers):
        task_queue.append((-1,-1,-1,None))

    for i in range(con):
        print(i)
        while answer_list[i] is None:
            print(ttt) 
            time.sleep(1)
        
        total_ot += answer_list[i]
        #sys.stdout.write(str(ot));sys.stdout.write('\n');
        
    print(total_ot)
    
    
  
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
    sys.stdin = open("C:\\HDDs\\ST500DM002\\Part1\\PROJECTS\\MISHA\\SPB2019\\TaskF\\test62.txt", "r")
    #test_cache_level()
    task_F_mt2()
    

