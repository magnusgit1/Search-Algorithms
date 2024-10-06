#Precode to collect cities and for plots:
import csv
import matplotlib.pyplot as plt
import time
import random
import numpy as np
#%matplotlib inline
np.random.seed(57)
#Map of Europe
europe_map = plt.imread('map.png')

#Lists of city coordinates
city_coords = {
    "Barcelona": [2.154007, 41.390205], "Belgrade": [20.46, 44.79], "Berlin": [13.40, 52.52], 
    "Brussels": [4.35, 50.85], "Bucharest": [26.10, 44.44], "Budapest": [19.04, 47.50],
    "Copenhagen": [12.57, 55.68], "Dublin": [-6.27, 53.35], "Hamburg": [9.99, 53.55], 
    "Istanbul": [28.98, 41.02], "Kyiv": [30.52, 50.45], "London": [-0.12, 51.51], 
    "Madrid": [-3.70, 40.42], "Milan": [9.19, 45.46], "Moscow": [37.62, 55.75],
    "Munich": [11.58, 48.14], "Paris": [2.35, 48.86], "Prague": [14.42, 50.07],
    "Rome": [12.50, 41.90], "Saint Petersburg": [30.31, 59.94], "Sofia": [23.32, 42.70],
    "Stockholm": [18.06, 60.33], "Vienna": [16.36, 48.21], "Warsaw": [21.02, 52.24]}

#Helper code for plotting plans
#First, visualizing the cities.

with open("european_cities.csv", "r") as f:
    data = list(csv.reader(f, delimiter=';'))
    cities = data[0]

fig, ax = plt.subplots(figsize=(10, 10))
ax.imshow(europe_map, extent=[-14.56, 38.43, 37.697 + 0.3, 64.344 + 2.0], aspect="auto")

# Map (long, lat) to (x, y) for plotting
for city, location in city_coords.items():
    x, y = (location[0], location[1])
    plt.plot(x, y, 'ok', markersize=5)
    plt.text(x, y, city, fontsize=12)

#A method you can use to plot your plan on the map.
def plot_plan(city_order):
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(europe_map, extent=[-14.56, 38.43, 37.697 + 0.3, 64.344 + 2.0], aspect="auto")

    # Map (long, lat) to (x, y) for plotting
    for index in range(len(city_order) - 1):
        current_city_coords = city_coords[city_order[index]]
        next_city_coords = city_coords[city_order[index+1]]
        x, y = current_city_coords[0], current_city_coords[1]
        #Plotting a line to the next city
        next_x, next_y = next_city_coords[0], next_city_coords[1]
        plt.plot([x, next_x], [y, next_y])

        plt.plot(x, y, 'ok', markersize=5)
        plt.text(x, y, index, fontsize=12)
    #Finally, plotting from last to first city
    first_city_coords = city_coords[city_order[0]]
    first_x, first_y = first_city_coords[0], first_city_coords[1]
    plt.plot([next_x, first_x], [next_y, first_y])
    #Plotting a marker and index for the final city
    plt.plot(next_x, next_y, 'ok', markersize=5)
    plt.text(next_x, next_y, index+1, fontsize=12)
    plt.show()


# -----------------------------------------------Start of my own code ----------------------------------------------------



# Method for calculating the fitness of solutions    
def calculate_fitness(solution):
    dist = 0
    for x in range(0, len(solution)-1):
        city1 = data[0].index(solution[x])+1
        city2 = data[0].index(solution[x+1])
        dist += float(data[city1][city2])
    firstCity = data[0].index(solution[0])+1
    lastCity = data[0].index(solution[len(solution)-1])
    dist += float(data[firstCity][lastCity])
    return dist 

# Method for order-crossover between a pair of parents, producing two children
def order_crossover(a, b):

    ran1 = random.randint(0, len(a)-1)
    ran2 = random.randint(0, len(a)-1)

    while ran1 == ran2:
        ran2 = random.randint(0, len(a)-1)
    
    if ran1 > ran2:
        locus1 = ran2
        locus2 = ran1 
    else:
        locus1 = ran1
        locus2 = ran2

    c1 = [None for i in a]
    c2 = [None for i in b]

    # first child:

    for n in range(locus1, locus2):
        c1[n] = a[n]

    ls = []
    for n in range(locus2, len(b)):
        if b[n] not in c1:
            ls.append(b[n])
        
    for n in range(0, locus2):
        if b[n] not in c1:
            ls.append(b[n])

    counter = 0
    for n in range(locus2, len(c1)):
        if c1[n] is None:
            c1[n] = ls[counter]
            counter += 1 
    
    for n in range(0, locus2):
        if c1[n] is None:
            c1[n] = ls[counter]
            counter += 1

    # second child:
            
    for n in range(locus1, locus2):
        c2[n] = b[n]

    ls = []
    for n in range(locus2, len(a)):
        if a[n] not in c2:
            ls.append(a[n])
    
    for n in range(0, locus2):
        if a[n] not in c2:
            ls.append(a[n])
    
    counter = 0

    for n in range(locus2, len(c2)):
        if c2[n] is None:
            c2[n] = ls[counter]
            counter += 1
    for n in range(0, locus2):
        if c2[n] is None:
            c2[n] = ls[counter]
            counter += 1
    
    return c1, c2


def geneticAlgorithm(popSize, numberOfCities, numberOfGenerations):

    # Create a population with unique random solutions of the given size
    counter = 0
    population = []
    fittestSolutionDistances = []

    while len(population) != popSize:
        solution = []
        for n in range(numberOfCities):
            randomCity = random.randint(0, numberOfCities-1)
            while cities[randomCity] in solution:
                randomCity = random.randint(0, numberOfCities-1)
            if cities[randomCity] not in solution:
                solution.append(cities[randomCity])
        if solution not in population:
            population.append(solution)

    # Run the algorithm x amount of times:
            
    for n in range(numberOfGenerations):

        # I will be using a fitness proportionate selection (FPS)
        # Therefore, i will pick 3 random solutions from the population at a time, rank them, and choose 1 of them
        # based on percentages that are based on the ranking of the fitness, e.g the highest fitness has the best chance of becoming a parent

        chosen = []
        seen = set()

        # Selecting parents:
        while len(chosen) != len(population)/2:

            # Make sure the solutions are not the same 
            ind1 = random.randint(0, len(population)-1)
            ind2 = random.randint(0, len(population)-1)
            ind3 = random.randint(0, len(population)-1)
            while ind1 == ind2 or ind2 == ind3 or ind1 == ind3:
                ind1 = random.randint(0, len(population)-1)
                ind2 = random.randint(0, len(population)-1)
                ind3 = random.randint(0, len(population)-1)
            
            seen.add(ind1)
            seen.add(ind2)
            seen.add(ind3)

            rank2 = 0
            
            # Calculate the fitness (distance) of each of the 3 chosen solutions, and rank them based on fitness

            lowest = float('inf')
            lowID = 0 
            highest = 0
            highID = 0

            dist = calculate_fitness(population[ind1])

            if dist < lowest:
                lowest = dist 
                lowID = ind1 
            if dist > highest:
                highest = dist 
                highID = ind1
            else:
                rank2 = ind1

            dist = calculate_fitness(population[ind2])

            if dist < lowest:
                lowest = dist 
                lowID = ind2
            if dist > highest:
                highest = dist 
                highID = ind2 
            else:
                rank2 = ind2 
            
            dist = calculate_fitness(population[ind3])

            if dist < lowest:
                lowest = dist 
                lowID = ind3 
            if dist > highest:
                highest = dist 
                highID = ind3 
            else:
                rank2 = ind3

            rank1 = lowID 
            rank3 = highID 

            # choose between one of the ranks
            # rank1 has 3/6 chance, rank2 has 2/6 and rank3 has 1/6 chance of selection

            chosenOne = random.randint(1,6)
            if chosenOne == 1:
                chosen.append(population[rank3])
            elif chosenOne == 2 or chosenOne == 3:
                chosen.append(population[rank2])
            else:
                chosen.append(population[rank1])


        # From the selected parents, i will use order crossover to create the offspring:
        
        offSpring = []
        picked = set()

        while len(offSpring) <= len(chosen):

            if len(offSpring) == len(chosen)-1:
                # if we have paired x amount of times and are left with a single parent with noone to pair with
                # we mutate that parent, and create a single offspring
                randomP = random.randint(0, len(population)-1)
                p = population[randomP]
                indexOne = random.randint(0, len(p)-1)
                indexTwo = random.randint(0, len(p)-1)
                res = p[indexOne]
                p[indexOne] = p[indexTwo]
                p[indexTwo] = res
                offSpring.append(p)
                break
            # First select random pairs of parents to create offspring:
            p1 = random.randint(0, len(chosen)-1)
            p2 = random.randint(0, len(chosen)-1)
            while p1 == p2:
                p1 = random.randint(0, len(chosen)-1)
                p2 = random.randint(0, len(chosen)-1)
            
            picked.add(p1)
            picked.add(p2)

            children = order_crossover(population[p1], population[p2])
            offSpring.append(children[0])
            offSpring.append(children[1])
        
        # Now that we have the offSpring, we are left with the last part of the algorithm.
        # I will now select which of the solutions that survive into the next generation.
        # First, i will choose all of the offspring to be a part of the new population,
        # then i will choose the single most fit solution from the previous population, and add this one aswell.
        # The remaining spots will be filled with random solutions from the previous population (exploration).

        newPopulation = []

        for sol in offSpring:
            newPopulation.append(sol)

        # Finding the fittest of the previous population, and adding it to the new population:
        
        bestSol = None
        fitness = float('inf')

        for sol in population:
            fitnessSol = calculate_fitness(sol)
            if fitnessSol < fitness:
                fitness = fitnessSol
                bestSol = sol
        newPopulation.append(bestSol)

        # filling the new population with solutions from the previous population:

        for sol in population:
            if len(newPopulation) != len(population):
                newPopulation.append(sol)
        
        population = newPopulation 

        # find and store the fittest individual of the new population

        greatestFitness = float('inf')
        for sol in newPopulation:
            dist = calculate_fitness(sol)
            if dist < greatestFitness:
                greatestFitness = dist 
        
        fittestSolutionDistances.append(greatestFitness)


    # finally, we find and return the greatest solution after the last generation, along with the list of 
    # fittest solutions between all of the generations:
    
    optimalSolution = None 
    optimalFitness = float('inf')

    for solution in population:
        dist = calculate_fitness(solution)
        if dist < optimalFitness:
            optimalFitness = dist 
            optimalSolution = solution 
    
    return optimalSolution, optimalFitness, fittestSolutionDistances

# creating the graph

x_values = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
y_values = [10000, 9700, 9400, 9100, 8800, 8500, 8200, 7900, 7600, 7300, 7100]
plt.plot(x_values, y_values, label='Main Curve', linestyle='None')
plt.xlabel('Number of generations')
plt.ylabel('Fitness')

# Running the algorithm 20 times (100 generations each) for population sizes 100, 200 and 300.
# Then im finding the average best-fitted individual for every generation, amongst the runs, and plotting them into the graph
# I used some simplifying techniques to find the average, so the code may seem messy for this method, but it gets the job done
def plot_averages():

    populationSize = 100
    ls = []
    averageRun = []
    for x in range(3):

        dict = {}
        start = time.time()
        for x in range(20):
            ans = geneticAlgorithm(100, 10, 100)
            dict[x] = ans[2]
        end = time.time()
        print("Time used for 20 runs on population size ", populationSize, " : ", (end-start))


        # Calculating the average amongst the runs

        totalSum = 0
        for x in range(20):
            sum = 0
            for x, y in dict.items():
                for f in y:
                    sum += f
                sum = sum / len(y)
            totalSum += sum 
        average = totalSum/20
        ls.append(average)
        for x,y in dict.items():
            tot = 0
            for z in y:
                tot += z 
            tot = tot/len(y)
            if tot <= (average+50) or tot >= (average-50):
                populationSize += 100
                averageRun.append(y)
                break

    populationSize = 100
    for x in range(3):
        curveX = [i for i in range(100)]
        curveY = averageRun[x]
        plt.plot(curveX, curveY, label=populationSize)
        populationSize += 100

    plt.legend()
    plt.show()

plot_averages()