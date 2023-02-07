import random
from matplotlib import pyplot as plt
from operator import add
from selectionSchemes import SelectionSchemes

class GraphColoring(SelectionSchemes):

    def __init__(self, file) -> None:

        self.text = []
        self.populationSize = 30
        self.population = []
        self.bestsofar =9999999999
        self.averageFitness=[]
        self.bestFitness= []
        self.numOfGenerations = 5000
        self.numOfIterations = 10

        super()

        read = file.readlines()
        for line in read:
            if line[-1] == '\n':
                row = [str(i) for i in line[:-1].split()]
                self.text.append(row)
            else:
                row = [str(i) for i in line.split()]
                self.text.append(row)

        self.chromosomeSize = int(self.text[0][2])
        self.edges = int(self.text[0][3])
        
        self.graph = {}
        for node in range(1, int(self.text[0][2])+1):
            self.graph[node] = []
        for edgeNumber in range(1, len(self.text)):
            self.graph[int(self.text[edgeNumber][1])].append(int(self.text[edgeNumber][2]))
            self.graph[int(self.text[edgeNumber][2])].append(int(self.text[edgeNumber][1]))

        outdegrees=[]
        for key, value in self.graph.items():
            outdegrees.append(len(value))
        outdegrees.sort()
        outdegrees.reverse()
        self.maxOutdegree = outdegrees[0]
        self.colors = self.maxOutdegree+1

    def populate(self):

        for chromosomeNumber in range(self.populationSize):
            chromosome = []
            for nodeNumber in range(int(self.text[0][2])):
                nodeColor = random.randint(1, self.colors)
                chromosome.append(nodeColor)
            self.population.append([self.edges+self.colors,chromosome])
        
    def calculateFitness(self):

        for chromosomeNumber in range(len(self.population)):
            graph = self.population[chromosomeNumber][1]
            fitness = self.edges
            for node in range(0, len(graph)):
                nodeColor = graph[node]
                neighbours = self.graph[node+1]
                for neighbour in neighbours:
                    if graph[neighbour-1] == nodeColor:
                        fitness -= 1
            totalColors = len(set(graph))
            fitness = fitness - totalColors
            self.population[chromosomeNumber] = [fitness, graph]

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

        offspring1 = [self.edges+self.colors, offspring1]
        offspring2 = [self.edges+self.colors, offspring2]

        return [offspring1, offspring2]
    
    def mutation(self, offspring):
        selectedIndexes = []
        for i in range(2):
            index1 = random.choice(list(set(range(0, self.chromosomeSize)) - set(selectedIndexes)))
            index2 = random.choice(list(set(range(0, self.chromosomeSize)) - set(selectedIndexes + [index1])))
            temp = offspring[1][index1]
            offspring[1][index1] = offspring[1][index2]
            offspring[1][index2] = temp
            selectedIndexes.append(index1)
            selectedIndexes.append(index2)
        return offspring
    
    def newFitness(self, offspring):
        graph = offspring[1]
        fitness = self.edges
        for node in range(0, len(graph)):
            nodeColor = graph[node]
            neighbours = self.graph[node+1]
            for neighbour in neighbours:
                if graph[neighbour-1] == nodeColor:
                    fitness -= 1
        totalColors = len(set(graph))
        fitness = fitness - totalColors
        offspring[0] = fitness
        return offspring
    
    def generationEvaluation(self):
        totalColors = 0
        
        for chromosome in self.population:
            totalColors += len(set(chromosome[1]))
            if (len(set(chromosome[1]))) < self.bestsofar:
                self.bestsofar =len(set(chromosome[1]))

        self.averageFitness.append(totalColors/len(self.population))
        self.bestFitness.append(self.bestsofar)

    def iterationEvaluation(self, fitnessEvaluation,iteration):
        # print(iteration)
        if iteration not in fitnessEvaluation:
            fitnessEvaluation[iteration] = [[],[]]
            fitnessEvaluation[iteration][0] = self.averageFitness 
            fitnessEvaluation[iteration][1] = self.bestFitness
          
    def plotGraphs(self, fitnessEvaluation):
        x_axis_generations = []
        addedAverageFitness = [0]*self.numOfGenerations
        addedBestFitness = [0]*self.numOfGenerations
        avgAverageFitness = []
        avgBestFitness = []

        # list representing x axis (num of Generations)
        for i in range (1, self.numOfGenerations+1):
            x_axis_generations.append(i)
       
       #adding avgaveragefitness and best fitness values across all iterations
        for iteration in (fitnessEvaluation):
            addedAverageFitness = list(map(add, fitnessEvaluation[iteration][0], addedAverageFitness))
            addedBestFitness  = list(map(add, fitnessEvaluation[iteration][1], addedBestFitness ))
        
        #adjusting added avgavergaefitness and best fitness values
        #creating list representing y_axis (average avergae fitness values) and (average average best fitness values)
        for fitness in (addedAverageFitness):
            avgAverageFitness.append(fitness/self.numOfIterations)
        
        for fitness in (addedBestFitness):
            avgBestFitness.append(fitness/self.numOfIterations)
       
        plt.plot(x_axis_generations, avgBestFitness, label = "Best Fitness")       
        plt.plot(x_axis_generations, avgAverageFitness,linestyle = "dashed", label = "Average Fitness")
        plt.xlabel("Number of Generations")
        plt.ylabel("Number of Colors")
        plt.title("Graph Coloring")
        plt.legend()
        plt.show()


    # def parentRandom(self):
    #     p1Index = random.randint(0,self.populationSize-1)
    #     p2Index = random.randint(0,self.populationSize-1)
    #     while p1Index == p2Index:
    #         p2Index = random.randint(0,self.populationSize-1)
    #     p1 = self.population[p1Index]
    #     p2 = self.population[p2Index]
    #     return [p1, p2]
    
    # def parentFPS(self):

    #     sumFitness = 0
    #     normalizedFitness = []
    #     ranges = []
    #     for chromosome in self.population:
    #         sumFitness += chromosome[0]
    #     for chromosome in self.population:
    #         normalizedFitness.append(chromosome[0]/sumFitness)
    #     pointer = 0
    #     for i in range(len(normalizedFitness)):
    #         limits = [pointer, pointer+normalizedFitness[i]]
    #         ranges.append(limits)
    #         pointer += normalizedFitness[i]

    #     randomIndex = random.uniform(0,1)
    #     for index in range(len(ranges)):
    #         if randomIndex >= ranges[index][0] and randomIndex <= ranges[index][1]:
    #             p1Index = index
            
    #     p2Index = p1Index
    #     while(p1Index == p2Index):
    #         randomIndex = random.uniform(0,1)
    #         for index in range(len(ranges)):
    #             if randomIndex >= ranges[index][0] and randomIndex <= ranges[index][1]:
    #                 p2Index = index

    #     return [self.population[p1Index], self.population[p2Index]]
    
    # def parentRBS(self):

    #     self.population.sort()
    #     ranks = []
    #     normalizedRanks = []
    #     sumRanks = 0
    #     ranges = []

    #     for rank in range(1, len(self.population)+1):
    #         ranks.append(rank)
    #         sumRanks += rank
    #     self.population.reverse()
    #     ranks.reverse()
    #     for i in ranks:
    #         normalizedRanks.append(i/sumRanks)

    #     pointer = 0
    #     for i in range(len(normalizedRanks)):
    #         limits = [pointer, pointer+normalizedRanks[i]]
    #         ranges.append(limits)
    #         pointer += normalizedRanks[i]
        
    #     randomIndex = random.uniform(0,1)
    #     for index in range(len(ranges)):
    #         if randomIndex >= ranges[index][0] and randomIndex <= ranges[index][1]:
    #             p1Index = index
            
    #     p2Index = p1Index
    #     while(p1Index == p2Index):
    #         randomIndex = random.uniform(0,1)
    #         for index in range(len(ranges)):
    #             if randomIndex >= ranges[index][0] and randomIndex <= ranges[index][1]:
    #                 p2Index = index

    #     return [self.population[p1Index], self.population[p2Index]]
    
    # def parentTruncation(self):
    #     self.population.sort()
    #     self.population.reverse()
    #     return [self.population[0], self.population[1]]
    
    # def parentBinary(self):
    #     contestant1 = random.randint(0, self.populationSize-1)
    #     contestant2 = random.choice(list(set(range(0, self.populationSize)) - set([contestant1])))

    #     if self.population[contestant1][0] >= self.population[contestant2][0]:
    #         p1Index = contestant1
    #     else:
    #         p1Index = contestant2

    #     contestant1 = random.choice(list(set(range(0, self.populationSize)) - set([p1Index])))
    #     contestant2 = random.choice(list(set(range(0, self.populationSize)) - set([p1Index, contestant1])))

    #     if self.population[contestant1][0] >= self.population[contestant2][0]:
    #         p2Index = contestant1
    #     else:
    #         p2Index = contestant2

    #     return [self.population[p1Index], self.population[p2Index]]
    

    # def survivorRandom(self):
    #     randomlist = random.sample(range(0, len(self.population)), self.populationSize)
    #     temp_population = []
    #     for index in randomlist:
    #         temp_population.append(self.population[index])
    #     self.population=temp_population

    # def survivorTruncation(self):
    #     self.population.sort()
    #     self.population.reverse()
    #     self.population = self.population[0:self.populationSize]

    # def survivorBinary(self):
    #     selectedIndexes = []

    #     for i in range(self.populationSize):
    #         contestant1 = random.choice(list(set(range(0, len(self.population))) - set(selectedIndexes)))
    #         contestant2 = random.choice(list(set(range(0, len(self.population))) - set(selectedIndexes + [contestant1])))

    #         if self.population[contestant1][0] >= self.population[contestant2][0]:
    #             selectedIndexes.append(contestant1)
    #         else:
    #             selectedIndexes.append(contestant2)

    #     tempPopulation = []
    #     for index in selectedIndexes:
    #         tempPopulation.append(self.population[index])
        
    #     self.population = tempPopulation
                


# def evolutionaryAlgorithm():

#     for iteration in range(10):

#         print("***** Iteration Number = " + str(iteration+1) + " *****")
#         g1 = GraphColoring(file = open('/Users/sajeelnadeemalam/Documents/CI/CI-Homework-1/gcol1.txt', 'r'))
#         g1.populate()
#         g1.calculateFitness()

#         for generation in range(100):
#             print("***** Iteration Number = " + str(iteration+1) + ", Generation Number = " + str(generation+1) + " *****")

#             for i in range(5):
#                 parents = g1.parentRandom()
#                 # parents = g1.parentFPS()
#                 # parents = g1.parentRBS()
#                 # parents = g1.parentTruncation()
#                 # parents = g1.parentBinary()

#                 p1 = parents[0]
#                 p2 = parents[1]
#                 offsprings = g1.crossover(p1, p2)
#                 for j in range(2):
#                     randomNumber = random.randint(0,1)
#                     if randomNumber == 1:
#                         tempOffspring = g1.mutation(offsprings[j])
#                         offsprings[j] = tempOffspring

#                     offspring = g1.newFitness(offsprings[j])
#                     g1.population.append(offspring)

#             g1.survivorTruncation()
#             # g1.survivorRandom()
#             # g1.survivorBinary()

#             print(g1.population[0])
#             print("number of colours: " + str(len(set(g1.population[0][1]))))
  

# graphFile = '/Users/sajeelnadeemalam/Documents/CI/CI-Homework-1/gcol1.txt'
# evolutionaryAlgorithm(graphFile)