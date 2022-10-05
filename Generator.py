import simpy
import numpy as np
import random

env = simpy.Environment()

N_i = [100,150,50,150,80,40,250] #maximum capacity 
t_i = [0.1, 0.15, 0.1, 0.1, 0.15, 0.1, 0.2] #picking time
u_i = [60, 36, 42, 42, 30, 60, 90]  #refilltime
sections = [simpy.Container(env, 100, init =100 ), simpy.Container(env, 150, init =150 ), simpy.Container(env, 50, init =50 ), simpy.Container(env, 150, init =150 ), simpy.Container(env, 80, init =80 ), simpy.Container(env, 40, init =40 ), simpy.Container(env, 250, init =250 ) ]
Counters = simpy.Resource(env, 4)
Sections = simpy.Resource(env,6)
simTime = 16*60
customer = 0
mosList = []


n_employees = 10
p_i = 0.05 * n_employees    #number of employees actually working, threshold value
lamda_c = 1/3
lamda_t = 2
N_7 = 4
t_7s = 0.1
t_7p = 0.2

#create random shopping list
def generateShoppingList():
    omega = []
    for i in range(0,7):
        x = random.randint(0,5)
        omega.append(x)
    print(omega)
    return omega

#return MOS number based on cicumstanses 
def generateMos(v, T_q):
    if (v==1) and (T_q==0):
        return 5
    
    if (v>0.9) and (T_q<0.3):
        return 4

    if (v>0.8) and (T_q<0.6):
        return 3
    
    if (v>0.7) and (T_q <1):
        return 2
    
    else:
        return 1

#as long as true, create new customer object with interval 1/lamda_c
def customerGenerator(env):
    #customer = 0
    while True:
        customer = Customer(env)
        yield env.timeout(np.random.exponential(1/lamda_c)) #maybe poison

    

#time it takes to walk inbetween sections       
def T_t():
    return np.random.exponential(1/lamda_t)


class Customer(object):
    def _init_(self,env):
        self.omega = generateShoppingList()
        total_items = sum(self.omega)
        self.i = 0  
        self.items = 0
        while self.i < 7:
            if self.omega[self.i]>0:
                if self.omega[self.i]<= sections[self.i].level: 
                    yield sections[self.i].get(self.omega[self.i])
                    yield self.timeout(self.omega[self.i]*t_i[self.i])
                    self.items+= self.omega[self.i]
                    yield self.timeout(T_t())
                    self.i+=1      
        
            with Counters.request() as req:
                queue_start = self.env.now
                yield req
                timestamp_2= self.env.now
                T_q = timestamp_2-queue_start
                if self.items > 0:
                    yield self.timeout(t_7s*self.items)
                    yield self.timeout(t_7p)

        v = self.items/total_items
        mosList.append(generateMos(v,T_q))      
                




class Employee(object):
    def _init_(self,env):
        self.i = 0
        while self.i < 7:
            yield self.timeout(T_t())
            with Sections.request() as req:
                yield req
                if sections[self.i].level < sections[self.i].capacity * p_i:
                    yield sections[self.i].put(sections[self.i].capacity - sections[self.i].level)
                    yield self.timeout(u_i[self.i])
                self.i += 1
                if self.i >= 7:
                    self.i = 0



generateShoppingList()



env.process(customerGenerator(env))

for y in range(1, n_employees):
    env.process(employee = Employee(env))
env.run(until=simTime)








