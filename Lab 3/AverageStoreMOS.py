

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

list_of_diff_emp = []

for emp in range(1, 20):
    average = []
    lambda_p=1
    #n_employees = emp
    p_i = 0.05 * emp 
    N_i = [100, 150, 50, 150, 80, 40, 250]
    u_i = [60, 36, 42, 42, 30, 60, 90]

    for i in range(0, 7):
        my = emp/u_i[i]
        #special case for section 5 where the threshold value is 2 which causes problems for the model
        if (i == 5):
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

        v = 1 - p_0
        MOS_score = calculate_Mos(v)
        average.append(MOS_score)
                
    print(average)
    avg_per_emp = sum(average)/len(average)
    list_of_diff_emp.append(avg_per_emp)

print(list_of_diff_emp)



