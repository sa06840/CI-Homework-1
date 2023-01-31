import random

class Knapsack():
    
    def __init__(self) -> None:

        self.populationSize = 30
        self.population = [0]*self.populationSize
        self.text = []

        file = open('/Users/sajeelnadeemalam/Documents/CI/assignment_1/instances_01_KP/low-dimensional/f8_l-d_kp_23_10000', 'r')
        read = file.readlines()
        for line in read:
            if line[-1] == '\n':
                row = [int(i) for i in line[:-1].split()]
                self.text.append(row)
            else:
                row = [int(i) for i in line.split()]
                self.text.append(row)

    def populate(self):
        for i in range(30):
            chromosome = [0] * self.text[0][0]
            for j in range(self.text[0][0]):
                chromosome[j] = random.randint(0,1)
            self.population[i] = [0, chromosome]
        return self.population

    def calculateFitness(self):
        for i in range(len(self.population)):
            totalWeight = 0
            totalProfit = 0
            for j in range(len(self.population[0][1])):
                if self.population[i][1][j] != 0:
                    totalWeight += self.text[j+1][1]
                    totalProfit += self.text[j+1][0]
                self.population[i][0] = totalProfit
                if totalWeight > self.text[0][1]:
                    self.population[i][0] = 0
        return self.population

    def selectionRandom(self):
        p1Index = random.randint(0,self.populationSize-1)
        p2Index = random.randint(0,self.populationSize-1)
        while p1Index == p2Index:
            p2Index = random.randint(0,self.populationSize-1)
        p1 = self.population[p1Index]
        p2 = self.population[p2Index]
        return [p1, p2]

    def crossover(self, p1, p2):
        offspring1 = offspring2 = [0]*self.text[0][0]
        p1 = p1[1]
        p2 = p2[1]
        start = random.randint(0, len(p1)//2)
        end = random.randint(len(p2)//2 + 1, len(p2)-1)

        offspring1[start:end+1] = p1[start:end+1]
        offspring1[0:start] = p2[0:start]
        offspring1[end+1:len(p1)] = p2[end+1:len(p1)]

        offspring2[start:end+1] = p2[start:end+1]
        offspring2[0:start] = p1[0:start]
        offspring2[end+1:len(p1)] = p1[end+1:len(p1)]
        
    def mutation(self, offspring):
        randomIndex1 = random.randint(0,self.text[0][0]-1)
        randomIndex2 = random.randint(0,self.text[0][0]-1)
        while randomIndex1 == randomIndex2:
            randomIndex2 = random.randint(0,self.text[0][0]-1)
        if offspring[randomIndex1] == 1:
            offspring[randomIndex1] = 0
            if offspring[randomIndex2] == 1:
                offspring[randomIndex2] = 0
            else:
                offspring[randomIndex2] = 1
        else:
            offspring[randomIndex1] = 1
            if offspring[randomIndex2] == 1:
                offspring[randomIndex2] = 0
            else:
                offspring[randomIndex2] = 1

    def newFitness(self, offspring):
        totalWeight = 0
        totalProfit = 0
        for i in range(len(offspring)):
            if offspring[i] != 0:
                totalWeight += self.text[i+1][1]
                totalProfit += self.text[i+1][0]
            offspring.insert(0, totalProfit)
            if totalWeight > 10000:
                offspring[0] = 0
        self.population.append(offspring)

    def fitnessSurvivor(self):
        self.population.sort()
        self.population.reverse()
        self.population = self.population[0:self.populationSize]







