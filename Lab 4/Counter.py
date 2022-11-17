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

avg_waiting_times = sum(Q_time)/len(Q_time)
print("Average: ", avg_waiting_times)
down_time = sum(down_time_list)
availability = (simTime-down_time)/simTime
print("Availability: ", availability)


