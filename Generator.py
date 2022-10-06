from importlib import resources
import simpy
import numpy as np
import random
import matplotlib.pyplot as plt

list_avg_different_employees = []

for z in range(1,21):

    print(z)
    env = simpy.Environment()

    N_i = [100,150,50,150,80,40,250] #maximum capacity 
    t_i = [0.1, 0.15, 0.1, 0.1, 0.15, 0.1, 0.2] #picking time
    u_i = [60, 36, 42, 42, 30, 60, 90]  #refilltime
    sections = [simpy.Container(env, 100, init =100 ), simpy.Container(env, 150, init =150 ), simpy.Container(env, 50, init =50 ), simpy.Container(env, 150, init =150 ), simpy.Container(env, 80, init =80 ), simpy.Container(env, 40, init =40 ), simpy.Container(env, 250, init =250 ) ]
    employeeResources = [simpy.Resource(env,1),simpy.Resource(env,1),simpy.Resource(env,1),simpy.Resource(env,1),simpy.Resource(env,1),simpy.Resource(env,1),simpy.Resource(env,1)]
    Counters = simpy.Resource(env, 4)
    #Sections = simpy.Resource(env,6)
    simTime = 16*60
    mosList = []
    mosListAvg = []
    nrEmployees = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]


    n_employees = z
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
            new_customer = Customer(env)
            env.process(new_customer)
            yield env.timeout(np.random.exponential(1/lamda_c)) #maybe poison



    #time it takes to walk inbetween sections       
    def T_t():
        return np.random.exponential(1/lamda_t)


    def Customer(env):
        omega = generateShoppingList()
        total_items = sum(omega)
        i = 0  
        items = 0
        while i < 7:
            if omega[i] > 0:
                if omega[i] <= sections[i].level: 
                    yield sections[i].get(omega[i])
                    yield env.timeout(omega[i]*t_i[i])
                    items += omega[i]
                    
            yield env.timeout(T_t())
            i += 1 
        
        with Counters.request() as req:
            queue_start = env.now
            yield req
            timestamp_2 = env.now
            T_q = timestamp_2-queue_start
            if items > 0:
                yield env.timeout(t_7s*items)
                yield env.timeout(t_7p)

        v = items/total_items
        mosList.append(generateMos(v,T_q))
        #mosListAvg.append(sum(mosList)/len(mosList))           

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
    for y in range(1, n_employees):
        env.process(Employee(env))


    env.run(until=simTime)
    #print("MOS List Avg.:")
    #print(mosListAvg)
    #mosListAvg.append(sum(mosList)/len(mosList))
    list_avg_different_employees.append(sum(mosList)/len(mosList))


#print(list_avg_different_employees)

print("avg: ")
#print(mosListAvg)
print(list_avg_different_employees)

x = np.array(nrEmployees)
y = np.array(list_avg_different_employees)

plt.bar(x,y)
plt.xticks(x)


def addLabels(x,y):
    for i in range(0,20):
        
        plt.text(i+1,y[i]+0.05,round(y[i],3), ha = 'center')

addLabels(x,y)

plt.xlabel("Number of employees")
plt.ylabel("MOS")
plt.show()








