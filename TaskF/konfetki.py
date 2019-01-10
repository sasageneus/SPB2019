def eratosthenes(n):     # n - число, до которого хотим найти простые числа 
    sieve = list(range(n + 1))
    sieve[1] = 0    # без этой строки итоговый список будет содержать единицу
    for i in sieve:
        if i > 1:
            for j in range(i + i, len(sieve), i):
                sieve[j] = 0
    return sieve

def print_last(sieve):
    for i in range(len(sieve)):
        v = sieve[- i - 1]
        if v != 0 :
            break
    print(v)

print_last(eratosthenes(5000000))    
