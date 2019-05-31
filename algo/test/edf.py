from functools import reduce

# tasks = {ti: [capacity, deadline, period]}
tasks = {
    't1': [3, 7, 20],
    't2': [2, 4, 5],
    't3': [2, 8, 10],
}


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


def _lcm(a, b):
    return int(a * b / gcd(a, b))


def lcm(_list):
    return reduce(_lcm, _list)


t_lcm = lcm([tasks[i][-1] for i in tasks])

t_dead = {i: tasks[i][1] for i in tasks}

print(sorted(t_dead.items(), key =
             lambda kv:(kv[1], kv[0])))