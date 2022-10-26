
lambda_p = 1
n_employees = 1
p_i = 0.05 * n_employees 
N_i = 40
u_i = 60
my = 1/u_i
lambda_0 = lambda_p / ( N_i - (p_i * N_i) )

p_0 = -lambda_p / (N_i * p_i * my - N_i * my - lambda_p)
p_1 = (N_i * p_i * - N_i * my) / (N_i * p_i * my - N_i * my - lambda_p)

v = 1 - p_0

def generateMos(v):
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

print(generateMos(v))