import random

class Knapsack():
    
    def __init__(self) -> None:

        self.populationSize = 30
        self.population = [0]*self.populationSize
        self.text = []
        self.mutationRate = 0.5

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

        offspring1 = [0, offspring1]
        offspring2 = [0, offspring2]

        return [offspring1, offspring2]
        
    def mutation(self, offspring):
        randomIndex1 = random.randint(0,self.text[0][0]-1)
        randomIndex2 = random.randint(0,self.text[0][0]-1)
        while randomIndex1 == randomIndex2:
            randomIndex2 = random.randint(0,self.text[0][0]-1)
        if offspring[1][randomIndex1] == 1:
            offspring[1][randomIndex1] = 0
            if offspring[1][randomIndex2] == 1:
                offspring[1][randomIndex2] = 0
            else:
                offspring[1][randomIndex2] = 1
        else:
            offspring[1][randomIndex1] = 1
            if offspring[1][randomIndex2] == 1:
                offspring[1][randomIndex2] = 0
            else:
                offspring[1][randomIndex2] = 1
        return offspring
        
    def newFitness(self, offspring):
        totalWeight = 0
        totalProfit = 0
        for i in range(len(offspring[1])):
            if offspring[1][i] != 0:
                totalWeight += self.text[i+1][1]
                totalProfit += self.text[i+1][0]
                # print(offspring)
                # print(i)
            offspring[0] = totalProfit
            # offspring.insert(0, totalProfit)
            if totalWeight > 10000:
                offspring[0] = 0
        return offspring

    def fitnessSurvivor(self):
        self.population.sort()
        self.population.reverse()
        self.population = self.population[0:self.populationSize]


def evolutionaryAlgorithm():

    for iteration in range(10):

        print("***** Iteration Number = " + str(iteration+1) + " *****")
        k1 = Knapsack()
        k1.populate()
        k1.calculateFitness()

        for generation in range(1000):
            print("***** Generation Number = " + str(generation+1) + " *****")
            generationOffsprings = []

            for i in range(5):
                parents = k1.selectionRandom()
                p1 = parents[0]
                p2 = parents[1]
                offsprings = k1.crossover(p1, p2)
                for j in range(2):
                    randomNumber = random.randint(0,1)
                    if randomNumber == 1:
                        tempOffspring = k1.mutation(offsprings[j])
                        offsprings[j] = tempOffspring

                    offspring = k1.newFitness(offsprings[j])
                    k1.population.append(offspring)

            k1.population.sort()
            k1.population.reverse()

            k1.population = k1.population[0:30]

            print(k1.population[0])
  
evolutionaryAlgorithm()



