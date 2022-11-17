from importlib import resources
import simpy
import numpy as np
import random
import matplotlib.pyplot as plt


env = simpy.Environment()
N_i = [100,150,50,150,80,40,250] #maximum capacity 
t_i = [0.1, 0.15, 0.1, 0.1, 0.15, 0.1, 0.2] #picking time
u_i = [60, 36, 42, 42, 30, 60, 90]  #refilltime
sections = [simpy.Container(env, 100, init =100 ), simpy.Container(env, 150, init =150 ), simpy.Container(env, 50, init =50 ), simpy.Container(env, 150, init =150 ), simpy.Container(env, 80, init =80 ), simpy.Container(env, 40, init =40 ), simpy.Container(env, 250, init =250 ) ]
employeeResources = [simpy.Resource(env,1),simpy.Resource(env,1),simpy.Resource(env,1),simpy.Resource(env,1),simpy.Resource(env,1),simpy.Resource(env,1),simpy.Resource(env,1)]
Counters = simpy.PreemptiveResource(env, 4) #er dette riktig? Var før kun Resource
simTime = 16*60
mosList = []
mosListAvg = []
nrEmployees = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
n_employees = 1
p_i = 0.05 * n_employees    #number of employees actually working, threshold value
lamda_c = 1/3
lambda_failure = 1/(4*60)
lambda_repair = 1/(15)
lambda_T_co = 1/2
lamda_t = 2
N_7 = 4
t_7s = 0.1
t_7p = 0.2
Q_time = []

#create random shopping list
def generateShoppingList():
    omega = []
    for i in range(0,7):
        x = random.randint(0,5)
        omega.append(x)
    while sum(omega) == 0:
        for i in range(0,7):
            x = random.randint(0,5)
            omega.append(x)
    return omega



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



#time it takes to walk inbetween sections       
def T_t():
    return np.random.exponential(1/lamda_t)


def Customer(env):
    omega = generateShoppingList()
    total_items2 = sum(omega)
    i = 0  
    items = 0
    items2 = 0
    while i < 7:
        yield env.timeout(T_t())
        if omega[i] > 0:
            if omega[i] <= sections[i].level: 
                yield sections[i].get(omega[i])
                yield env.timeout(omega[i]*t_i[i])
                items2 += omega[i]
                if i == 0:
                    items += 1
                elif i != 0:
                    items += omega[i]
        i += 1 
    with Counters.request() as req:
        queue_start = env.now
        yield req
        timestamp_2 = env.now
        T_q = timestamp_2-queue_start
        Q_time.append(T_q)
        yield env.timeout(np.random.exponential(1/lambda_T_co))
    



def Failure(env):

    with Counters.request(priority=0, preempt=True) as req:
        yield req
        yield env.timeout(np.random.exponential(1/lambda_repair)) 




def Employee(env):
    i = 0
    while i < 7:
        yield env.timeout(T_t())            
        if employeeResources[i].count < 1:
            with employeeResources[i].request() as req:
                yield req
                if sections[i].level < sections[i].capacity * p_i:
                    yield env.timeout(u_i[i])
                    yield sections[i].put(sections[i].capacity - sections[i].level)
                    #yield env.timeout(u_i[i])
        i += 1
        if i >= 7:
            i = 0

env.process(customerGenerator(env))
env.process(failureGenerator(env))
for y in range(1, n_employees):
    env.process(Employee(env))


env.run(until=simTime)

print(Q_time)

