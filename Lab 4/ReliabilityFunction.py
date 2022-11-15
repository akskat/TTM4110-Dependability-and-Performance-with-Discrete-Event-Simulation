import numpy as np
import matplotlib.pyplot as plt


t = 2*60
timelist = []
for p in range(0,t+1):
    timelist.append(p)


lambda_p = 1
emp = 1
p_i = 0.05 * emp 
N_i = [100, 150, 50, 150, 80, 40, 250]
u_i = [60, 36, 42, 42, 30, 60, 90]

lambda_0 = lambda_p / ( N_i[0] - 2 )
lambda_1 = lambda_p / ( N_i[1] - 2 )
lambda_2 = lambda_p / ( N_i[2] - 2 )
lambda_3 = lambda_p / ( N_i[3] - 2 )
lambda_4 = lambda_p / ( N_i[4] - 2 )
lambda_5 = lambda_p / ( N_i[5] - 2 )
lambda_6 = lambda_p / ( N_i[6] - 2 )

def R(t):
    list = []
    i=0
    while i < t+1:
        exp_total = (1 - ( (1 - np.exp(-lambda_1*i) * np.exp(-lambda_4*i)) * (1 - np.exp(-lambda_5*i)) )) * np.exp(-lambda_2*i) * np.exp(-lambda_3*i) * np.exp(-lambda_6*i)
        
        list.append(exp_total)
        i+=1
    return list
print(R(t))

x = np.array(timelist)
y = np.array(R(t))

plt.plot(x, y)
plt.title("Reliability for time (one employee)")
plt.xlabel("Time")
plt.ylabel("Reliability")
plt.show()
