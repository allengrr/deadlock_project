from functools import reduce
from sys import *
import numpy as np
import random as r
import ping_code as pc
import socket
import struct
import subprocess as sp
from threading import Thread
import paramiko
import ast
import time
import os
import getpass as gp
import data

hosts = {}  # {hostname: ip}
multicast_group = '224.3.29.71'
server_address = ('', 10000)

# Create the socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Bind to the server address
sock.bind(server_address)
# Tell the operating system to add the socket to the multicast group
# on all interfaces.
group = socket.inet_aton(multicast_group)
mreq = struct.pack('4sL', group, socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

_tasks = {'t1': {'wcet': 3, 'period': 20},
          't2': {'wcet': 1, 'period': 5},
          't3': {'wcet': 2, 'period': 10},
          't4': {'wcet': 1, 'period': 10},
          't5': {'wcet': 3, 'period': 15}
          }

# mat = {'p0': ['cpu', 'mem', 'storage']}
_need = {
    't1': [7, 4, 3],
    't2': [1, 2, 2],
    't3': [6, 0, 0],
    't4': [0, 1, 1],
    't5': [4, 3, 1]

}
allocation = {
    't1': [0, 1, 0],
    't2': [2, 0, 0],
    't3': [3, 0, 2],
    't4': [2, 1, 1],
    't5': [0, 0, 2]
}

mec_waiting_time = {}   # {ip : [moving (waiting time + rtt)]}

offload_register = {}      # {task: host_ip}

discovering = 0            # if discovering == 0 update host
_pos = 0                   # keep tracks of time and tasks


def ip_address():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]


def get_rtt(host):
    rtt = pc.verbose_ping(host)

    return rtt


def gcd(a, b):
    if b == 0: return a
    return gcd(b, a % b)


def lcm(a, b):
    return int(a * b / gcd(a, b))


def LCM(list):
    return reduce(lcm, list)


def gosh_dist(_range):
    return ((23 ** r.randrange(1, 1331)) % r.randrange(1, 1777)) % _range


def get_rms():
    global tasks
    global _pos

    tasks = data.task[_pos]
    _pos += 1

    '''
    tasks = {}
    while len(tasks) < 2:
        a = list(_tasks.keys())[gosh_dist(5)]
        tasks[a] = _tasks[a]
    '''

    print('Running RMS on Tasks: ', tasks, '\n')
    waiting_time_init()
    a = load_tasks()
    return scheduler(a)


def waiting_time_init():
    global t_time

    t_time = {i: [round(r.uniform(0.4, 0.8), 3), round((tasks[i]['period']) / (tasks[i]['wcet']), 3)] for i in
              tasks}  # t_time = {'ti': [execution_time, latency], ..}

    t_time = {**t_time, **check_mec_offload()}
    print('[Execution_time, Latency]: ', t_time)


def load_tasks():
    global tasks

    period_list = [tasks[i]['period'] for i in tasks]

    lcm_period = LCM(period_list)
    # insert idle task
    tasks['idle'] = {'wcet': lcm_period, 'period': lcm_period + 1}
    return lcm_period


def scheduler(D):
    queue = list(tasks.keys())  # initialize task queue
    schedule = []
    rms = []
    curr = ''  # current task
    prev = ''  # previous task
    tmp = {}
    for task in tasks.keys():
        tmp[task] = {}  # temporary data for each task
        tmp[task]['deadline'] = tasks[task]['period']
        tmp[task]['executed'] = 0

    # start scheduling...
    # proceed by one timestamp to handle preemption
    for time in range(D):
        # insert new tasks into the queue
        for t in tmp.keys():
            if time == tmp[t]['deadline']:
                if tasks[t]['wcet'] > tmp[t]['executed']:
                    # print('Scheduling Failed at %d' % time)
                    exit(1)
                else:
                    tmp[t]['deadline'] += tasks[t]['period']
                    tmp[t]['executed'] = 0
                    queue.append(t)
        # select next task to be scheduled
        min = D * 2
        for task in queue:
            if tmp[task]['deadline'] < min:
                min = tmp[task]['deadline']
                curr = task
        tmp[curr]['executed'] += 1
        # print(time, queue, curr)

        # dequeue the execution-completed task
        if tmp[curr]['executed'] == tasks[curr]['wcet']:
            for i in range(len(queue)):
                if curr == queue[i]:
                    del queue[i]
                    break

        # record to the schedule trace
        if prev != curr:
            if prev in queue and prev != 'idle':  # previous task is preempted..
                s = schedule.pop()
                schedule.append([s[0], s[1], '*'])
                rms.append(s[1])
            schedule.append([time, curr])
            if curr != 'idle': rms.append(curr)
        prev = curr

    return offloaded + rms


# generate execution sequence
def wait_die(processes, avail, n_need, allocat):
    offload = []

    # To store execution sequence
    exec_seq = []

    # Make a copy of available resources
    work = [0] * len(processes)

    # While all processes are not finished
    # or system is not in safe state.
    while 'w' or 0 in work:
        if 0 in work:
            ind = work.index(0)
            i = processes[ind]
        elif 'w' in work:
            # print('wk: ', work)
            ind = work.index('w')
            i = processes[ind]
        else:
            break

        # print('comparing| process: ', i, _need[i], 'work: ', avail)
        if not (False in list(np.greater_equal(avail, n_need[i]))):
            exec_seq.append(i)
            avail = np.add(avail, allocat[i])
            work[ind] = 1
            # print('added: ', exec_seq)

        else:
            a = list(set(processes) - set(exec_seq) - set(offload))
            n = {}
            for j in a:
                n[j] = sum(allocat[j])
            _max = max(n, key=n.get)
            # print('work: ', work, 'need: ', _need[_max])
            if processes.index(_max) > processes.index(i):   # if true, i is older
                # if process is already waiting then offload process
                if work[ind] == 'w':
                    offload.append(i)
                    avail = np.array(avail) + np.array(allocat[i])
                    work[processes.index(i)] = 1
                    # print('offload reentry: ', i, offload)
                else:
                    # wait put process to waiting
                    work[processes.index(i)] = 'w'
                    # print('waiting: ', i)

            else:
                # abort i
                offload.append(i)
                avail = np.array(avail) + np.array(allocat[i])
                work[processes.index(i)] = 1
                # print('offload: ', i)

    if len(offload) > 0:
        print('offloading tasks: ', offload)
        cooperative_mec(offload, 0)

    print('Execution seq: ', exec_seq)

    return exec_seq


def get_exec_seq(pro):
    global P
    global R

    # Number of processes
    P = len(pro)

    # Number of resources
    R = 3
    processes = ['{}_{}'.format(pro[i], i) for i in range(P)]

    # Available instances of resources
    avail = [5, 5, 5]
    n_need = {i: _need[i[:2]] for i in processes}
    # print('need', n_need)
    # Resources allocated to processes
    allot = {i: allocation[i[:2]] for i in processes}

    # return execution sequence
    return wait_die(processes, avail, n_need, allot)


def calc_wait_time(list_seq):
    pre = 0
    time_dic = {}
    for i in list_seq:
        j = '_'.join(i.split('_')[:-1])            # i = 't5_3_3', j = 't5_3'
        time_dic[i] = round(t_time[j][0] + pre, 3)
        pre += t_time[j][0]
    w_send = time_dic[list(time_dic.keys())[-1]]
    send_message(str(w_send))   # Broadcasting waiting time to cooperative MECs
    return time_dic


def compare_local_mec(list_seq):
    time_compare_dict = {i: t_time['_'.join(i.split('_')[:-1])][1] > list_seq[i] for i in list_seq}
    print('local vs MEC comparison: ', time_compare_dict)
    execute_mec = []
    execute_locally = []
    for i in time_compare_dict:
        if time_compare_dict[i]:
            execute_locally.append(i)
        else:
            execute_mec.append(i)

    return execute_mec, execute_locally


def calculate_mov_avg(ma1, a1):

    if ma1 in mec_waiting_time:
        _count = len(mec_waiting_time[ma1])
        avg1 = mec_waiting_time[ma1][-1]
    else:
        _count = 0
        avg1 = 0
    _count += 1
    avg1 = ((_count - 1) * avg1 + a1) / _count
    # ma1.append(avg1) #cumulative average formula
    # μ_n=((n-1) μ_(n-1)  + x_n)/n
    return avg1


def send_message(mg):
    _multicast_group = ('224.3.29.71', 10000)
    try:

        # Send data to the multicast group
        if mg == 'hello':
            smg = mg + ' ' + message()
            sock.sendto(str.encode(smg), _multicast_group)
            print('\nHello message sent')

        else:
            sock.sendto(str.encode(mg), _multicast_group)

    except Exception as e:
        print(e)


def message():
    cmd = ['cat /etc/hostname']
    hostname = str(sp.check_output(cmd, shell=True), 'utf-8')[0:-1]
    return hostname


def receive_message():
    global hosts

    while True:
        data, address = sock.recvfrom(1024)

        if data.decode()[:5] == 'hello':
            hosts[data.decode()[6:]] = address[0]

        elif (data.decode()[:6] == 'update') and (discovering == 0):
            hosts = ast.literal_eval(data.decode()[7:])
            # print('received: ', hosts)

        elif (data.decode()[:6] != 'update') and (address[0] != host_ip):
            w_time = calculate_mov_avg(address[0], float(data.decode()) + get_rtt(address[0]))      # calcuate moving average of mec wait time => w_time = wait time + rtt
            if address[0] in mec_waiting_time:
                mec_waiting_time[address[0]].append(w_time)
            else:
                mec_waiting_time[address[0]] = [w_time]


def mec_comparison():
    # returns min average waiting for all mecs
    if len(mec_waiting_time) == 0:
        return 0
    min_mec = {i: mec_waiting_time[i][-1] for i in mec_waiting_time}
    min_wt = min(min_mec, key=min_mec.get)
    return min_wt


def mec_task_unicast(task, host_):
    try:
        c = paramiko.SSHClient()

        un = 'mec'
        pw = 'password'
        port = 22

        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect(host_, port, un, pw)
        cmd = ('echo "{} {} {}" >> /home/mec/deadlock_project/temp/task_share.txt'.format(host_ip, task, t_time[task[:2]]))  # task share : host ip task

        stdin, stdout, stderr = c.exec_command(cmd)
    except Exception as e:
        print(e)


def cooperative_mec(mec_list, n):
    for i in mec_list:
        _host = mec_comparison()
        if _host == 0:
            mec_task_unicast(i, cloud_ip)

            print('\n=========SENDING {} TO CLOUD==========='.format(i))

        elif n == 0:
            j = '_'.join(i.split('_')[:-1])
            if mec_waiting_time[_host][-1] < t_time[j][1]:     # CHECK IF THE MINIMUM MEC WAIT TIME IS LESS THAN TASK LATENCY

                mec_task_unicast(i, _host)                 # SENDS TASK TO MEC FOR EXECUTION

                mec_waiting_time[_host].append(mec_waiting_time[_host][-1] + t_time[j][0])      # adds a new average waiting time
                print('\n======SENDING {} TO MEC {}========='.format(i, _host))
            else:
                mec_task_unicast(i, cloud_ip)

                print('\n=========SENDING {} TO CLOUD==========='.format(i))
        else:
            j = '_'.join(i.split('_')[:-1])
            if mec_waiting_time[_host][-1] < t_time[j][1]:  # CHECK IF THE MINIMUM MEC WAIT TIME IS LESS THAN TASK LATENCY

                mec_task_unicast(i, _host)  # SENDS TASK TO MEC FOR EXECUTION

                mec_waiting_time[_host].append(mec_waiting_time[_host][-1] + t_time[j][0])  # adds a new average waiting time
                print('\n======SENDING {} TO MEC {}========='.format(i, _host))
            else:
                mec_task_unicast(i, cloud_ip)

                print('\n=========SENDING {} TO CLOUD==========='.format(i))


def check_mec_offload():
    global offloaded

    offloaded = []
    t_mec = {}                # {t1: [execution, latency}
    try:
        fr = open('/home/mec/deadlock_project/temp/task_share.txt', 'r')
        t = fr.readlines()
        for i in t:
            ta = i[:-1].split()[1][:2] + '_' + str(t.index(i))
            offloaded.append(ta)
            offload_register[ta] = i[:-1].split()[0]
            t_mec[ta] = ast.literal_eval(''.join(i[:-1].split()[2:]))
        fr.close()
        os.system('rm /home/mec/deadlock_project/temp/task_share.txt')
        print('Tasks Offloaded to MEC: {}'.format(offloaded))
    except Exception as e:
        print('no offloaded Task!')
    return t_mec


def execute(local):
    print('\nExecuting :', local)
    send = []
    for i in local:
        j = '_'.join(i.split('_')[:-1])
        time.sleep(t_time[j][0])
        print('#' *((local.index(i) + 1) * 3), ' Executed: ', i)
        if len(j) > 2:
            send.append(j)
    print('============== EXECUTION DONE ===============')
    return send


def send_back_task(l_list):
    _host_ip = ip_address()
    for i in l_list:
        try:
            c = paramiko.SSHClient()

            un = 'mec'
            pw = 'password'
            port = 22

            c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            c.connect(offload_register[i], port, un, pw)
            cmd = ('echo "{} {}" >> /home/mec/deadlock_project/temp/executed.txt'.format(i, _host_ip))  # task share : host ip task

            stdin, stdout, stderr = c.exec_command(cmd)
        except Exception as e:
            print(e)


def receive_executed_task():
    try:
        fr = open('/home/mec/deadlock_project/temp/executed.txt', 'r')
        t = fr.readlines()
        for i in t:
            i = i[:-1].split()
            print('Received Executed task {} from {}'.format(i[0], i[1]))
        fr.close()
        os.system('rm /home/mec/deadlock_project/temp/executed.txt')
    except Exception as e:
        print('No Executed Tasks from MEC Received')


def run_me():
    global discovering
    global hosts

    initialization()
    while True:
        if len(hosts) == mec_no:
            print('MEC Details: ', hosts)
            del hosts[message()]
            discovering = 1
            break
        time.sleep(2)
    start_loop()


def start_loop():
    print('\n============* WELCOME TO THE DEADLOCK EMULATION PROGRAM *=============\n')
    while True:
        x = gp.getpass('Press any key to Start...').lower()
        if x != 'exit':
            for i in range(500):

                rms_list = get_rms()
                print('RMS List of Processes: ', rms_list, '\n')
                print('\nRunning Bankers Algorithm')
                list_seq = get_exec_seq(rms_list)
                if len(list_seq) > 0:              # do only when there is a task in safe sequence
                    wait_list = calc_wait_time(list_seq)
                    print('\nWaiting Time List: ', wait_list)
                    compare_result = compare_local_mec(wait_list)
                    print('\nExecute Locally: ', compare_result[1])
                    print('\nExecute in MEC: ', compare_result[0])
                    print('\nSending to cooperative platform')
                    if len(compare_result[0]) > 0:
                        cooperative_mec(compare_result[0], 1)
                    local_ = execute(compare_result[1])
                    if len(local_) > 0:            # do only when there is a task to send back
                        send_back_task(local_)
                receive_executed_task()
                time.sleep(3)
            print('\nEnter "Exit" to stop Programme!')
        if x == 'exit':
            print('\nProgramme Terminated')
            break


def initialization():
    global mec_no
    global host_ip
    global cloud_ip

    host_ip = ip_address()
    try:
        mec_no = int(input('Number of MECs: ').strip())
        cloud_ip = input('Cloud Server IP: ').strip()
        print('\nCompiling MEC Details')
        h1 = Thread(target=receive_message)
        h1.start()
        while True:
            b = input('Send Hello Message (Y/N): ').strip().lower()
            if b == 'y':
                send_message('hello')
                break
            else:
                print('\nPlease Type "y" to send Hello message\n')
    except KeyboardInterrupt:
        print('\nProgramme Terminated')
        exit(0)


def main():
    os.system('clear')
    run_me()


if __name__ == "__main__":
    main()

