import sys
from datetime import datetime

CASES_FOLDER = 'SolomonPotvinBengio'
N = None
GRAPH = None
SCHEDULES = None
MAX_ITER = None
TIMEOUT = 1000000
START = datetime.now()
CASES = sorted(['rc_201.1.txt','rc_201.4.txt','rc_202.3.txt','rc_203.2.txt','rc_204.1.txt','rc_205.1.txt','rc_205.4.txt','rc_206.3.txt','rc_207.2.txt','rc_208.1.txt','rc_201.2.txt','rc_202.1.txt','rc_202.4.txt','rc_203.3.txt','rc_204.2.txt','rc_205.2.txt','rc_206.1.txt','rc_206.4.txt','rc_207.3.txt','rc_208.2.txt','rc_201.3.txt','rc_202.2.txt','rc_203.1.txt','rc_203.4.txt','rc_204.3.txt','rc_205.3.txt','rc_206.2.txt','rc_207.1.txt','rc_207.4.txt','rc_208.3.txt'])


def build_graph(case: str):
    global N, GRAPH, SCHEDULES, CASES_FOLDER
    with open(CASES_FOLDER + '/' + case, 'r') as case_file:
        N = int(case_file.readline())
        GRAPH = []
        SCHEDULES = []
        for i in range(N):
            GRAPH.append([float(x) for x in case_file.readline().strip().split(' ')])
        for i in range(N):
            line = case_file.readline().strip().split(' ')
            schedule = []
            for x in line:
                try:
                    schedule.append(float(x))
                except: 
                    pass
            SCHEDULES.append(tuple(schedule))

def load_expected(case: str):
    expected = {}
    with open('expected.txt', 'r') as expected_file:
        for line in expected_file.readlines():
            processed = [x for x in line.strip().split(' ') if x != '']
            if (processed[0][0] != '#'):
                expected[processed[0]] = (float(processed[1]), [0] + [int(x) for x in processed[3:]] + [0])
    return expected[case]

def calculate_path_cost(path: list):
    global GRAPH, SCHEDULES
    diff = 0
    prev = path[0]
    elapsed = 0
    overused = 0
    total = 0
    for i in range(1, len(path)):
        curr = path[i]
        elapsed = max(elapsed + GRAPH[prev][curr], SCHEDULES[curr][0])
        if elapsed > SCHEDULES[curr][1]:
            overused += 1
        total += GRAPH[prev][curr]
        prev = curr
    return elapsed, overused, total


def calculate_path_cost_print(path: list):
    global GRAPH, SCHEDULES
    diff = 0
    prev = path[0]
    elapsed = 0
    overused = 0
    total = 0
    for i in range(1, len(path)):
        curr = path[i]
        print('prev {} curr {} cost {} elapsed {} schedules {}'.format(prev, curr, GRAPH[prev][curr], elapsed, SCHEDULES[curr]))
        elapsed = max(elapsed + GRAPH[prev][curr], SCHEDULES[curr][0])
        if elapsed > SCHEDULES[curr][1]:
            overused += 1 
        total += GRAPH[prev][curr]
        prev = curr
    return elapsed, overused, total

def build_base_greedy():
    global N, GRAPH
    path = [0]
    prev = 0
    elapsed = 0
    for i in range(1, N):
        curr_min = float('inf')
        curr_min_node = -1
        for j in range(1, N):
            cost = max(elapsed + GRAPH[prev][j], SCHEDULES[j][0])
            if prev != j and j not in path and (curr_min > cost or curr_min_node == -1):
                curr_min = cost
                curr_min_node = j
        path.append(curr_min_node)
        prev = curr_min_node
        elapsed = curr_min
    
    return path + [0]

def calculate_level_and_deviation(m: int):
    global N
    curr = m
    for i in range(1, N):
        if curr < N-i:
            break
        curr -= N-i
    return i-1, curr

def build_greedy(iteration: int):
    global N, GRAPH, SCHEDULES
    level, deviation = calculate_level_and_deviation(iteration)
    path = [0]
    prev = 0
    elapsed = 0
    for i in range(1, N):
        possible = []
        for j in range(1, N):
            if prev != j and j not in path:
                possible.append((max(GRAPH[prev][j], SCHEDULES[j][0]), j))
        possible.sort()
        taken = 0
        if i - 1 == level:
            taken = deviation
        path.append(possible[taken][1])
        prev = path[-1]
        elapsed += possible[taken][0]
    
    return path + [0]

def two_opt_swap(path: list, i: int, k: int):
    return path[:i] + path[i:k][::-1] + path[k:]

def two_opt(path: list):
    best_path = path
    best_elapsed, best_error, best_total = calculate_path_cost(path)
    for i in range(1, len(path)-1):
        for k in range(i+1, len(path)-1):
            new_path = two_opt_swap(path, i, k)
            new_elapsed, new_error, new_total = calculate_path_cost(new_path)
            if (new_error <= best_error and new_total < best_total):
                best_elapsed, best_error, best_total, best_path = new_elapsed, new_error, new_total, new_path
    return best_path


def print_graph():
    global N, GRAPH, SCHEDULES
    for i in range(N):
        print(GRAPH[i])
    for i in range(N):
        print(SCHEDULES[i])
    
    return path + [0]

def vns(m: int):
    global N, MAX_ITER, START, TIMEOUT
    best_path, best_i = build_base_greedy(), 0
    best_elapsed, best_overused, best_total = calculate_path_cost(best_path)
    fallback_level = 1
    max_fallback_level = MAX_ITER
    used = {}
    for i in range(m):
        path =  best_path
        path_tp = tuple(path)
        if path_tp in used and fallback_level < max_fallback_level:
            path = build_greedy(fallback_level)
            path_tp = tuple(path)
            fallback_level += 1
        elif path_tp in used and fallback_level == max_fallback_level:
            break
        if  (datetime.now() - START).total_seconds() > TIMEOUT: 
            break
        used[path_tp] = True
        elapsed, overused, total = calculate_path_cost(path)
        new_path = two_opt(path)
        new_elapsed, new_overused, new_total = calculate_path_cost(new_path)
        
        if (new_overused <= best_overused and new_total < best_total):
            best_path, best_elapsed, best_overused, best_total, best_i = new_path, new_elapsed, new_overused, new_total, i

    return best_i, best_path, best_elapsed, best_overused, best_total

def d_t(i: int, j: int, t: float):
    global GRAPH, SCHEDULES
    return max(SCHEDULES[j][0], GRAPH[i][j] + t)

def preprocessing():
    global N, GRAPH, SCHEDULES
    changed = True
    P = set()
    while changed:
        changed = False
        for i in range(1, N):
            original = SCHEDULES[i]
            SCHEDULES[i] = (max(SCHEDULES[i][0], 
                                min(SCHEDULES[i][1], 
                                    min([d_t(j, i, SCHEDULES[j][0]) if j != i else SCHEDULES[i][1] for j in range(0, N)]))), 
                            SCHEDULES[i][1])
            changed |= original != SCHEDULES[i]
        for i in range(1, N):
            for j in range(0, N):
                if i != j:
                    if d_t(i, j, SCHEDULES[i][0]) > SCHEDULES[j][1]:
                        if GRAPH[i][j] != float('inf'):
                            changed |= True
                            GRAPH[i][j] = float('inf')
                            P.add((j, i))
    for i in range(1, N):
        for j in range(1, N):
            if i != j:
                prescedence = True
                prescedence2 = True
                for k in range(1, N):
                    if k != i and k != j:
                        prescedence &= d_t(j, k, d_t(i, j, SCHEDULES[i][0])) > SCHEDULES[k][1] and d_t(i, j, d_t(k, i, SCHEDULES[k][0])) > SCHEDULES[j][1]
                        prescedence2 &= prescedence and d_t(k, j, d_t(i, k, SCHEDULES[i][0])) > SCHEDULES[j][1]
                if prescedence and GRAPH[i][j] != float('inf'):
                    GRAPH[i][j] = float('inf')
                    changed |= True
                if prescedence2:
                    P.add((j, i))
    for i in range(1, N):
        for j in range(1, N):
            if i != j and GRAPH[j][i] == float('inf'):
                for k in range(1, N):
                    if k != i and k != j:
                        if GRAPH[k][j] == float('inf') and GRAPH[k][i] != float('inf'):
                            GRAPH[k][i] = float('inf')
                            P.add((i, k))
    for edge in P:
        GRAPH[edge[0]][0] = float('inf')
        GRAPH[0][edge[1]] = float('inf')

def solve_case(case: str):
    global N, MAX_ITER, START
    START = datetime.now()
    build_graph(case)
    preprocessing()
    
    MAX_ITER = (N * (N-1))//2
    best_i, best_path, best_elapsed, best_overused, best_total = vns(MAX_ITER * 5)
    end = datetime.now()
    if best_overused == 0.0:
        print('{:20} | {:131} | {:20}'.format('case', 'path', 'cost'))
        print('{:20} | {:131} | {:20}'.format(case, str(best_path)[1:-1], best_total))
    else:
        print('no feasible solution found')
    return best_overused == 0.0

def solve_all():
    not_solved = 0
    not_solved_cases = []
    for case in CASES:
        if not(solve_case(case)):
            not_solved += 1
            not_solved_cases.append(case)
    print('not solved cases', not_solved, not_solved_cases)

def main():
    global N, TIMEOUT
    TIMEOUT = int(sys.argv[1])
    case = sys.argv[2]
    #solve_all()
    solve_case(case)
    
main()
