
lambda_p=1 
emp = 1
p_i = 0.05 * emp
N_i = [100, 150, 50, 150, 80, 40, 250]
u_i = [60, 36, 42, 42, 30, 60, 90]

list_availibility_sections = []

for i in range(0, 7):
    my = emp/u_i[i]
    lambda_0 = lambda_p / ( N_i[i] - 2 )
    p_0 = lambda_0 / (lambda_0 + my) 

    v = 1 - p_0
    list_availibility_sections.append(v)
s_total = list_availibility_sections
exp_parallell = 1 - ( (1 - s_total[1]*s_total[4]) * (1 - s_total[5]) )
exp_total = exp_parallell*s_total[2]*s_total[3]*s_total[6]

print(s_total)
print()
print(exp_total)





