import tsplib95
import math
import random
import copy




class TSP():
    #Initializes variables
    # Reads the data file and stores coordinates for each country (dictionary)
    def __init__(self, filename) -> None:
        self.populationSize = 30
        self.euclideanDistance = dict()      
        self.population=[]                  #stores all solutions
        self.listOfCountries=[]             #stores names of countries
        self.fitness=[]                     #stores total distance of every solution

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
        self.initializePopulation(countryCoordinates)

    #Initializing a Population of 30 with a random shuffle of Countries
    def initializePopulation(self,countryCoordinates):
     
        for country in countryCoordinates:
            self.listOfCountries.append(country)

        for i in range(30):
            solution = copy.deepcopy(self.listOfCountries)
            random.shuffle(solution)
            self.population.append([0,solution])
        
        self.calculateFitness(self.population)
        
    #Calculating Total Distance of each solution and storing in Fitness list
    def calculateFitness(self, Population):
        count=0
        for solution in Population:
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
            self.population[count][0]=round(totalDistance,2)
            count+=1

    def selectionRandom(self):
        p1Index = random.randint(0,self.populationSize-1)
        p2Index = random.randint(0,self.populationSize-1)
        while p1Index == p2Index:
            p2Index = random.randint(0,self.populationSize-1)
        p1 = self.population[p1Index]
        p2 = self.population[p2Index]
        return ([p1, p2])
     
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
        offspring[0]=round(totalDistance,2)

        self.population.append(offspring)
        return (offspring)
    
    def truncation(self):
        self.population.sort(key = lambda x: x[0])
        self.population = self.population[0:30]
       


filename ='qa194.tsp'
T1=TSP(filename)
parents = T1.selectionRandom()
p1 = parents[0]
p2 = parents[1]
offsprings = T1.crossover(p1, p2)
offspring1=T1.mutation(offsprings[0])
offspring2=T1.mutation(offsprings[1])
fitness_offspring1=T1.newFitness(offspring1)
fitness_offspring2=T1.newFitness(offspring2)
# print(fitness_offspring)
T1.truncation()
