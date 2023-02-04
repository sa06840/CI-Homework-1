import random
import numpy as np

class Knapsack():
    
    def __init__(self, file) -> None:

        self.populationSize = 30
        self.population = [0]*self.populationSize
        self.text = []
        self.mutationRate = 0.5
        self.chromosomeSize = self.text[0][0]
        self.maxWeight = self.text[0][1]

        read = file.readlines()
        for line in read:
            if line[-1] == '\n':
                row = [int(i) for i in line[:-1].split()]
                self.text.append(row)
            else:
                row = [int(i) for i in line.split()]
                self.text.append(row)

    def goodPopulate(self):
        for i in range(self.populationSize):
            chromosome = [0] * self.chromosomeSize
            totalWeight = 0
            totalProfit = 0
            while totalWeight <= self.maxWeight:
                randomNumber = random.randint(0,self.chromosomeSize-1)
                while chromosome[randomNumber] == 1:
                    randomNumber = random.randint(0,self.chromosomeSize-1)
                if (totalWeight + self.text[randomNumber+1][1]) <= self.maxWeight:
                    chromosome[randomNumber] = 1
                    totalWeight += self.text[randomNumber+1][1]
                    totalProfit += self.text[randomNumber+1][0]
                else:
                    break
            self.population[i] = [self.maxWeight-totalProfit, chromosome]

    def populate(self):
        for i in range(self.populationSize):
            chromosome = [0] * self.chromosomeSize
            for j in range(self.chromosomeSize):
                chromosome[j] = random.randint(0,1)
            self.population[i] = [self.maxWeight, chromosome]

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
                    self.population[i][0] = 100
    
    def crossover(self, p1, p2):
        offspring1 = [0]*self.chromosomeSize
        offspring2 = [0]*self.chromosomeSize

        p1 = p1[1]
        p2 = p2[1]

        start = random.randint(0, self.chromosomeSize-1)
        end = random.randint(0, self.chromosomeSize-1)
        while start == end:
            end = random.randint(0, self.chromosomeSize-1)
        
        if start > end:

            offspring1[start:len(p1)] = p1[start:len(p1)]
            offspring1[0:end] = p1[0:end]
            offspring1[end:start] = p2[end:start]
            offspring2[start:len(p1)] = p2[start:len(p1)]
            offspring2[0:end] = p2[0:end]
            offspring2[end:start] = p1[end:start]

        elif start < end:

            offspring1[start:end] = p1[start:end]
            offspring1[end:len(p1)] = p2[end:len(p1)]
            offspring1[0:start] = p2[0:start]
            offspring2[start:end] = p2[start:end]
            offspring2[end:len(p1)] = p1[end:len(p1)]
            offspring2[0:start] = p1[0:start]

        offspring1 = [0, offspring1]
        offspring2 = [0, offspring2]

        return [offspring1, offspring2]
        
    def mutation(self, offspring):
        repeated = []
        for i in range(2):
            randomIndex = random.randint(0, self.chromosomeSize-1)

            while randomIndex in repeated:
                randomIndex = random.randint(0, self.chromosomeSize-1)

            if offspring[1][randomIndex] == 1:
                offspring[1][randomIndex] = 0
            elif offspring[1][randomIndex] == 0:
                offspring[1][randomIndex] = 1
            repeated.append(randomIndex)

        # randomIndex1 = random.randint(0,self.text[0][0]-1)
        # randomIndex2 = random.randint(0,self.text[0][0]-1)
        # while randomIndex1 == randomIndex2:
        #     randomIndex2 = random.randint(0,self.text[0][0]-1)

        # if offspring[1][randomIndex1] == 1:
        #     offspring[1][randomIndex1] = 0
        #     if offspring[1][randomIndex2] == 1:
        #         offspring[1][randomIndex2] = 0
        #     else:
        #         offspring[1][randomIndex2] = 1

        # else:
        #     offspring[1][randomIndex1] = 1
        #     if offspring[1][randomIndex2] == 1:
        #         offspring[1][randomIndex2] = 0
        #     else:
        #         offspring[1][randomIndex2] = 1
        return offspring
        
    def newFitness(self, offspring):
        totalWeight = 0
        totalProfit = 0
        for i in range(len(offspring[1])):
            
            if offspring[1][i] != 0:
                totalWeight += self.text[i+1][1]
                totalProfit += self.text[i+1][0]

            offspring[0] = totalProfit
            if totalWeight > self.maxWeight:
                offspring[0] = 100
        return offspring
    

    def parentRandom(self):
        p1Index = random.randint(0,self.populationSize-1)
        p2Index = random.randint(0,self.populationSize-1)
        while p1Index == p2Index:
            p2Index = random.randint(0,self.populationSize-1)
        p1 = self.population[p1Index]
        p2 = self.population[p2Index]
        return [p1, p2]

    def parentFPS(self):

        sumFitness = 0
        normalizedFitness = []
        ranges = []
        for chromosome in self.population:
            sumFitness += chromosome[0]
        for chromosome in self.population:
            normalizedFitness.append(chromosome[0]/sumFitness)
        pointer = 0
        for i in range(len(normalizedFitness)):
            limits = [pointer, pointer+normalizedFitness[i]]
            ranges.append(limits)
            pointer += normalizedFitness[i]

        randomIndex = random.uniform(0,1)
        for index in range(len(ranges)):
            if randomIndex >= ranges[index][0] and randomIndex <= ranges[index][1]:
                p1Index = index
            
        p2Index = p1Index
        while(p1Index == p2Index):
            randomIndex = random.uniform(0,1)
            for index in range(len(ranges)):
                if randomIndex >= ranges[index][0] and randomIndex <= ranges[index][1]:
                    p2Index = index

        return [self.population[p1Index], self.population[p2Index]]
    
    def parentRBS(self):

        self.population.sort()
        ranks = []
        normalizedRanks = []
        sumRanks = 0
        ranges = []

        for rank in range(1, len(self.population)+1):
            ranks.append(rank)
            sumRanks += rank
        self.population.reverse()
        ranks.reverse()
        for i in ranks:
            normalizedRanks.append(i/sumRanks)

        pointer = 0
        for i in range(len(normalizedRanks)):
            limits = [pointer, pointer+normalizedRanks[i]]
            ranges.append(limits)
            pointer += normalizedRanks[i]
        
        randomIndex = random.uniform(0,1)
        for index in range(len(ranges)):
            if randomIndex >= ranges[index][0] and randomIndex <= ranges[index][1]:
                p1Index = index
            
        p2Index = p1Index
        while(p1Index == p2Index):
            randomIndex = random.uniform(0,1)
            for index in range(len(ranges)):
                if randomIndex >= ranges[index][0] and randomIndex <= ranges[index][1]:
                    p2Index = index

        return [self.population[p1Index], self.population[p2Index]]
    
    def parentTruncation(self):
        self.population.sort()
        self.population.reverse()
        return [self.population[0], self.population[1]]
    
    def parentBinary(self):
        contestant1 = random.randint(0, self.populationSize-1)
        contestant2 = random.choice(list(set(range(0, self.populationSize)) - set([contestant1])))

        if self.population[contestant1][0] >= self.population[contestant2][0]:
            p1Index = contestant1
        else:
            p1Index = contestant2

        contestant1 = random.choice(list(set(range(0, self.populationSize)) - set([p1Index])))
        contestant2 = random.choice(list(set(range(0, self.populationSize)) - set([p1Index, contestant1])))

        if self.population[contestant1][0] >= self.population[contestant2][0]:
            p2Index = contestant1
        else:
            p2Index = contestant2

        return [self.population[p1Index], self.population[p2Index]]


    def survivorRandom(self):
        randomlist = random.sample(range(0, len(self.population)), self.populationSize)
        temp_population = []
        for index in randomlist:
            temp_population.append(self.population[index])
        self.population=temp_population
            
    def survivorTruncation(self):
        self.population.sort()
        self.population.reverse()
        self.population = self.population[0:self.populationSize]

    def survivorBinary(self):
        selectedIndexes = []

        for i in range(self.populationSize):
            contestant1 = random.choice(list(set(range(0, len(self.population))) - set(selectedIndexes)))
            contestant2 = random.choice(list(set(range(0, len(self.population))) - set(selectedIndexes + [contestant1])))

            if self.population[contestant1][0] >= self.population[contestant2][0]:
                selectedIndexes.append(contestant1)
            else:
                selectedIndexes.append(contestant2)

        tempPopulation = []
        for index in selectedIndexes:
            tempPopulation.append(self.population[index])
        
        self.population = tempPopulation


def evolutionaryAlgorithm():

    for iteration in range(10):

        print("***** Iteration Number = " + str(iteration+1) + " *****")
        k1 = Knapsack(file = open('/Users/sajeelnadeemalam/Documents/CI/CI-Homework-1/instances_01_KP/low-dimensional/f8_l-d_kp_23_10000', 'r'))
        # k1.populate()
        k1.goodPopulate()
        # k1.calculateFitness()

        for generation in range(1000):
            print("***** Iteration Number = " + str(iteration+1) + ", Generation Number = " + str(generation+1) + " *****")

            for i in range(5):
                parents = k1.parentRandom()
                # parents = k1.parentFPS()
                # parents = k1.parentRBS()
                # parents = k1.parentTruncation()
                # parents = k1.parentBinary()

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

            k1.survivorTruncation()
            # k1.selectionRandom()
            # k1.survivorBinary()


            print(k1.population[0])
  
evolutionaryAlgorithm()



