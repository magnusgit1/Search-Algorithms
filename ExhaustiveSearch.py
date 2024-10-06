#Precode to collect cities and for plots:
import csv
from itertools import permutations
import time 
import matplotlib.pyplot as plt
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


def exhaustiveSearch(numberOfCities):

    # creating a subset of a number of cities dictated by the argument to the function
    subsetOfCities = [cities[n] for n in range(numberOfCities)]
    # creating a list with all the possible permutations of the subset with itertools' "permuations"
    allTours = list(permutations(subsetOfCities))

    shortestPath = []
    # initializing the shortest distance to be infinite
    shortestTravellingDistance = float('inf')

    # for every permuation:
    for path in allTours:

        # store the total distance travelled 
        totalDistanceTravelled = 0

        # calculate all the distances between the cities in the plan
        for i in range(0, len(path)-1):

            # finding the index of where the first city's distances are, aswell as the index of the adjacent (i+1) city
            # +1 in the distances of the starting city because the first index of "data" contains the cities, and not distances
            cityIndex = data[0].index(path[i]) +1
            nextCityIndex = data[0].index(path[i+1])

            # finding the distance and adding it to the total distance travelled
            distance = float(data[cityIndex][nextCityIndex])
            totalDistanceTravelled += distance
        
        # adding distance between the starting- and endpoint in the same manner
        startingCityIndex = data[0].index(path[0]) +1
        endCityIndex = data[0].index(path[len(path)-1]) 
        distance = float(data[startingCityIndex][endCityIndex])
        totalDistanceTravelled += distance

        # condition that checks if a path is the shortest one yet, if so, store it and its total distance
        if totalDistanceTravelled < shortestTravellingDistance:
            shortestPath = path
            shortestTravellingDistance = totalDistanceTravelled
    
    return shortestPath, shortestTravellingDistance

# measuring the time and printing the shortest path and its distance, for 6-10 cities
for i in range(6, 11):
    start = time.time()
    ans = exhaustiveSearch(i)
    end = time.time()
    print("With ", i, " cities: \n", "Shortest path: ", ans[0], "\n", "Distance: ", ans[1], "\n", "Calculation time: ", (end-start))

plot_plan(exhaustiveSearch(6)[0])
plot_plan(exhaustiveSearch(10)[0])