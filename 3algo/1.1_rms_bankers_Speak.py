# Author Emeka Ugwuanyi Emmanuel

from functools import reduce
from sys import *
import numpy as np
import random as r
import ping_code as pc
import socket
import struct
import subprocess as sp
from threading import Thread
import threading
import ast
import time
import os
import psutil
import datetime as dt
import getpass as gp
import paho.mqtt.client as mqtt
from netifaces import interfaces, ifaddresses, AF_INET
import smtplib
import config
import paramiko

hosts = {}  # {hostname: ip}

_tasks = {'t1': {'wcet': 3, 'period': 20, 'deadline': 15},
          't2': {'wcet': 1, 'period': 5, 'deadline': 4},
          't3': {'wcet': 2, 'period': 10, 'deadline': 8},
          't4': {'wcet': 1, 'period': 10, 'deadline': 9},
          't5': {'wcet': 3, 'period': 15, 'deadline': 12}
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

_cpu = []  # cpu plot list
prev_t = 0  # variable for cpu util
_off_mec = 0  # used to keep a count of tasks offloaded from local mec to another mec
_off_cloud = 0  # used to keep a count of tasks offloaded to cloud
_loc = 0  # used to keep a count of tasks executed locally
_inward_mec = 0  # used to keep a count of tasks offloaded from another mec to local mec
deadlock = [1]  # keeps count of how many deadlock is resolved
mec_waiting_time = {}  # {ip : [moving (waiting time + rtt)]}
memory = []
mec_rtt = {}  # {ip: [RTT]}

offload_register = {}  # {task: host_ip} to keep track of tasks sent to mec for offload
reoffload_list = [[], {}]  # [[task_list],{wait_time}] => records that’s re-offloaded to mec to execute.
discovering = 0  # if discovering == 0 update host
test = []
_time = []
_pos = 0
# received_task_queue = []   # [[(task_list,wait_time), host_ip], ....]
received_task_queue = []  # [(task_list,wait_time), ....]
received_time = []
thread_record = []
port = 65000
_port_ = 64000
cloud_register = {}  # ={client_id:client_ip} keeps address of task offloaded to cloud
cloud_port = 63000
stop = 0
t_track = 1
task_record = {}     # keeps record of task reoffloaded
task_id = 0          # id for each task reoffloaded
shared_resource_lock = threading.Lock()


def discovering_group():
    global sock1

    multicast_group = '224.3.29.71'
    server_address = ('', 10000)

    # Create the socket
    sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind to the server address
    sock1.bind(server_address)
    # Tell the operating system to add the socket to the multicast group
    # on all interfaces.
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock1.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


def offloading_group():
    global sock2

    multicast_group = '224.5.5.55'
    server_address = ('', 20000)

    # Create the socket
    sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Bind to the server address
    sock2.bind(server_address)
    # Tell the operating system to add the socket to the multicast group
    # on all interfaces.
    group = socket.inet_aton(multicast_group)
    mreq = struct.pack('4sL', group, socket.INADDR_ANY)
    sock2.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)


def ip_address():
    try:
        cmd = ['ifconfig eth1 | grep inet | cut -d ":" -f 2 | cut -d " " -f 1']
        address = str(sp.check_output(cmd, shell=True), 'utf-8')[0:-1]
        if len(address.strip().split('.')) == 4:
            return address.strip()
        else:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception as e:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]


def _memory():
    global memory

    memory.append(round(algo.memory_percent(), 4))


def get_mec_rtts():
    for i in mec_rtt:
        mec_rtt[i].append(get_rtt(i))


def m_cpu():
    global prev_t

    # get cpu
    next_t = psutil.cpu_percent(percpu=False)
    delta = abs(prev_t - next_t)
    prev_t = next_t
    _cpu.append(round(delta, 4))


def generate_results():
    _memory()
    m_cpu()
    get_mec_rtts()


def host_ip_set():
    global ip_set

    ip_set = set()
    for ifaceName in interfaces():
        addresses = [i['addr'] for i in ifaddresses(ifaceName).setdefault(AF_INET, [{'addr': 'No IP addr'}])]
        ip_set.add(', '.join(addresses))


def get_time():
    _time_ = []
    d = str(dt.datetime.utcnow()).split()
    _time_ += d[0].split('-')
    g = d[1].split('.')
    _time_ += g[0].split(':')
    _time_.append(g[1])
    return _time_


def get_rtt(host):
    rtt = pc.verbose_ping(host)
    if rtt:
        return round(rtt, 4)
    else:
        return get_rtt(host)


def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)


def _lcm(a, b):
    return int(a * b / gcd(a, b))


def lcm(_list):
    return reduce(_lcm, _list)


def gosh_dist(_range):
    return ((23 ** r.randrange(1, 1331)) % r.randrange(1, 1777)) % _range


def on_connect(connect_client, userdata, flags, rc):
    # print("Connected with Code :" +str(rc))
    # Subscribe Topic from here
    connect_client.subscribe(node_id, )
    connect_client.subscribe('mec')


# Callback Function on Receiving the Subscribed Topic/Message
def on_message(message_client, userdata, msg):
    data = str(msg.payload, 'utf-8')
    if data[0] == 'c':  # receive from cloud
        received_task = data[2:]
        # send_client({received_task: get_time()}, cloud_register[received_task.split('.')[2]])
        if received_task in task_record:
            del task_record[received_task]
            received_task = '.'.join(received_task.split('.')[:-1])
            _client.publish(topic=received_task.split('.')[2], payload=str({received_task: get_time()+['cloud']}), )
            cooperate['cloud'] += 1
            count_task_sent(received_task)

    elif data[0] == 't':  # receive from client
        received_task = ast.literal_eval(data[2:])
        received_task_queue.append(received_task)
        received_time.append(time.time())
    '''
    else:
        print('data: ', data)

    elif data[0] == 't':
        print('send: ', data[2:])
    '''


def connect_to_broker():
    global _client
    global broker_ip
    global topic

    username = 'mec'
    password = 'password'
    broker_ip = 'localhost'
    broker_port_no = 1883
    topic = 'mec'  # topic used to exchange mec details to clients

    _client = mqtt.Client()
    _client.on_connect = on_connect
    _client.on_message = on_message

    _client.username_pw_set(username, password)
    _client.connect(broker_ip, broker_port_no, 60)
    _client.loop_forever()


def task_time_map(seq, process):
    exe_seq = []
    capacity_sum = 0
    for job in process:
        capacity_sum += process[job]['wcet']
    while capacity_sum > 0:
        for job in seq:
            if process[job]['wcet'] > 0:
                exe_seq.append(job)
                process[job]['wcet'] -= 1
                capacity_sum -= 1

    return exe_seq


def load_tasks():
    period_list = [tasks[i]['period'] for i in tasks]

    lcm_period = lcm(period_list)
    # insert idle task
    s_task = {**tasks, 'idle': {'wcet': lcm_period, 'period': lcm_period + 1}}
    return lcm_period, s_task


total_received_task = 0


def scheduler(_lcm_, s_tasks):  # RMS algorithm
    global total_received_task
    queue = list(s_tasks.keys())  # initialize task queue
    schedule = []
    rms = []
    curr = ''  # current task
    prev = ''  # previous task
    tmp = {}
    for task in s_tasks.keys():
        tmp[task] = {}  # temporary data for each task
        tmp[task]['deadline'] = s_tasks[task]['period']
        tmp[task]['executed'] = 0

    # start scheduling...
    # proceed by one timestamp to handle preemption
    for _time_ in range(_lcm_):
        # insert new tasks into the queue
        for t in tmp.keys():
            if _time_ == tmp[t]['deadline']:
                if s_tasks[t]['wcet'] > tmp[t]['executed']:
                    # print('Scheduling Failed at %d' % time)
                    exit(1)
                else:
                    tmp[t]['deadline'] += s_tasks[t]['period']
                    tmp[t]['executed'] = 0
                    queue.append(t)
        # select next task to be scheduled
        _min_ = _lcm_ * 2
        for task in queue:
            if tmp[task]['deadline'] < _min_:
                _min_ = tmp[task]['deadline']
                curr = task
        tmp[curr]['executed'] += 1
        # print(time, queue, curr)

        # dequeue the execution-completed task
        if tmp[curr]['executed'] == s_tasks[curr]['wcet']:
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
            schedule.append([_time_, curr])
            if curr != 'idle':
                rms.append(curr)
        prev = curr
    process = {task: {'wcet': tasks[task]['wcet']} for task in tasks}
    rms = task_time_map(seq=rms, process=process)
    total_received_task += len(rms)
    return rms


# generate execution sequence  using banker's algorithm
def is_safe(processes, avail, _need_, allot, p):  # bankers algorithm
    need = [_need_[i] for i in _need_]
    _allot_ = [allot[i] for i in allot]
    # tasks to offload if exit
    offload = []

    # Number of resources
    res = 3

    # Mark all processes as unfinished
    finish = [0] * p

    # To store safe sequence
    safe_seq = [0] * p

    # Make a copy of available resources
    work = [0] * res
    for i in range(res):
        work[i] = avail[i]

        # While all processes are not finished
    # or system is not in safe state.
    count = 0
    while count < p:

        # Find a process which is not finish
        # and whose needs can be satisfied
        # with current work[] resources.
        found = False
        for t in range(p):

            # First check if a process is finished,
            # if no, go for next condition
            if finish[t] == 0:

                # Check if for all resources
                # of current P need is less
                # than work
                for j in range(res):
                    if need[t][j] > work[j]:
                        break

                # If all needs of p were satisfied.
                if j == res - 1:

                    # Add the allocated resources of
                    # current P to the available/work
                    # resources i.e.free the resources
                    for k in range(res):
                        work[k] += _allot_[t][k]

                        # Add this process to safe sequence.
                    safe_seq[count] = processes[t]
                    count += 1

                    # Mark this p as finished
                    finish[t] = 1

                    found = True

        # If we could not find a next process
        # in safe sequence.
        if not found:
            print("System is not in safe state")

            a = list(set(processes) - set(safe_seq) - set(offload))
            _max = np.array([0, 0, 0])
            n = {}
            for i in a:
                n[i] = sum(allocation[i[:2]])
            _max = max(n, key=n.get)
            print('work: ', work, 'need: ', _need[_max[:2]])
            offload.append(_max)
            work = np.array(work) + np.array(allocation[_max[:2]])
            count += 1

            # Mark this p as finished
            finish[processes.index(_max)] = 1
            found = True

    # If system is in safe state then
    # safe sequence will be as below
    if len(offload) > 0:
        safe_seq = safe_seq[:safe_seq.index(0)]
        print('offloading tasks: ', offload)
        cooperative_mec(offload)
        deadlock[0] += 1
    print("System is in safe state.",
          "\nSafe sequence is: ", end=" ")
    print('safe seq: ', safe_seq)

    return safe_seq


def get_exec_seq(pro):
    # Number of processes
    p = len(pro)

    processes = ['{}_{}'.format(pro[i], i) for i in range(len(pro))]

    # Available instances of resources
    avail = [6, 5, 5]
    n_need = {i: _need[i[:2]] for i in processes}
    # print('need', n_need)
    # Resources allocated to processes
    allot = {i: allocation[i[:2]] for i in processes}

    # return execution sequence
    return is_safe(processes, avail, n_need, allot, p)


def calc_wait_time(list_seq):
    pre = 0
    time_dic = {}
    for i in list_seq:
        j = i.split('_')[0]
        time_dic[i] = round(t_time[j][0] + pre, 3)
        pre += t_time[j][0]
    # waiting time = total waiting time ÷ 2 average waiting time might be too tight
    w_send = round(time_dic[list(time_dic.keys())[-1]] / 2, 3)
    send_message('wt {} {}'.format(ip_address(), str(w_send)))  # multi-casting waiting time to cooperative MECs
    return time_dic

timed_out_tasks  = 0
def compare_local_mec(list_seq):
    global received_time, timed_out_tasks
    execute_mec = []
    execute_locally = []
    diff = time.time() - received_time.pop(0)
    checking_times = {}
    for i in list_seq:
        t_time[i.split('_')[0]][1]-=diff
        # if t_time[i.split('_')[0]][1] < 0:
        #     _client.publish(i.split('_')[0].split('.')[2], str({i.split('_')[0]: get_time() + ['local']}), )
        #     timed_out_tasks += 1
        if t_time[i.split('_')[0]][1] > list_seq[i]:
            execute_locally.append(i)
        else:
            execute_mec.append(i)
            checking_times[i] = {'Latency': t_time[i.split('_')[0]][1], 'Expected_exec_time': list_seq[i]}
    print('Execution time comparison:= ', checking_times)
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
    return round(avg1, 4)


def algo_id():
    no = int(os.path.basename(__file__)[0])
    if no <= 2:
        return 2
    elif no <= 4:
        return 3
    elif no <= 7:
        return 7
    elif no <= 10:
        return 10
    elif no <= 13:
        return 12
    else:
        return 16


def send_message(mg):
    _multicast_group = ('224.3.29.71', 10000)
    try:

        # Send data to the multicast group
        if mg == 'hello':
            smg = mg + ' ' + str(['speaker', ip_address()])
            sock1.sendto(str.encode(smg), _multicast_group)
            print('\nHello message sent')
        elif mg == 'update':
            ho = hosts.copy()
            ho['speaker'] = host_ip
            smg = mg + ' ' + str(ho)
            sock1.sendto(str.encode(smg), _multicast_group)
            send_message('client')
            # print('\n===**====**==update message sent===**======**=========')
        elif mg == 'client':
            ho = hosts.copy()
            ho[get_hostname()] = host_ip
            smg = f'm {ho}_{algo_id()}'
            _client.publish(topic, smg, retain=True)
        else:
            sock1.sendto(str.encode(mg), _multicast_group)

    except Exception as e:
        print(e)


def get_hostname():
    cmd = ['cat /etc/hostname']
    hostname = str(sp.check_output(cmd, shell=True), 'utf-8')[0:-1]
    return hostname


def receive_message():
    global hosts

    while True:
        if stop == 1:
            print('Stopped : receive_message()')
            break
        else:
            data, address = sock1.recvfrom(1024)
            _d = data.decode()
            if _d[:5] == 'hello':
                _data = ast.literal_eval(_d[6:])
                hosts[_data[0]] = _data[1]
                # print('received: ', hosts)
                if _data[1] != host_ip:
                    mec_rtt[_data[1]] = []

            elif (_d[:6] == 'update') and (discovering == 0):
                hosts = ast.literal_eval(_d[7:])
                # print('received: ', hosts)
                for i in hosts:
                    if i != host_ip:
                        mec_rtt[i] = []

            elif _d[:2] == 'wt':
                split_data = _d.split()
                if split_data[1] != host_ip:
                    w_time = calculate_mov_avg(split_data[1], float(split_data[2]) + get_rtt(
                        address[0]))  # calcuate moving average of mec wait time => w_time = wait time + rtt

                    if split_data[1] in mec_waiting_time:
                        mec_waiting_time[split_data[1]].append(w_time)
                    else:
                        mec_waiting_time[split_data[1]] = [w_time]

            elif data.decode().strip() == 'user':
                send_message('update')


def mec_comparison():
    # returns min average waiting for all mecs
    if len(mec_waiting_time) == 0:
        return 0
    min_mec = {i: mec_waiting_time[i][-1] for i in mec_waiting_time}
    min_wt = min(min_mec, key=min_mec.get)
    return min_wt


def cooperative_mec(mec_list):
    global _off_cloud
    global _off_mec
    global task_id, task_record

    for i in mec_list:
        _host = mec_comparison()
        if _host == 0:
            # send_cloud([i.split('_')[0], t_time[i.split('_')[0]][0]])  # [task_id,exec_time]
            _send_task = f"{i.split('_')[0]}.{task_id}"
            _client.publish(cloud_ip, str([_send_task, t_time[i.split('_')[0]][0]]), )
            task_record[_send_task] = 'cloud'
            task_id += 1
            _off_cloud += 1
            # cloud_register[i.split('_')[0].split('.')[2]] = send_back_host

            print('\n=========SENDING {} TO CLOUD==========='.format(i))

        else:
            j = i.split('_')[0]
            _max = np.array([6, 5, 5])
            send = 'false'
            if not (False in list(np.greater_equal(_max, _need[j[:2]]))):
                send = 'true'
            # CHECK IF THE MINIMUM MEC WAIT TIME IS LESS THAN LATENCY
            if mec_waiting_time[_host][-1] < t_time[j][1] and send == 'true':
                _send_task = f"{j}.{task_id}"
                send_offloaded_task_mec('{} {} {}'.format('ex', mec_id(_host), [_send_task, t_time[j][0]]))
                task_record[_send_task] = 'mec'
                task_id += 1
                _off_mec += 1
                # SENDS TASK TO MEC FOR EXECUTION

                w_send = mec_waiting_time[_host][-1] + 0.001
                mec_waiting_time[_host].append(w_send)  # adds a new average waiting time
                print('\n======SENDING {} TO MEC {}========='.format(i, _host))
            elif send == 'true' and (get_rtt(_host) < get_rtt(cloud_ip)):
                _send_task = f"{j}.{task_id}"
                send_offloaded_task_mec('{} {} {}'.format('ex', mec_id(_host), [_send_task, t_time[j][0]]))
                task_record[_send_task] = 'mec'
                task_id += 1
                _off_mec += 1
                # SENDS TASK TO MEC FOR EXECUTION
                w_send = mec_waiting_time[_host][-1] + 0.001
                mec_waiting_time[_host].append(w_send)  # adds a new average waiting time
                print('\n======SENDING {} TO MEC {}========='.format(i, _host))

            else:
                _send_task = f"{j}.{task_id}"
                _client.publish(cloud_ip, str([_send_task, t_time[j][0]]), )
                task_record[_send_task] = 'cloud'
                task_id += 1
                _off_cloud += 1
                # send_cloud([j, t_time[j][0]])    # # [task_id,exec_time]

                # cloud_register[j.split('.')[2]] = send_back_host

                print('\n=========SENDING {} TO CLOUD==========='.format(i))


outward_mec = 0
offload_check = [0,0]
def execute_re_offloaded_task(offloaded_task):
    global outward_mec, offload_check
    exec_list = get_exec_seq(offloaded_task[0])
    # if len(exec_list) != len(offloaded_task[0]):
    #     print('\n\n', '@ ' * 50)
    #     print('exec: ', exec_list, 'off: ', offloaded_task[0])
    #     print('\n\n', '@ ' * 50)
    #     offload_check.append((exec_list, offloaded_task[0]))
    outward_mec += len(exec_list)
    for i in offloaded_task[0]:  # i = 't1.1.2.3*1_3'
        j = i.split('_')[0]
        time.sleep(offloaded_task[1][j] / 2)
        # print('j task: ', j)
        send_offloaded_task_mec('{} {}'.format(j.split('.')[1], i.split('*')[0]))

clients_record = {}


def count_task_sent(task):
    global clients_record
    c_id = task.split('.')[2]
    if c_id in clients_record:
        clients_record[c_id] += 1
    else:
        clients_record[c_id] = 1


def execute(local):
    print('\nExecuting :', local)

    for i in local:
        j = i.split('_')[0]
        _t = t_time[j][0] / 2
        time.sleep(_t)
        print('#{}'.format(local.index(i) + 1), ' Executed: ', i)
        _client.publish(j.split('.')[2], str({j: get_time() + ['local']}), )
        count_task_sent(j)
        # if j.split('.')[1] != node_id:
        #     send_offloaded_task_mec('{} {}'.format(j.split('.')[1], j))
        #     outward_mec += 1
        # elif j.split('.')[1] == node_id:
        #     # send_client({j: get_time()}, send_back_host)
        #     _client.publish(j.split('.')[2], str({j: get_time()+['local']}), )
        #     count_task_sent(j)
        #     _loc += 1
        # else:
        #     print('else execute: ', j)
    print('============== EXECUTION DONE ===============')


cooperate = {'mec': 0, 'cloud': 0}


def receive_offloaded_task_mec():  # run as a thread
    global _inward_mec
    global t_track

    while True:
        if stop == 1:
            print('Stopped: receive_offloaded_task_mec()')
            break
        else:
            data, address = sock2.recvfrom(1024)
            if len(data.decode()) > 0:
                da = data.decode().split(' ')
                if (address[0] not in ip_set) and (da[0] == node_id):  # send back to client
                    # send_client({da[1]: get_time()}, offload_register[da[1]])     # send back to client
                    if da[1] in task_record:
                        del task_record[da[1]]
                        task_new = '.'.join(da[1].split('.')[:-1])
                        _client.publish(da[1].split('.')[2], str({task_new: get_time()+['mec']}), )
                        count_task_sent(da[1])
                        cooperate['mec'] += 1
                    else:
                        print('*'*30 + f'\n{da[1]} Not in Task Record\n' + '*'*30)
                elif (address[0] not in ip_set) and (da[0] == 'ex') and (da[1] == node_id):
                    _received = ast.literal_eval(da[2] + da[3])
                    shared_resource_lock.acquire()
                    task = _received[0] + '*{}'.format(t_track)
                    reoffload_list[0].append(task)
                    reoffload_list[1][task] = _received[1]
                    shared_resource_lock.release()
                    t_track += 1
                    _inward_mec += 1


def call_execute_re_offload():
    global reoffload_list, outward_mec
    global offload_check

    while True:
        if stop == 1:
            print('Stopped: call_execute_re_offload()')
            break
        else:
            if len(reoffload_list[0]) == 1:
                t = reoffload_list[0][-1]
                time.sleep(reoffload_list[1][t] / 2)
                shared_resource_lock.acquire()
                reoffload_list[0].remove(t)
                del reoffload_list[1][t]
                shared_resource_lock.release()
                send_offloaded_task_mec('{} {}'.format(t.split('.')[1], t.split('*')[0]))
                outward_mec += 1
                offload_check[0] += 1
            elif len(reoffload_list[0]) > 1:
                o = reoffload_list.copy()
                offload_check[1] += len(o)
                execute_re_offloaded_task(o)
                for i in o[0]:
                    shared_resource_lock.acquire()
                    reoffload_list[0].remove(i)
                    del reoffload_list[1][i]
                    shared_resource_lock.release()


def send_email(msg):
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com')
        server.ehlo()
        server.login(config.email_address, config.password)
        subject = 'Deadlock results rms+bankers {}'.format(get_hostname())
        # msg = 'Attendance done for {}'.format(_timer)
        _message = 'Subject: {}\n\n{}\n\n SENT BY RIHANNA \n\n'.format(subject, msg)
        server.sendmail(config.email_address, config.send_email, _message)
        server.quit()
        print("Email sent!")
    except Exception as e:
        print(e)


def send_offloaded_task_mec(msg):
    _multicast_group = ('224.5.5.55', 20000)
    try:
        sock2.sendto(str.encode(msg), _multicast_group)

    except Exception as e:
        print(e)


def send_result(host_, data):
    try:
        c = paramiko.SSHClient()

        un = 'mec'
        pw = 'password'
        s_port = 22

        c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        c.connect(host_, s_port, un, pw)
        for i in data:
            cmd = ('echo "{}" >> /home/mec/result/data.py'.format(i))  # task share : host ip task
            stdin, stdout, stderr = c.exec_command(cmd)
        c.close()
    except Exception as e:
        print(e)


def mec_id(client_ip):
    _id = client_ip.split('.')[-1]
    if len(_id) == 1:
        return '00' + _id
    elif len(_id) == 2:
        return '0' + _id
    else:
        return _id


def run_me():
    global discovering

    initialization()
    while True:
        if len(hosts) == mec_no:
            print('MEC Details: ', hosts)
            del hosts['speaker']
            discovering = 1
            break
        time.sleep(2)
    speak = Thread(target=speaking_node)
    thread_record.append(speak)
    speak.daemon = True
    speak.start()
    start_loop()


def save_and_email():
    _id_ = get_hostname()[-1]
    result = f"\nwt{_id_}_2_{mec_no} = {mec_waiting_time} " \
             f"\nrtt{_id_}_2_{mec_no} = {mec_rtt} \ncpu{_id_}_2_{mec_no} = {_cpu} " \
             f"\noff_mec{_id_}_2_{mec_no} = {_off_mec} " \
             f"\noff_cloud{_id_}_2_{mec_no} = {_off_cloud} " \
             f"\ninward_mec{_id_}_2_{mec_no} = {_inward_mec}" \
             f"\nloc{_id_}_2_{mec_no} = {_loc} " \
             f"\ndeadlock{_id_}_2_{mec_no} = {deadlock} \nmemory{_id_}_2_{mec_no} = {memory}" \
             f"\ntask_received = {total_received_task} \nsent_t = {clients_record}" \
             f"\ncooperate{_id_}_2_{mec_no} = {cooperate} \ntask_record{_id_}_2_{mec_no} = {task_record}" \
             f"\noutward_mec{_id_}_2_{mec_no} = {outward_mec}" \
             f"\noffload_check{_id_}_2_{mec_no} = {offload_check}" \
             f"\ntimed_out_tasks{_id_}_2_{mec_no} = {timed_out_tasks}\n"
    list_result = [
        f"\nwt{_id_}_2_{mec_no} = {mec_waiting_time} ",
        f"\nrtt{_id_}_2_{mec_no} = {mec_rtt} \ncpu{_id_}_2_{mec_no} = {_cpu} ",
        f"\noff_mec{_id_}_2_{mec_no} = {_off_mec} \noff_cloud{_id_}_2_{mec_no} = {_off_cloud} ",
        f"\ninward_mec{_id_}_2_{mec_no} = {_inward_mec}",
        f"\nloc{_id_}_2_{mec_no} = {_loc} ",
        f"\ndeadlock{_id_}_2_{mec_no} = {deadlock} \nmemory{_id_}_2_{mec_no} = {memory}",
        f"\ntask_received{_id_}_2_{mec_no} = {total_received_task} \nsent_t{_id_}_2_{mec_no} = {clients_record}",
        f"\ncooperate{_id_}_2_{mec_no} = {cooperate} \ntask_record{_id_}_2_{mec_no} = {task_record} "
        f"\noutward_mec{_id_}_2_{mec_no} = {outward_mec}",
        f"\noffload_check{_id_}_2_{mec_no} = {offload_check}",
        f"\ntimed_out_tasks{_id_}_2_{mec_no} = {timed_out_tasks}"
    ]
    path_ = 'data/raw/'
    if os.path.exists(path_):
        cmd = f"echo '' > {path_}{_id_}_2_{mec_no}datal.py"
        os.system(cmd)
        cmd = f"echo '' > {path_}{_id_}_2_{mec_no}datap.py"
        os.system(cmd)
    else:
        os.mkdir(path_)
        cmd = f"echo '' > {path_}{_id_}_2_{mec_no}datal.py"
        os.system(cmd)
        cmd = f"echo '' > {path_}{_id_}_2_{mec_no}datap.py"
        os.system(cmd)

    file_ = open(f'{path_}{_id_}_2_{mec_no}datap.py', 'w')
    for i in list_result:
        cmd = f'echo "{i}" >> {path_}{_id_}_2_{mec_no}datal.py'
        file_.write(i)
        os.system(cmd)
    file_.close()
    sp.run(
        ["scp", f"{path_}{_id_}_2_{mec_no}datap.py", f"mec@{hosts['osboxes-0']}:/home/mec/result/python"])
    sp.run(
        ["scp", f"{path_}{_id_}_2_{mec_no}datal.py", f"mec@{hosts['osboxes-0']}:/home/mec/result/linux"])

    send_result(hosts['osboxes-0'], list_result)
    send_email(result)
    if len(task_record) > 0:
        for _task_ in task_record:
            task_new = '.'.join(_task_.split('.')[:-1])
            _client.publish(task_new.split('.')[2], str({task_new: get_time()+[task_record[_task_]]}), )


def start_loop():
    global _loc
    global tasks
    global t_time
    global node_id
    global stop

    print('\n============* WELCOME TO THE DEADLOCK EMULATION PROGRAM *=============\n')

    node_id = mec_id(ip_address())
    # print('node id: ', node_id)
    _threads_ = [receive_offloaded_task_mec, call_execute_re_offload, connect_to_broker]
    for i in _threads_:
        Thread(target=i).daemon = True
        Thread(target=i).start()
    time.sleep(2)
    send_message('client')  # send mec details to clients
    # print('algo_id: ', algo_id())
    x = gp.getpass('Press any key to Start...').lower()
    if x != 'exit':
        print('========= Waiting for tasks ==========')
        _time_ = dt.datetime.now()
        while True:
            try:
                if len(received_task_queue) > 0:
                    info = received_task_queue.pop(0)
                    tasks, t_time = info

                    print('RMS List of Processes: ', tasks, '\n')

                    print('\n========= Running Deadlock Algorithm ===========')
                    lcm_result, task_load = load_tasks()
                    list_seq = get_exec_seq(scheduler(lcm_result, task_load))
                    if len(list_seq) > 0:  # do only when there is a task in safe sequence
                        wait_list = calc_wait_time(list_seq)
                        print('\nWaiting Time List: ', wait_list)
                        compare_result = compare_local_mec(wait_list)
                        print('\nExecute Locally: ', compare_result[1])
                        _loc += len(compare_result[1])  # total number of tasks to be executed locally
                        print('\nExecute in MEC: ', compare_result[0])

                        if len(compare_result[0]) > 0:
                            print('\nSending to cooperative platform')
                            cooperative_mec(compare_result[0])
                        execute(compare_result[1])
                        generate_results()
                    _time_ = dt.datetime.now()
                else:
                    send_message(str('wt {} 0.0'.format(ip_address())))
                    time.sleep(0.4)
                    now = dt.datetime.now()
                    delta = now - _time_
                    if delta > dt.timedelta(minutes=4):
                        print('terminating programme 3 mins elapsed')
                        save_and_email()
                        stop += 1
                        '''
                        for i in thread_record:
                            i.join()
                        '''
                        _client.loop_stop()
                        time.sleep(1)
                        print('done')
                        os.system('kill -9 {}'.format(os.getpid()))
                        break

            except KeyboardInterrupt:
                print('\nProgramme Terminated')
                save_and_email()
                stop += 1
                '''
                for i in thread_record:
                    i.join()
                '''
                _client.loop_stop()
                time.sleep(1)
                print('done')
                os.system('kill -9 {}'.format(os.getpid()))
                break


def speaking_node():
    global mec_no

    while True:
        if len(hosts) > (mec_no - 1):
            send_message('update')
            mec_no = len(hosts) + 1
        time.sleep(2)


def initialization():
    global mec_no
    global host_ip
    global cloud_ip

    host_ip = ip_address()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    print('Broker IP: ', s.getsockname()[0])
    try:
        mec_no = int(input('Number of MECs: ').strip())
        cloud_ip = input('Cloud Server IP: ').strip()
        print('\nCompiling MEC Details')
        h1 = Thread(target=receive_message)
        h2 = Thread(target=receive_offloaded_task_mec)
        h1.daemon = True
        h2.daemon = True
        h1.start()
        h2.start()
        time.sleep(1.5)
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
    global algo

    os.system('clear')
    print('mec ip: ', ip_address())
    algo = psutil.Process()
    discovering_group()
    offloading_group()
    host_ip_set()
    run_me()


if __name__ == "__main__":
    main()
