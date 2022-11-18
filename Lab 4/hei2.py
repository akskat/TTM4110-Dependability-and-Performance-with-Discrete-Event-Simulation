from importlib import resources
import simpy
import numpy as np
import random
import matplotlib.pyplot as plt


env = simpy.Environment()
Counters = simpy.PreemptiveResource(env, 4) #er dette riktig? Var før kun Resource
simTime = 500000 #number of employees actually working, threshold value
lamda_c = 1/3
lambda_failure = 4/(4*60)
lambda_repair = 1/(15)
lambda_T_co = 1/2
Q_time = []
availability_counter = []
down_time = 0
down_time_list = []

waitingtime_0_counter = []
waitingtime_1_counter = []
waitingtime_2_counter = []
waitingtime_3_counter = []
waitingtime_4_counter = []



#as long as true, create new customer object with interval 1/lamda_c
def customerGenerator(env):
    while True:
        new_customer = Customer(env)
        env.process(new_customer)
        yield env.timeout(np.random.exponential(1/lamda_c)) #maybe poison

def failureGenerator(env):
    while True:
        new_failure = Failure(env)
        env.process(new_failure)
        yield env.timeout(np.random.exponential(1/lambda_failure)) 


def Customer(env):
    with Counters.request() as req:
        queue_start = env.now
        yield req
        timestamp_2 = env.now
        T_q = timestamp_2-queue_start
        if (len(availability_counter) == 4):
            waitingtime_4_counter.append(T_q)
        if (len(availability_counter) == 3):
            waitingtime_3_counter.append(T_q)
        if (len(availability_counter) == 2):
            waitingtime_2_counter.append(T_q)
        if (len(availability_counter) == 1):
            waitingtime_1_counter.append(T_q)
        if (len(availability_counter) == 0):
            waitingtime_0_counter.append(T_q)

        Q_time.append(T_q)
        yield env.timeout(np.random.exponential(1/lambda_T_co))
        

def Failure(env):
    availability_counter.append(1)
    T_A1 = 0
    T_A2 = 0
    if (len(availability_counter) > 3):
        T_A1 = env.now
    with Counters.request(priority=0, preempt=True) as req:
        yield req
        yield env.timeout(np.random.exponential(1/lambda_repair)) 
    del availability_counter[0]
    if (len(availability_counter) >= 3):
        T_A2 = env.now
    T_A_total = T_A2 - T_A1
    down_time_list.append(T_A_total)


env.process(customerGenerator(env))
env.process(failureGenerator(env))

env.run(until=simTime)

#print(Q_time)
print("1")
avg_waiting_times = sum(Q_time)/len(Q_time)
print("Average: ", avg_waiting_times)
down_time = sum(down_time_list)
availability = (simTime-down_time)/simTime
print("Availability: ", availability)

print("2")
avg_1_counter = sum(waitingtime_1_counter)/len(waitingtime_1_counter)
avg_2_counter = sum(waitingtime_2_counter)/len(waitingtime_2_counter)
avg_3_counter = sum(waitingtime_3_counter)/len(waitingtime_3_counter)
avg_4_counter = sum(waitingtime_4_counter)/len(waitingtime_4_counter)
avg_5_counter = sum(waitingtime_0_counter)/len(waitingtime_0_counter)

#avg_counters_list = [avg_1_counter, avg_2_counter, avg_3_counter, avg_4_counter]
print("3")
print("Avg 1 counter out of service:")
print(avg_1_counter)
print("Avg 2 counters out of service:")
print(avg_2_counter)
print("Avg 3 counters out of service:")
print(avg_3_counter)
print("Avg 4 countersout of service:")
print(avg_4_counter)
print("4")

from datetime import datetime
x_values = [0,1,2,3,4]
y_values_python = [avg_5_counter, avg_1_counter, avg_2_counter, avg_3_counter, avg_4_counter]
y_values_analytical = [0.00304,0.02787,0.25,4, 15]


def plot_graph():
    plt.plot(x_values, y_values_python, color='r', label='Simulation')
    plt.plot(x_values, y_values_analytical, color='b', label='Analytical')
    plt.xticks([0, 1, 2, 3, 4]) 
    plt.tight_layout()
    plt.title("Waiting time as a function of number of failures")
    plt.xlabel("Number of failures")
    plt.ylabel("Waiting time in minutes")
    plt.legend()
    plt.show()

plot_graph()
print("Avg for 0")
avg0 = sum(waitingtime_0_counter)/len(waitingtime_0_counter)
print(avg0)





