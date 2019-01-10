import sys

OTVET = None

prost_ch = None

def find_list_of_prost(n):
    sieve = list(range(n + 1))
    sieve[1] = 0
    for i in sieve:
        if i > 1:
            for j in range(i + i, len(sieve), i):
                sieve[j] = 0

    prost = []
    for i in sieve:
        if i != 0:
            prost.append(i)


    return prost


def razl_na_mn(ch, prostik):
    mas = []

    for e in prostik:
        con = 0
        while ch % e == 0:
            ch //= e
            con += 1
        if con > 0:
            mas.append((e, con))

        if ch == 1:
            break
    else:
        throw(RuntimeError('razl_na_mn'))

    return mas


def find_answer(ch, x_lst):
    
    def counter_of_dividers():
        if len(mas) == 0:
            return 1

        iterate = True
        ot = 1
        for i in range(len(mas)):
            n = mas[i]
            if n > 0:
                ot *= n + 1
                if iterate:
                    iterate = False
                    mas[i]-=1                    
        return ot

    
    mas = [e[1] for e in razl_na_mn(ch, prost_ch)]
    mas.sort()

    x_lst.sort(key=lambda e: e[1], reverse=False)
    itera = 0        

    remain = len(x_lst)
    while  remain > 0:
        c_div = counter_of_dividers()
        
        for i in range(remain-1, -1, -1):
          num, x = x_lst[i]
          if c_div <= x:
            OTVET[num]+=itera
            remain-=1

        if c_div == 1:
            break
        itera += 1


def print_otvet():
  for ot in OTVET:
    sys.stdout.write(str(ot)); sys.stdout.write('\n')

def resolve():
    global prost_ch, OTVET
    omg = int(input())
    mask = [(int(e), []) for e in input().split(" ")]
    con = int(input())
    #print(con)
    OTVET = [0 for i in range(con)]

    prost_ch = find_list_of_prost(200001)

    for i in range(con):
        a, b, x = map(int,input().split(" "))
        #print(a, b, x)

        for j in range(a-1, b):
          mask[j][1].append((i, x))

    for item in mask:
      ch, x_lst = item      
      if len(x_lst) > 0:
        find_answer(ch, x_lst)

    print_otvet()

sys.stdin = open("test63.txt", "r")    
resolve()
  
