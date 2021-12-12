# Functions
from itertools import chain, compress
from functools import partial
from numpy.core.fromnumeric import prod

def read_data(path):
    return list(map(lambda x : list(map(int, x.replace("\n", ""))), open(path)))

def leftCoord(heightMap, rowCoord, colCoord):
    return heightMap[rowCoord][colCoord - 1]

def rightCoord(heightMap, rowCoord, colCoord):
    return heightMap[rowCoord][colCoord + 1]

def downCoord(heightMap, rowCoord, colCoord):
    return heightMap[rowCoord + 1][colCoord]

def upCoord(heightMap, rowCoord, colCoord):
    return heightMap[rowCoord - 1][colCoord]

def testLeft(heightMap, rowCoord, colCoord, basinTest = False):
    if not basinTest:
        return heightMap[rowCoord][colCoord] < leftCoord(heightMap, rowCoord, colCoord)
    else:
        isNine = heightMap[rowCoord][colCoord] == 9
        isAdjacent = heightMap[rowCoord][colCoord] == leftCoord(heightMap, rowCoord, colCoord) - 1
        return (not isNine) & isAdjacent

def testRight(heightMap, rowCoord, colCoord, basinTest = False):
    if not basinTest:
        return heightMap[rowCoord][colCoord] < rightCoord(heightMap, rowCoord, colCoord)
    else:
        isNine = heightMap[rowCoord][colCoord] == 9
        isAdjacent = heightMap[rowCoord][colCoord] == rightCoord(heightMap, rowCoord, colCoord) - 1
        return (not isNine) & isAdjacent

def testDown(heightMap, rowCoord, colCoord, basinTest = False):
    if not basinTest:
        return heightMap[rowCoord][colCoord] < downCoord(heightMap, rowCoord, colCoord)
    else:
        isNine = heightMap[rowCoord][colCoord] == 9
        isAdjacent = heightMap[rowCoord][colCoord] == downCoord(heightMap, rowCoord, colCoord) - 1
        return (not isNine) & isAdjacent

def testUp(heightMap, rowCoord, colCoord, basinTest = False):
    if not basinTest:
        return heightMap[rowCoord][colCoord] < upCoord(heightMap, rowCoord, colCoord)
    else:
        isNine = heightMap[rowCoord][colCoord] == 9
        isAdjacent = heightMap[rowCoord][colCoord] == upCoord(heightMap, rowCoord, colCoord) - 1
        return (not isNine) & isAdjacent

def isLowPoint(coords, heightMap, basinTest = False):
    rowCoord = coords[0]
    colCoord = coords[1]
    nrows = len(heightMap)
    ncols = len(heightMap[0])
    topLeft = (rowCoord == 0) & (colCoord == 0)
    topRight = (rowCoord == 0) & (colCoord == ncols - 1)
    bottomLeft = (rowCoord == nrows - 1) & (colCoord == 0)
    bottomRight = (rowCoord == nrows - 1) & (colCoord == ncols - 1)
    corner = any([topLeft, topRight, bottomLeft, bottomRight])
    topEdge = rowCoord == 0
    bottomEdge = rowCoord == nrows - 1
    leftEdge = colCoord == 0
    rightEdge = colCoord == ncols - 1
    if topLeft:
        if not basinTest:
            right = testRight(heightMap, rowCoord, colCoord)
            down = testDown(heightMap, rowCoord, colCoord)
            return right & down
        else:
            right = testRight(heightMap, rowCoord, colCoord, basinTest)
            down = testDown(heightMap, rowCoord, colCoord, basinTest)
            basinCoords = []
            if right:
                basinCoords += [[rowCoord, colCoord + 1]]
            if down:
                basinCoords += [[rowCoord + 1, colCoord]]
            return basinCoords
    elif topRight:
        if not basinTest:
            left = testLeft(heightMap, rowCoord, colCoord)
            down = testDown(heightMap, rowCoord, colCoord)
            return left & down
        else:
            left = testLeft(heightMap, rowCoord, colCoord, basinTest)
            down = testDown(heightMap, rowCoord, colCoord, basinTest)
            basinCoords = []
            if left:
                basinCoords += [[rowCoord, colCoord - 1]]
            if down:
                basinCoords += [[rowCoord + 1, colCoord]]
            return basinCoords
    elif bottomLeft:
        if not basinTest:
            right = testRight(heightMap, rowCoord, colCoord)
            up = testUp(heightMap, rowCoord, colCoord)
            return right & up
        else:
            right = testRight(heightMap, rowCoord, colCoord, basinTest)
            up = testUp(heightMap, rowCoord, colCoord, basinTest)
            basinCoords = []
            if right:
                basinCoords += [[rowCoord, colCoord + 1]]
            if up:
                basinCoords += [[rowCoord - 1, colCoord]]
            return basinCoords
    elif bottomRight:
        if not basinTest:
            left = testLeft(heightMap, rowCoord, colCoord)
            up = testUp(heightMap, rowCoord, colCoord)
            return left & up
        else:
            left = testLeft(heightMap, rowCoord, colCoord, basinTest)
            up = testUp(heightMap, rowCoord, colCoord, basinTest)
            basinCoords = []
            if left:
                basinCoords += [[rowCoord, colCoord - 1]]
            if up:
                basinCoords += [[rowCoord - 1, colCoord]]
            return basinCoords
    elif (not corner) & topEdge:
        if not basinTest:
            left = testLeft(heightMap, rowCoord, colCoord)
            right = testRight(heightMap, rowCoord, colCoord)
            down = testDown(heightMap, rowCoord, colCoord)
            return left & right & down
        else:
            left = testLeft(heightMap, rowCoord, colCoord, basinTest)
            right = testRight(heightMap, rowCoord, colCoord, basinTest)
            down = testDown(heightMap, rowCoord, colCoord, basinTest)
            basinCoords = []
            if left:
                basinCoords += [[rowCoord, colCoord - 1]]
            if right:
                basinCoords += [[rowCoord, colCoord + 1]]
            if down:
                basinCoords += [[rowCoord + 1, colCoord]]
            return basinCoords
    elif (not corner) & bottomEdge:
        if not basinTest:
            left = testLeft(heightMap, rowCoord, colCoord)
            right = testRight(heightMap, rowCoord, colCoord)
            up = testUp(heightMap, rowCoord, colCoord)
            return left & right & up
        else:
            left = testLeft(heightMap, rowCoord, colCoord, basinTest)
            right = testRight(heightMap, rowCoord, colCoord, basinTest)
            up = testUp(heightMap, rowCoord, colCoord, basinTest)
            basinCoords = []
            if left:
                basinCoords += [[rowCoord, colCoord - 1]]
            if right:
                basinCoords += [[rowCoord, colCoord + 1]]
            if up:
                basinCoords += [[rowCoord - 1, colCoord]]
            return basinCoords
    elif (not corner) & leftEdge:
        if not basinTest:
            right = testRight(heightMap, rowCoord, colCoord)
            up = testUp(heightMap, rowCoord, colCoord)
            down = testDown(heightMap, rowCoord, colCoord)
            return right & up & down
        else:
            right = testRight(heightMap, rowCoord, colCoord, basinTest)
            up = testUp(heightMap, rowCoord, colCoord, basinTest)
            down = testDown(heightMap, rowCoord, colCoord, basinTest)
            basinCoords = []
            if right:
                basinCoords += [[rowCoord, colCoord + 1]]
            if up:
                basinCoords += [[rowCoord - 1, colCoord]]
            if down:
                basinCoords += [[rowCoord + 1, colCoord]]
            return basinCoords
    elif (not corner) & rightEdge:
        if not basinTest:
            left = testLeft(heightMap, rowCoord, colCoord)
            up = testUp(heightMap, rowCoord, colCoord)
            down = testDown(heightMap, rowCoord, colCoord)
            return left & up & down
        else:
            left = testLeft(heightMap, rowCoord, colCoord, basinTest)
            up = testUp(heightMap, rowCoord, colCoord, basinTest)
            down = testDown(heightMap, rowCoord, colCoord, basinTest)
            basinCoords = []
            if left:
                basinCoords += [[rowCoord, colCoord - 1]]
            if up:
                basinCoords += [[rowCoord - 1, colCoord]]
            if down:
                basinCoords += [[rowCoord + 1, colCoord]]
            return basinCoords
    else:
        if not basinTest:
            right = testRight(heightMap, rowCoord, colCoord)
            left = testLeft(heightMap, rowCoord, colCoord)
            up = testUp(heightMap, rowCoord, colCoord)
            down = testDown(heightMap, rowCoord, colCoord)
            return right & left & up & down
        else:
            right = testRight(heightMap, rowCoord, colCoord, basinTest)
            left = testLeft(heightMap, rowCoord, colCoord, basinTest)
            up = testUp(heightMap, rowCoord, colCoord, basinTest)
            down = testDown(heightMap, rowCoord, colCoord, basinTest)
            basinCoords = []
            if left:
                basinCoords += [[rowCoord, colCoord - 1]]
            if right:
                basinCoords += [[rowCoord, colCoord + 1]]
            if up:
                basinCoords += [[rowCoord - 1, colCoord]]
            if down:
                basinCoords += [[rowCoord + 1, colCoord]]
            return basinCoords

def findLowCoords(heightMap):
    nrows = len(heightMap)
    ncols = len(heightMap[0])
    coords = list(chain(*map(lambda row : list(map(lambda col : [row, col], range(ncols))), range(nrows))))
    lowPointCoords = list(compress(coords, map(partial(isLowPoint, heightMap = heightMap, basinTest = False), coords)))
    return lowPointCoords

def sumCoords(heightMap, Coords):
    return sum(map(lambda coord : heightMap[coord[0]][coord[1]] + 1, Coords))

def part1(path):
    heightMap = read_data(path)
    return sumCoords(heightMap, findLowCoords(heightMap))
## Part 2
def findBasins(heightMap, coords):
    newCoords = list(chain(*map(partial(isLowPoint, heightMap = heightMap, basinTest = True), coords)))
    if len(newCoords) == 0:
        return coords
    else:
        return coords + findBasins(heightMap, newCoords)

def vecCountIn(vec, test):
    return sum(map(lambda x : x == test, vec))

def removeDuplicates(vec):
    return list(map(lambda i : vecCountIn(vec[0:i + 1], vec[i]) <= 1, range(len(vec))))

def findAllBasins(coord, heightMap):
    basins = findBasins(heightMap, [coord])
    basins = list(compress(basins, removeDuplicates(basins)))
    basins = list(filter(lambda x : heightMap[x[0]][x[1]] != 9, basins))
    return basins

def basinLenProduct(path):
    heightMap = read_data(path)
    coords = findLowCoords(heightMap)
    basins = sorted(map(partial(findAllBasins, heightMap = heightMap), coords),
                    key = len, 
                    reverse = True)
    return prod(list(map(len, basins[0:3])))

# Part 1
## Example
path = "Inputs/Day 09 Example.txt"
part1(path) # 15
## Solution
path = "Inputs/Day 09.txt"
part1(path) # 560
# Part 2
## Example
path = "Inputs/Day 09 Example.txt"
basinLenProduct(path) # 1134
## Solution
path = "Inputs/Day 09.txt"
basinLenProduct(path) # Wrong 483664