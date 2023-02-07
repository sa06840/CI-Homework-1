import random
from knapsack import Knapsack
from tspv2 import TSP
from graphColoring import GraphColoring


def evolutionaryAlgorithm(knapsackFile, tspFile, graphFile):
    fitnessEvaluation = dict()
    for iteration in range(10):

        print("***** Iteration Number = " + str(iteration+1) + " *****")

        k1 = Knapsack(file = open(knapsackFile, 'r'))
        t1 = TSP(tspFile)
        g1 = GraphColoring(file = open(graphFile, 'r'))

        k1.goodPopulate()
        t1.calculateFitness()
        g1.populate()
        g1.calculateFitness()

        for generation in range(g1.numOfGenerations):
            # print("***** Iteration Number = " + str(iteration+1) + ", Generation Number = " + str(generation+1) + " *****")

            totalOffsprings = []

            for i in range(5):
                # parents = k1.randomSelection(0)
                # parents = k1.fpsSelection(0)
                # parents = k1.rbsSelection(0)
                # parents = k1.truncation(0)
                # parents = k1.binarySelection(0)

                parents = g1.randomSelection(0)
                # parents = g1.fpsSelection(0)
                # parents = g1.rbsSelection(0)
                # parents = g1.truncation(0)
                # parents = g1.binarySelection(0)

                # parents = t1.randomSelection(0)
                # parents = t1.fpsSelection(0)
                # parents = t1.rbsSelection(0)
                # parents = t1.truncation(0)
                # parents = t1.binarySelection(0)

                p1 = parents[0]
                p2 = parents[1]

                # offsprings = k1.crossover(p1, p2)
                offsprings = g1.crossover(p1, p2)
                # offsprings = t1.crossover(p1, p2)

                for j in range(2):
                    randomNumber = random.randint(0,1)
                    if randomNumber == 1:

                        # tempOffspring = k1.mutation(offsprings[j])
                        tempOffspring = g1.mutation(offsprings[j])
                        # tempOffspring = t1.mutation(offsprings[j])

                        offsprings[j] = tempOffspring

                    # offspring = k1.newFitness(offsprings[j])
                    offspring = g1.newFitness(offsprings[j])
                    # offspring = t1.newFitness(offsprings[j])

                    totalOffsprings.append(offspring)
            
            for i in totalOffsprings:
                # k1.population.append(i)
                g1.population.append(i)
                # t1.population.append(i)

            # k1.randomSelection(1)
            # k1.fpsSelection(1)
            # k1.rbsSelection(1)
            # k1.truncation(1)
            # k1.binarySelection(1)

            g1.randomSelection(1)
            # g1.fpsSelection(1)
            # g1.rbsSelection(1)
            # g1.truncation(1)
            # g1.binarySelection(1)

            # t1.randomSelection(1)
            # t1.fpsSelection(1)
            # t1.rbsSelection(1)
            # t1.truncation(1)
            # t1.binarySelection(1)

            # print(k1.population[0])
            # print(g1.population[0])
            # print("number of colours: " + str(len(set(g1.population[0][1]))))

            # k1.generationEvaluation()
            g1.generationEvaluation()
            # t1.generationEvaluation()
            

            # print(t1.population[0])
            # print("distance: " + str(t1.maxDistance-t1.population[0][0]))
        # k1.iterationEvaluation(fitnessEvaluation,iteration)
        g1.iterationEvaluation(fitnessEvaluation,iteration)
        # t1.iterationEvaluation(fitnessEvaluation,iteration)
        
    # k1.plotGraphs(fitnessEvaluation)
    g1.plotGraphs(fitnessEvaluation)
    # t1.plotGraphs(fitnessEvaluation)
  
knapsackFile = 'instances_01_KP/low-dimensional/f8_l-d_kp_23_10000'
tspFile ='qa194.tsp'
graphFile = 'gcol1.txt'

evolutionaryAlgorithm(knapsackFile, tspFile, graphFile)