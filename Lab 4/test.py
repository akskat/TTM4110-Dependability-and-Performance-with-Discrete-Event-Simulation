import numpy
import matplotlib.pyplot as plt


N = [100, 150, 50, 150, 80, 40, 250]
u = [60, 36, 42, 42, 30, 60, 90]


lambda_p = 1

def p2_exception(Ni, Ui, numberOfEmployees):
    S1 = (Ni-Ni*0.05*numberOfEmployees)
    lambda_1 = 1/S1
    Myi = numberOfEmployees/Ui
    p_1 = (lambda_1) / (lambda_1 + Myi)
    return 1-p_1


service_availability = []


def calc_V(employees):
    Si = [0,0,0,0,0,0,0]
   # Ri = [0,0,0,0,0,0,0]
    for i in range(1,7):
        Si[i] = p2_exception(N[i], u[i], employees)
        #  Ri[i] = numpy.exp(-p2_exception(N[i], u[i], employees))
        if (employees == 2  and (i ==6)):
            print(Si[2])

    probS = ((Si[1] * Si[4]) + Si[5] - ((Si[1] * Si[4]) * Si[5])) * Si[2] * Si[3] * Si[6]
    #Rt = ((Ri[1] * Ri[4]) + Ri[5] - ((Ri[1] * Ri[4]) * Ri[5])) * Ri[2] * Ri[3] * Ri[6]
    service_availability.append(probS)
    
            
def iterate_V_emp():
    for j in range(1,16):
        calc_V(j)
    #print(service_availability)


# ((S1 * S4) + S5 - ((S1 * S4) * S5)) * S2 * S3 * S6)

# Results

# for i in range(0,6):
#     print(1 - p2(N[i],u[i],1))

#print(1 - p2_exception(40, 60, 1))

S0 = 0.631336405529954
S1 = 0.825048091525767
S2 = 0.5362471245481433
S3 = 0.7987163029525033
S4 = 0.7346698113207548
S5 = 0.3877551020408163
S6 = 0.7539022445026775


#((S1 * S4) + S5 - ((S1 * S4) * S5)) * S2 * S3 * S6
" Service availability for sections 1-6 with 1 employee 0.24503842"
#print( ((S1 * S4) + S5 - ((S1 * S4) * S5)) * S2 * S3 * S6)


iterate_V_emp()

names = ['1', '2', '3', '4', '5', '6', '7', '8' ,'9', '10', '11', '12', '13', '14', '15']



def bar_plot_graph():
    x = numpy.array(names)
    y = numpy.array(service_availability)
    plt.plot(x,y)
    plt.xticks(x)
    plt.title("Service availability per employee")
    plt.xlabel("Number of employees")
    plt.ylabel("Service probability")
    plt.show()

#bar_plot_graph()