### Functions
from functools import partial, reduce
from compose import compose
read_data = lambda path : list(map(lambda string : string.replace("\n", ""), open(path)))
splitData = lambda commands : list(map(lambda string : string.split(" "), commands))
## Part 1
identifyDirections = lambda splitData : set(list(zip(*splitData))[0])
sumDirection = lambda dirDist, direction : sum(list(map(lambda dirDist : int(dirDist[1]), filter(lambda dirDist : dirDist[0] == direction, dirDist))))
def calcCoords(dirDist):
    uniqueDirections = identifyDirections(dirDist)
    sumSteps = list(map(partial(sumDirection, dirDist), uniqueDirections))
    stepDict = dict(zip(uniqueDirections, sumSteps))
    vertical = stepDict["down"] - stepDict["up"]
    horizontal = stepDict["forward"]
    return vertical, horizontal
pairProduct = lambda x : x[0] * x[1]
## Part 2
def calcAxis(current, instruction):
    direction = instruction[0]
    stepSize = int(instruction[1])
    if direction == "down":
        current[2] += stepSize
    elif direction == "up":
        current[2] -= stepSize
    elif direction == "forward":
        current[0] += stepSize
        current[1] += stepSize * current[2]
    return current
horTimesDepth = lambda coords : coords[0] * coords[1]
prependCenter = lambda dirDist : [[0] * 3] + dirDist

### Part 1
## Example
path = "Inputs/Day 02 Example.txt"
compose(pairProduct, calcCoords, splitData, read_data)(path)
## Solution
path = "Inputs/Day 02.txt"
compose(pairProduct, calcCoords, splitData, read_data)(path)

### Part 2
## Example
# Now need a recursion.
path = "Inputs/Day 02 Example.txt"
compose(horTimesDepth, partial(reduce, calcAxis), prependCenter, splitData, read_data)(path)
## Solution
path = "Inputs/Day 02.txt"
compose(horTimesDepth, partial(reduce, calcAxis), prependCenter, splitData, read_data)(path)