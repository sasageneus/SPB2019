import sys

N = None
TABLE = None
RESOLVE_LIST = None
CLOSED = None #Список городов имеющих

def data_read():
    global N, TABLE, CLOSED, RESOLVE_LIST
    N = int(input())
    TABLE = [[int(e) for e in input().split(' ')] for i in range(N)]
    CLOSED = False
    RESOLVE_LIST = []    

# Цель найти путь 1->N
# 0. Для каждого города создаем список еще не найденных путей. 
# 1. Собираем пути из единичных маршрутов, получаем начальный набор путей.
# 2. Проверяем есть ли наш целевой путь 1->N, если найден запоминаем
# 3. Соединяем два очередных произвольных пути
# 4. Проверяем корректность полученного пути если нет то отбрасываем попытку и пробуем следующую пару, переходим на шаг 3
# 5. Уточняем список не найденных путей

class Unresolved(Exception):
    pass

def normalize_path(path):
    if path[0] == 0:
        return path
    else:
        return path[::-1] #reverse

def print_resolve():
    r = RESOLVE_LIST[0]
    if len(RESOLVE_LIST) == 2:
        if len(RESOLVE_LIST[1]) < len(RESOLVE_LIST[0]):
            r = RESOLVE_LIST[1]

    print(len(r) - 1)
    for e in r:
        print(e + 1, end=' ')
    print()
            
        
def append_resolve(path):
    for resolve in RESOLVE_LIST:
        if resolve == path:
            return
    RESOLVE_LIST.append(path)
    if len(RESOLVE_LIST) > 2 or (not CLOSED and len(RESOLVE_LIST) > 1):
        raise Unresolved()
        

def check_all_chain_for_resolve(chain_list):
    for chain in chain_list:
        if exists_resolve(chain):
            return True
    return False

def exists_resolve(chain):
    path = []
    find = False
    for city in chain:
        if city == 0 or city == (N-1):
            path.append(city)
            if find:
                append_resolve(normalize_path(path))
                return True
            
            find = True
        elif find:
            path.append(city)
            
    return False #целевой маршрут не найден

def init_chain_list(cost_list_by_city):
    chain_list = []
    
    def find_and_append_target(city, target):
        for chain in chain_list:
            if chain[-1] == city:
                if chain.count(target) == 0:
                    chain.append(target)
                return True
            if chain[0] == city:
                if chain.count(target) == 0:
                    chain.insert(0, target)
                return True
        return False
    
    for city in range(N):
        remove_list = []
        for p in cost_list_by_city[city]:            
            target, cost = p
            if cost == 1:
                if not find_and_append_target(city, target) \
                       and not find_and_append_target(target, city):                    
                    chain_list.append([city, target])
                remove_list.append(p)
        for p in remove_list:
            cost_list_by_city[city].remove(p)

    #города которые не вошли ни в один путь превратятся в путь из одного элемента
    for city in range(N):
        for chain in chain_list:
            if chain.count(city) == 1:
                break
        else:
            chain_list.append(city)
            
    return chain_list

def init_cost_list_by_city():
    global CLOSED
    cost_list_by_city = []
    for j in range(N):
        cost_list_by_city.append([])
        for i in range(N):
            if TABLE[j][i] > 0:
                if i == j : CLOSED = True
                cost_list_by_city[j].append((i, TABLE[j][i]))
                
    return cost_list_by_city

def edge_distance_calculate(edge_distance, chain):
    chain_len = len(chain)
    for i in range(chain_len):
        # расстояние от ближайшего конца в цепочке пути
        edge_distance[chain[i]] = i if i < chain_len // 2 else chain_len - (i + 1)

def join_and_check(cost_list_by_city, chain_list, edge_distance):
    assert(len(chain_list) > 1)        
    
    new_edge_distance = None
    new_chain_list = None
    new_cost_list_by_city = None
        
    def is_correct_path(path):        
        edge_distance_calculate(new_edge_distance, path)
        #print(path)
        for city in path:
            new_cost_list_by_city[city] = []
            for target_cost in cost_list_by_city[city]:
                target, cost = target_cost
                if path.count(target) == 1:
                    if target != city:
                        dist = abs(path.index(city) - path.index(target)) 
                        if dist != cost:
                            if not CLOSED or (len(path) - dist != cost) :
                                return False # неудача, проверка не пройдена
                    #проверим случай когда путь закольцован
                    if target == city and cost != len(path): 
                        return False # неудача, проверка не пройдена

                    #print()
                    #print('target %d, cost %d' % (target, cost))
                else:
                    new_cost_list_by_city[city].append(target_cost)
                    if new_edge_distance[city] + new_edge_distance[target] + 1 > cost:
                        return False #минимальная цена возможного пути city->target будет больше чем задана исходной таблицей
                
        return True            
        
    for j in range(len(chain_list)):
        for i in range(len(chain_list)):
            if i == j: continue

            new_cost_list_by_city = cost_list_by_city[:]
            new_edge_distance = edge_distance[:]

            join_path = chain_list[j] + chain_list[i]
            if is_correct_path(join_path):
                if exists_resolve(join_path):                    
                    continue #перебираем все пути

                if len(chain_list) == 2:
                    continue
                
                new_chain_list = []
                new_chain_list.append(join_path)
                for k in range(chain_list):
                    if k==i or k==j: continue
                    new_chain_list.append(chain_list[k])

                join_and_check(new_cost_list_by_city, new_chain_list, new_edge_distance)
                    
    

def resolve_task_E():
    data_read()
    
    cost_list_by_city = init_cost_list_by_city()    
    #print(cost_list_by_city)
    
    chain_list = init_chain_list(cost_list_by_city)
    #print(chain_list)

    if check_all_chain_for_resolve(chain_list):
        print_resolve()
    else:
        edge_distance = [0 for i in range(N)]
        
        for chain in chain_list:
            edge_distance_calculate(edge_distance, chain)

        try:            
            join_and_check(cost_list_by_city, chain_list, edge_distance)
        
            if len(RESOLVE_LIST) > 0:
                print_resolve()
            else:
                raise Unresolved()
        except Unresolved:
            print('-1')
        
sys.stdin = open('test1', 'r')
resolve_task_E()

#print(N)
#print(TABLE)
    
