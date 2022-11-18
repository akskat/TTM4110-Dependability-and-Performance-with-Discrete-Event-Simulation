var1 = input("Write a math problem")



def calculateProblem(var1):

    for i in range(len(var1)):

        symbols = []
        numbers = [0,1,2,3,4,5,6,7,8,9]
        numbersToBeCalculated = []

        if (i == "+") or (i=="-"):
            symbols.append(i)
        if i in numbers:
            numbersToBeCalculated.append(int(i))
    math = numbersToBeCalculated[0] + symbols[0] + numbersToBeCalculated[1]

    print(var1 + "is equal to: " + numbersToBeCalculated)

calculateProblem(var1)
