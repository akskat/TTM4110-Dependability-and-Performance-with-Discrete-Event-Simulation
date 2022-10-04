import simpy
import numpy as np
import random

N_i = [100,150,50,150,80,40,250] #maximum capacity 
t_i = [0.1, 0.15, 0.1, 0.1, 0.15, 0.1, 0.2] #picking time
u_i = [60, 36, 42, 42, 30, 60, 90]  #refilltime

lamda_c = 1/3
lamda_t = 2
N_7 = 4
t_7s=0.1
t_7p=0.2

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
    while True:
        customer = Customer(env)
        yield env.timeout(np.random.exponential(1/lamda_c))

#time it takes to walk inbetween sections       
def T_t():
    return np.random.exponential(1/lamda_t)


class Customer(object):
    def _init_(self,env):
        self.omega = generateShoppingList()
        self.i = 0
        self.items = 0
        while self.i < 7:
            if self.omega[self.i]>0:
                if self.omega[self.i]<= 10: #implement stock (simpy resource)
                    yield 
                    yield self.timeout(self.omega[self.i]*t_i[self.i])
                    self.items+= self.omega[self.i]
                    yield self.timeout(T_t())
                    self.i+=1
                        
        while self.items > 0:
            timestamp_1= self.env.now
            #implement aquire 
            timestamp_2= self.env.now
            T_q=timestamp_2-timestamp_1
            yield self.timeout(t_7s*self.items)
            yield self.timeout(t_7p)
            #implement release cashier

        #implement: hvis kunde ikke har handlet noe self.items==0

generateShoppingList()

env = simpy.Enviroment()
S_0 = simpy.Container(env, 100, init =100 )
S_1 = simpy.Container(env, 150, init =150 )
S_2 = simpy.Container(env, 50, init =50 )
S_3 = simpy.Container(env, 150, init =150 )
S_4 = simpy.Container(env, 80, init =80 )
S_5 = simpy.Container(env, 40, init =40 )
S_6 = simpy.Container(env, 250, init =250 )







