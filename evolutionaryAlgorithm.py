import random


# Knapsack Problem

def populate(text):
    population = [0]*30
    for i in range(30):
        chromosome = [0]*text[0][0]
        for j in range(text[0][0]):
            chromosome[j] = random.randint(0,1)
        population[i] = [0, chromosome]
    return population

def readFile():
    file = open('/Users/sajeelnadeemalam/Documents/CI/assignment_1/instances_01_KP/low-dimensional/f8_l-d_kp_23_10000', 'r')
    read = file.readlines()
    text = []
    for line in read:
        if line[-1] == '\n':
            row = [int(i) for i in line[:-1].split()]
            text.append(row)
        else:
            row = [int(i) for i in line.split()]
            text.append(row)
    print(text)
    return text

def calculateFitness(population, text):
    for i in range(len(population)):
        totalWeight = 0
        totalProfit = 0
        for j in range(len(population[0][1])):
            if population[i][1][j] != 0:
                totalWeight += text[j+1][1]
                totalProfit += text[j+1][0]
            population[i][0] = totalProfit
            if totalWeight > text[0][1]:
                population[i][0] = 0
    return population

text = readFile()
population = populate(text)
print(calculateFitness(population, text))





