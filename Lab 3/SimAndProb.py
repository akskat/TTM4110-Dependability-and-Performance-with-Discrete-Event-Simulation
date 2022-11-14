from importlib import resources
import simpy
import numpy as np
import random
import matplotlib.pyplot as plt

simulation_avg = []
lists_of_simulations = []
print("If the code gives a divided by zero error; run again")
for z in range(1,21):
    list_avg_different_employees = []
    print(z , "employees: 30 simulations")
    for i in range(1,31):
        env = simpy.Environment()
        N_i = [100,150,50,150,80,40,250] #maximum capacity 
        t_i = [0.1, 0.15, 0.1, 0.1, 0.15, 0.1, 0.2] #picking time
        u_i = [60, 36, 42, 42, 30, 60, 90]  #refilltime
        sections = [simpy.Container(env, 100, init =100 ), simpy.Container(env, 150, init =150 ), simpy.Container(env, 50, init =50 ), simpy.Container(env, 150, init =150 ), simpy.Container(env, 80, init =80 ), simpy.Container(env, 40, init =40 ), simpy.Container(env, 250, init =250 ) ]
        employeeResources = [simpy.Resource(env,1),simpy.Resource(env,1),simpy.Resource(env,1),simpy.Resource(env,1),simpy.Resource(env,1),simpy.Resource(env,1),simpy.Resource(env,1)]
        Counters = simpy.Resource(env, 4)
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
            while sum(omega) == 0:
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
                if items > 0:
                    yield env.timeout(t_7s * items)
                    yield env.timeout(t_7p)
            v = items2/total_items2
            mosList.append(generateMos(v,T_q))           

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
        list_avg_different_employees.append(sum(mosList)/len(mosList))
    simulation_avg.append(sum(list_avg_different_employees)/len(list_avg_different_employees))
    lists_of_simulations.append(list_avg_different_employees)


print("avg per employee after 20 simulations: ")
print(simulation_avg)




def calculate_Mos(v):
    if (v==1):
        return 5
    if (v>0.9):
        return 4
    if (v>0.8):
        return 3
    if (v>0.7):
        return 2
    else:
        return 1

avg_mos_employee = [0]

# when number of employees is more than 18 the results gets unstable therefore we only go up to 18
for emp in range(1, 19):
    lambda_p=1
    #n_employees = emp
    p_i = 0.05 * emp 
    N_i = [100, 150, 50, 150, 80, 40, 250]
    u_i = [60, 36, 42, 42, 30, 60, 90]
    list_mos_sections = []

    for i in range(0, 7):
        my = emp/u_i[i]
        #special case for section 5 where the threshold value is 2 and number of employeers are 1
        if (i == 5) and (emp == 1):
            lambda_0 = lambda_p / ( N_i[i] - (p_i * N_i[i]) )
            p_0 = lambda_0 / (lambda_0 + my) 

            #v= 1 - p_0
            #MOS_score = calculate_Mos(v)
            #average.append(MOS_score)

        #all the other sections
        else:
            lambda_0 = lambda_p / ( (p_i * N_i[i]) - 2 )
            lambda_1 = lambda_p / ( N_i[i] - (p_i * N_i[i]) )
            p_0 = (lambda_0 * lambda_1 / ((lambda_0 * lambda_1) + (lambda_0 * my) + (lambda_1 * my) + my**(2)))

        v = round((1 - p_0),2)
        MOS_score = calculate_Mos(v)
        list_mos_sections.append(MOS_score)

        
    avg_mos = sum(list_mos_sections)/len(list_mos_sections)
    avg_mos_employee.append(avg_mos)

print(avg_mos_employee)

def bar_plot_graph():
    x = np.array(nrEmployees)
    y = np.array(simulation_avg)
    plt.bar(x,y)
    plt.xticks(x)
    def addLabels(x,y):
        for i in range(0,20):
            plt.text(i+1,y[i]+0.05,round(y[i],2), ha = 'center')
    addLabels(x,y)
    plt.title("30 simulations")
    plt.xlabel("Number of employees")
    plt.ylabel("MOS")
    plt.show()


def box_plot_graph():
    fig = plt.figure(figsize =(10, 7))
    plt.boxplot(lists_of_simulations)
    ypoints = np.array(avg_mos_employee)
    plt.plot(ypoints, color = 'r')
    plt.title("30 simulations")
    plt.xlabel("Number of employees")
    plt.ylabel("MOS")
    plt.show()

bar_plot_graph()
box_plot_graph()



# source: https://simpy.readthedocs.io/en/latest/examples/gas_station_refuel.html?fbclid=IwAR0HUGQIf0_76r91vCFj9CnSMlGaqqvMJiWtNXAW0uaRTOrTP_xSp8oMsow






