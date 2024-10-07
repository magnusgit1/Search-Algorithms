
#Precode used to collect cities and for plots:

import csv
import matplotlib.pyplot as plt
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



def hillClimber(numberOfCities):

    # Creating the subset of the first n cities according to the function-argument
    subsetOfCities = [cities[n] for n in range(numberOfCities)]

    # Creating a random starting solution

    startingSolution = []

    while len(startingSolution) != len(subsetOfCities):
        randomCity = random.randint(0, numberOfCities-1) 
        if cities[randomCity] not in startingSolution:
            startingSolution.append(cities[randomCity])
    
    # Storing the current solution's distance
    solutionDistance = 0.0
    for n in range(0, len(startingSolution)-1):
        index1 = data[0].index(startingSolution[n])+1
        index2 = data[0].index(startingSolution[n+1])
        solutionDistance += float(data[index1][index2])
    
    # adding start-to-endpoint distance
    firstCityIndex = data[0].index(startingSolution[0])+1
    lastCityIndex = data[0].index(startingSolution[len(startingSolution)-1]) 
    solutionDistance += float(data[firstCityIndex][lastCityIndex])


    # Create 5 neighbouring solutions, which swaps 2 random connections from the starting solution
    # Choose the neighbour with the best/shortests tour, and replace this with the current solution if it is better
    # Repeat this process 1000 times
    cntr = 0
    while cntr < 1000:
        cntr += 1

        neighbours = []
        used = set()

        # Create the neighbours
        for n in range(5):
            solutionCopy = startingSolution
            neighbour = []
            randomIndex1 = random.randint(0, len(solutionCopy)-1)
            randomIndex2 = random.randint(0, len(solutionCopy)-1)

            # Make sure the swapping indexes arent the same or used before
            while randomIndex1 == randomIndex2 or (randomIndex1, randomIndex2) in used:
                randomIndex1 = random.randint(0, len(solutionCopy)-1)
                randomIndex2 = random.randint(0, len(solutionCopy)-1)
            
            used.add((randomIndex1, randomIndex2))
            
            res = solutionCopy[randomIndex1]
            solutionCopy[randomIndex1] = solutionCopy[randomIndex2]
            solutionCopy[randomIndex2] = res
            neighbour = solutionCopy
            neighbours.append(neighbour)
        
        
        # for all the neighbours, calculate their distance, and find the one with the best tour
        bestNeighbour = None
        # bestDistance initialized with inf so that we always get one of the neighbours to be the best neighbour
        bestDistance = float('inf')
        for nb in neighbours:
            currDist = 0.0
            for n in range(0, len(nb)-1):
                indexNb1 = cities.index(nb[n]) +1
                indexNb2 = cities.index(nb[n+1])
                currDist += float(data[indexNb1][indexNb2])
            # adding start and endpoint
            firstCityInd = data[0].index(nb[0])+1
            lastCityInd = data[0].index(nb[len(nb)-1]) 
            currDist += float(data[firstCityInd][lastCityInd])
            if currDist < bestDistance:
                bestNeighbour = nb
                bestDistance = currDist

        # if the best neighbour is better than the current solution, replace the solution with the neighbour and repeat the process
        # if not, return the best solution and we have found our local optima
        if bestDistance <= solutionDistance:
            startingSolution = bestNeighbour
            solutionDistance = bestDistance
    
    return startingSolution, solutionDistance

# Method to run the algorithm with x amount of cities y amount of times, and finding the best/worst/mean tours

def runClimber(cities, runs):

    bestTour = []
    bestDistance = float('inf')

    worstTour = []
    worstDistance = 0
    totalDist = 0.0
    for n in range(runs):
        ans = hillClimber(cities)
        totalDist += ans[1]
        if ans[1] > worstDistance:
            worstTour = ans[0]
            worstDistance = ans[1]
        if ans[1] < bestDistance:
            bestTour = ans[0]
            bestDistance = ans[1]

    print("Best tour with ", cities, " cities: ", bestTour, " Distance: ", bestDistance)
    print("Worst tour with ", cities, " cities: ", worstTour, " Distance: ", worstDistance)
    print("Avarage distance in all runs: ", totalDist/runs)
    return bestTour

# 20 runs with both 10 cities and 24 cities, presenting the best, worst and avarage tour distances.
plt10 = runClimber(10, 20)
print("\n")
plt24 = runClimber(24, 20)