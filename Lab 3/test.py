



lambda_0 = lambda_p / ( (p_i * N_i[i]) - 2 )
lambda_1 = lambda_p / ( N_i[i] - (p_i * N_i[i]) )

p_0 = (lambda_0 * lambda_1 / ((lambda_0 * lambda_1) + (lambda_0 * my) + (lambda_1 * my) + my**(2)))

v = 1 - p_0

print(v)