# https://market.yandex.ru/product--monitor-dell-s2319hn/47667127/spec?track=tabs
# https://market.yandex.ru/product--monitor-dell-s2419h/47419270/spec?track=tabs


import time, sys

sys.stdin = open("C:\\HDDs\\ST500DM002\\Part1\\PROJECTS\\MISHA\\SPB2019\\TaskF\\test62.txt", "r")

global CACHE_LIST

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
    if ch == 1:
        mas = [(1, 1)]
        return mas
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
        raise RuntimeError('razl_na_mn')

    return mas


def sort_by(cl):
    return cl[1]


def counter_of_dividers(mas):
    if len(mas) == 0 or mas[0][0] == 1:
        return 1

    ot = 1
    for i in mas:
        ot *= i[1] + 1

    return ot



def find_answer(ch, prost):
    itera = 0
    t_list = []
    mas = razl_na_mn(ch, prost)
    mas.sort(key=sort_by)
    c_div = counter_of_dividers(mas)
    t_list.append(c_div)
    while 1 < c_div:
        if mas[0][1] > 1:
            ch //= mas[0][0]
            itera += 1
            mas[0] = (mas[0][0], mas[0][1] - 1)
        else:
            ch //= mas[0][0]
            del(mas[0])
            itera += 1

        c_div = counter_of_dividers(mas)
        t_list.append(c_div)


    return t_list



def main():
    CACHE_LIST = []
    omg = int(input())
    mask = [int(e) for e in input().split(" ")]
    con = int(input())

    max_ch = max(mask)
    prost_ch = find_list_of_prost(max_ch)

    # for i in mask:
    #     CACHE_LIST.append(find_answer(1, i, prost_ch))

    # print(CACHE_LIST)

    CACHE_LIST = [-1 for i in range(omg)]

    total_ot = 0
    for i in range(con):
        if i % 10000 == 0:
            print("GOD", i / 1000000 * 100)
        a, b, c = map(int,input().split(" "))

        ot = 0
        for j in range(a-1, b):

            if CACHE_LIST[j] == -1:
                CACHE_LIST[j] = find_answer(mask[j], prost_ch)
                # if len(CACHE_LIST[j]) > max_answer :
                    # max_answer = len(CACHE_LIST[j])
                    # print(max_answer)


            con = 0
            for t in CACHE_LIST[j]:
                if t <= c:
                    ot += con
                    break

                con += 1
                
        total_ot += ot
        #print(ot)
        
    print(total_ot)

def test():
    CACHE_LIST = []
    omg = int(input())
    mask = [int(e) for e in input().split(" ")]
    con = int(input())

    max_ch = max(mask)
    print(max_ch)
    prost_ch = find_list_of_prost(max_ch)

    check_sum = 0
    for ch in mask:
        check_sum += sum(find_answer(ch, prost_ch))

    print(check_sum)
    
if __name__ == "__main__":
    main()
