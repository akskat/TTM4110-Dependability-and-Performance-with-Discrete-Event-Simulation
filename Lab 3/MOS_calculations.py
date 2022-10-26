
lambda_p = 1
n_employees = 10
p_i = 0.05 * n_employees 
N_i = 100
u_i = 60
my = 1/u_i
lambda_0 = lambda_p / ( (p_i * N_i) - 2 )
lambda_1 = lambda_p / ( N_i - (p_i * N_i) )

p_0 = (lambda_0 * lambda_1 / ((lambda_0 * lambda_1) + (lambda_0 * my) + (lambda_1 * my) + my**(2)))
p_1 = (lambda_1 * my / ((lambda_0 * lambda_1) + (lambda_0 * my) + (lambda_1 * my) + my**(2)))
p_2 = my / (lambda_1 + my)

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