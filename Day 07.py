### Functions
from functools import partial
from itertools import compress
from compose import compose

def read_data(path):
    coords = list(open(path))[0].split(",")
    return list(map(int, coords))

def absDifference(coord, destination):
    return abs(coord - destination)

def triangle(n):
    return int(n * (n + 1) / 2)

def calcFuelConsumed(coords, destination, calcTriangle = False):
    fuelConsumed = map(partial(absDifference, destination = destination), coords)
    if calcTriangle:
        return list(map(triangle, fuelConsumed))
    else:
        return list(fuelConsumed)

def isEqual(a, b):
    return a == b

def minFuelMethod(path, calcTriangle = False):
    coords = read_data(path)
        
    coordRange = range(min(coords), max(coords) + 1)
    
    fuelConsumed = list(map(sum,
                            map(partial(calcFuelConsumed, 
                                        coords,
                                        calcTriangle = calcTriangle),
                                coordRange)))
    
    mostEfficient_lgl = list(map(partial(isEqual, min(fuelConsumed)), fuelConsumed))
    
    bestCoordinate = list(compress(coordRange, mostEfficient_lgl))[0]
    leastFuelConsumed = list(compress(fuelConsumed, mostEfficient_lgl))[0]
    
    return bestCoordinate, leastFuelConsumed
    
### Part 1
## Example
path = "Inputs/Day 07 Example.txt"
bestCoordinate, leastFuelConsumed = minFuelMethod(path)
leastFuelConsumed # 37
## Solution
path = "Inputs/Day 07.txt"
bestCoordinate, leastFuelConsumed = minFuelMethod(path)
leastFuelConsumed # 348664
### Part 2
## Example
path = "Inputs/Day 07 Example.txt"
bestCoordinate, leastFuelConsumed = minFuelMethod(path, calcTriangle = True)
leastFuelConsumed # 168
## Solution
path = "Inputs/Day 07.txt"
bestCoordinate, leastFuelConsumed = minFuelMethod(path, calcTriangle = True)
leastFuelConsumed # 100220525