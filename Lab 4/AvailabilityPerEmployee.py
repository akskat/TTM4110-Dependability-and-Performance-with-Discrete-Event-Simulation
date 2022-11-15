import numpy as np
import matplotlib.pyplot as plt


avail_per_employee = []
N_i = [100, 150, 50, 150, 80, 40, 250]
u_i = [60, 36, 42, 42, 30, 60, 90]
for emp in range(1, 16):
    lambda_p=1
    p_i = 0.05 * emp 
    s_total = []

    for i in range(0, 7):
        my = emp/u_i[i]
        lambda_0 = (lambda_p) / ( N_i[i] - 2 )
        p_0 = (lambda_0) / (lambda_0 + my) 
        v = 1 - p_0
        s_total.append(v)
        

    exp_parallell = 1 - ( (1 - s_total[1]*s_total[4]) * (1 - s_total[5]) )
    #exp_parallell = -s_total[1] * s_total[4] * s_total[5] + s_total[1] * s_total[4] + s_total[5]
    exp_total = exp_parallell * s_total[2] * s_total[3] * s_total[6]

    avail_per_employee.append(exp_total)


#print(avail_per_employee)

x = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15])
y = np.array(avail_per_employee)

plt.plot(x, y)
plt.title("Availability per employee")
plt.xlabel("Employees")
plt.ylabel("Availability")
plt.show()
