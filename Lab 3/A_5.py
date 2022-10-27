
#Task A.5




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


# when number of employees is more than 18 the results gets unstable therefore we only go up to 18

lambda_p=1
n_employees = 1
p_i = 0.05 * n_employees 
N_i = [100, 150, 50, 150, 80, 40, 250]
u_i = [60, 36, 42, 42, 30, 60, 90]
list_mos_sections = []

for i in range(0, 7):
    my = n_employees/u_i[i]
    #special case for section 5 where the threshold value is 2 and number of employeers are 1
    if (i == 5):
        lambda_0 = lambda_p / ( N_i[i] - (p_i * N_i[i]) )
        p_0 = lambda_0 / (lambda_0 + my) 

    #all the other sections
    else:
        lambda_0 = lambda_p / ( (p_i * N_i[i]) - 2 )
        lambda_1 = lambda_p / ( N_i[i] - (p_i * N_i[i]) )
        p_0 = (lambda_0 * lambda_1 / ((lambda_0 * lambda_1) + (lambda_0 * my) + (lambda_1 * my) + my**(2)))

    v = round((1 - p_0),2)
    MOS_score = calculate_Mos(v)
    list_mos_sections.append(MOS_score)

print(list_mos_sections)
    



    
                
    
    
    





