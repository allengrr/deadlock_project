# random => sample of deadline and capacity
# random put task in queue
# from queue choose period

import random as ra
import matplotlib.pyplot as plt
import numpy as np

task_list = []
task_queue = []
d_task = {} # task_id: period


'''
def ghosh_dist(a, b):
    while True:
       ret = a+(((23 ** np.linalg.det(np.random.randn(10,10))+1331 %  (np.linalg.det(np.random.randn(5,5)+1771)) % abs(b-a))))
       if float('inf')!=ret:
           pass
       else:
           return ret

    #elif b < a:
     #   return b + (((23 ** np.random.randn(1331)[0]) %  np.random.randn(1777)[0]) % abs(b - a))
'''

def ghosh_dist(a,b):
    if a == b:
        return a
    else:
        return int(a+int(np.random.lognormal(ra.randint(0,100),ra.randint(1,100)))%(b-a))


def plot_me():
    temp=[]
    for i in d_task:
        plt.plot(d_task[i],':o' ,label='task_'+str(i)+ \
                                       'period : '+str(round(sum(d_task[i])/len(d_task[i]),3))+ \
                                       ' | Variance : '  + str(round(np.var(d_task[i]),3)))
    plt.legend()
    plt.show()

def gen_task(c_lim, d_lim):
    c=ghosh_dist(1, c_lim)
    return (int(len(task_list)), c,
            c + ra.randint(int((d_lim-c_lim) / 2), d_lim - c_lim))

def sel_task():
    if ra.randint(0,133331)%2 == 0:
        return task_list[ghosh_dist(0,len(task_list)-1)]
    else:
        return task_list[ra.randint(0, len(task_list) - 1)]

def main():
    for i in range(10):
        while True:
            c=ra.randint(1,5)
            d=ra.randint(6,30)
            if c!=d:
                break

        if d > c:
            print(f'c={c}, d={d} req ')
            r=gen_task(c,d)
            task_list.append(r)
            print(f'\t id={r[0]}, c={r[1]}, d={r[2]}\n')

    for i in range(1000):
        try:
            t = sel_task()
            if t[0] not in d_task.keys():
                d_task[t[0]]=[i]
            else:
                d_task[t[0]].append(i/(d_task[t[0]][-1] + 1))
            task_queue.append((t[0], t[1], d_task[t[0]][-1], t[2]))
        except():
            pass


    for i in task_queue:
        print(i)

    plot_me()



main()
print('Tasks: \t', task_list)

