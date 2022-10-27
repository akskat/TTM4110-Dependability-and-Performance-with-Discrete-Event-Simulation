#Task A.4

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


lambda_p=1
n_employees = 1
p_i = 0.05 * n_employees 
N_1 = 150
u_1 = 36
N_i = N_1
u_i = u_1
my = n_employees/u_i

lambda_0 = lambda_p / ( (p_i * N_i) - 2 )
lambda_1 = lambda_p / ( N_i - (p_i * N_i) )
p_0 = (lambda_0 * lambda_1 / ((lambda_0 * lambda_1) + (lambda_0 * my) + (lambda_1 * my) + my**(2)))

v = round((1 - p_0),2)
MOS_score = calculate_Mos(v)

print(MOS_score)



