import tsplib95
import math
import random
import copy
from matplotlib import pyplot as plt
from operator import add



class TSP():
    #Initializes variables
    # Reads the data file and stores coordinates for each country (dictionary)
    def __init__(self, filename) -> None:
        self.populationSize = 30
        self.euclideanDistance = dict()      
        self.population=[]                  #stores all solutions
        self.listOfCountries=[]             #stores names of countries
        self.fitness=[]                     #stores total distance of every solution
        self.bestFitness= []
        self.averageFitness =[]
        self.numOfGenerations = 100
        self.numOfIterations  = 10
        self.maxDistance = 0  #changed
        
        
        self.bestsofar = 9999999999

        problem = tsplib95.load(filename)
        temp = problem.as_name_dict()
        countryCoordinates= temp["node_coords"]
        self.generateEuclideanDistance(countryCoordinates)

    # Generates distance for each country with respect to each country (dictionary)   
    def generateEuclideanDistance(self,countryCoordinates):

        for country1 in countryCoordinates:
            distances=[]
            for country2 in countryCoordinates:
                distances.append(math.dist(countryCoordinates[country1], countryCoordinates[country2]))
            self.euclideanDistance[country1]= distances
            self.maxDistance += round(max(distances),2)  #changed
        self.initializePopulation(countryCoordinates)

        # print(self.maxDistance)

    #Initializing a Population of 30 with a random shuffle of Countries
    def initializePopulation(self,countryCoordinates):
     
        for country in countryCoordinates:
            self.listOfCountries.append(country)

        for i in range(30):
            solution = copy.deepcopy(self.listOfCountries)
            random.shuffle(solution)
            self.population.append([0,solution])
        
    #Calculating Total Distance of each solution 
    def calculateFitness(self):
        count=0
        for solution in self.population:
            totalDistance=0
            for i in range(len(solution[1])-1):
                listOfDistance=self.euclideanDistance[solution[1][i]]
                distance=listOfDistance[(solution[1][i+1])-1]
                totalDistance+=distance
            '''
            Adding Distance of going back to origin country
            '''
            listOfDistance=self.euclideanDistance[solution[1][i+1]]
            distance=listOfDistance[solution[1][0]-1]
            totalDistance+=distance
            self.population[count][0]=self.maxDistance-round(totalDistance,2) #changed
            count+=1

        
    def newFitness(self, offspring):
        totalDistance=0
        distance = 0

        for i in range(len(offspring[1])-1):
            listOfDistance=self.euclideanDistance[offspring[1][i]]
            distance=listOfDistance[(offspring[1][i+1])-1]
            totalDistance+=distance

        '''
        Adding Distance of going back to origin country
        '''
        listOfDistance=self.euclideanDistance[offspring[1][i+1]]
        distance=listOfDistance[offspring[1][0]-1]
        totalDistance+=distance
        offspring[0]=self.maxDistance-round(totalDistance,2)   #changed

        # self.population.append(offspring)
        return (offspring)

    def crossover(self, p1, p2):
        self.length_of_solution=len(self.listOfCountries)
        offspring1 = [0]*self.length_of_solution
        offspring2 = [0]*self.length_of_solution
        #eliminating fitness values for both parents        
        p1 = p1[1]          
        p2 = p2[1]             

        start = random.randint(0, self.length_of_solution-1)
        end = random.randint(0, self.length_of_solution-1)
        while start == end:
            end = random.randint(0, self.length_of_solution)

        if start > end:
            offspring1[start:len(p1)] = p1[start:len(p1)]
            offspring1[0:end] = p1[0:end]
            offspring1[end:start] = p2[end:start]
            
            offspring2[start:len(p2)] = p2[start:len(p1)]
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

        randomIndex1 = random.randint(0,self.length_of_solution-1)
        randomIndex2 = random.randint(0,self.length_of_solution-1)
        while randomIndex1 == randomIndex2:
            randomIndex2 = random.randint(0,self.length_of_solution-1)
        
        country1 = offspring[1][randomIndex1]
        country2 = offspring[1][randomIndex2]
        offspring[1][randomIndex1] = country2
        offspring[1][randomIndex2] = country1

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

    # def generationEvaluation(self):
    #     totalDistance = 0
        
    #     for chromosome in self.population:
    #         totalDistance += chromosome[0]
    #         if chromosome[0] < self.bestsofar:
    #             self.bestsofar = chromosome[0]

    #     self.averageFitness.append(totalDistance/len(self.population))
    #     self.bestFitness.append(self.bestsofar)

    # def iterationEvaluation(self, fitnessEvaluation,iteration):
    #     # print(iteration)
    #     if iteration not in fitnessEvaluation:
    #         fitnessEvaluation[iteration] = [[],[]]
    #         fitnessEvaluation[iteration][0] = self.averageFitness 
    #         fitnessEvaluation[iteration][1] = self.bestFitness
          
    # def plotGraphs(self, fitnessEvaluation):
    #     x_axis_generations = []
    #     addedAverageFitness = [0]*self.numOfGenerations
    #     addedBestFitness = [0]*self.numOfGenerations
    #     avgAverageFitness = []
    #     avgBestFitness = []

    #     # list representing x axis (num of Generations)
    #     for i in range (1, self.numOfGenerations+1):
    #         x_axis_generations.append(i)
       
    #    #adding avgaveragefitness and best fitness values across all iterations
    #     for iteration in (fitnessEvaluation):
    #         addedAverageFitness = list(map(add, fitnessEvaluation[iteration][0], addedAverageFitness))
    #         addedBestFitness  = list(map(add, fitnessEvaluation[iteration][1], addedBestFitness ))
        
    #     #adjusting added avgavergaefitness and best fitness values
    #     #creating list representing y_axis (average avergae fitness values) and (average average best fitness values)
    #     for fitness in (addedAverageFitness):
    #         avgAverageFitness.append(fitness/self.numOfIterations)
        
    #     for fitness in (addedBestFitness):
    #         avgBestFitness.append(fitness/self.numOfIterations)
              
    #     plt.plot(x_axis_generations, avgAverageFitness, label = "Average Fitness")
    #     plt.plot(x_axis_generations, avgBestFitness, label = "Best Fitness")
        
    #     plt.legend()
    #     plt.show()

# Evolutionary Algorithm
def evolutionaryAlgorithm():
    # fitnessEvaluation = dict()
    # for iteration in range(1, 11):

        # print("***** Iteration Number = " + str(iteration+1) + " *****")
        filename ='qa194.tsp'
        T1=TSP(filename)
        # T1.populate()
        T1.calculateFitness()

        for generation in range(100):
            # print("***** Iteration Number = " + str(iteration+1) + ", Generation Number = " + str(generation+1) + " *****")

            for i in range(5):
                parents = T1.parentRandom()
                # print("PARENTS")
                # print(T1.population)
                # print("SELECTED PARENTS")
                # parents = T1.parentTruncation()
                # parents = T1.parentFPS()
                # parents = T1.parentRBS()
                # parents = T1.parentBinary()
                
                # print("PARENT 1")
                # print(parents)
                p1 = parents[0]
                # print(p1)
                # print("PARENT 2")
                p2 = parents[1]
                # print(p2)
                
                # print("OFF SPRINGSS")
                offsprings = T1.crossover(p1, p2)
                # print(offsprings)

                for j in range(2):
                    randomNumber = random.randint(0,1)
                    if randomNumber == 1:
                        tempOffspring = T1.mutation(offsprings[j])
                        # print("MUTATED OFFSPRING")
                        # print(tempOffspring)
                        offsprings[j] = tempOffspring

                    offspring = T1.newFitness(offsprings[j])
                    # print("OFFSPRING WITH FITNESS VALUE")
                    # print(offspring)
                    T1.population.append(offspring)
                    # print(len(T1.population))

            T1.survivorTruncation()
            # T1.generationEvaluation()
            # T1.survivorBinary()
            # T1.survivorRandom()
            # T1.fitnessProportional()
            print(T1.population[0])
            print("distance: " + str(T1.maxDistance-T1.population[0][0]))
        # print(T1.avergeFitness)
        # print(T1.bestFitness)
        # T1.iterationEvaluation(fitnessEvaluation,iteration)
        # print(len(T1.bestFitness))
        # print(len(T1.avergeFitness))
    # print(fitnessEvaluation)
    # T1.plotGraphs(fitnessEvaluation)

evolutionaryAlgorithm()

