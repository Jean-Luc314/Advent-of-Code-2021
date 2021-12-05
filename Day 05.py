### Functions
from itertools import chain, compress
from functools import partial
read_data = lambda path : list(zip(*map(lambda string : string.replace("\n", "").split(" -> "),
                                        open(path))))
def convertToDict(input, name1, name2):
    x, y = list(zip(*map(lambda string : map(int, string.split(",")), input)))
    return {name1 : x, name2 : y}
isHorVert = lambda x1, y1, x2, y2 : (x1 == x2) | (y1 == y2)
def isOnLine(coordinate, xnode1, ynode1, xnode2, ynode2, checkDiag = False):
    x = coordinate[0]
    y = coordinate[1]
    horVert_lgl = isHorVert(xnode1, ynode1, xnode2, ynode2)
    diag_lgl = (not horVert_lgl) & ((x - xnode1) == (y - ynode1)) | ((x - xnode1) == -(y - ynode1))
    if xnode2 >= xnode1:
        xInRange = (x >= xnode1) & (x <= xnode2)
    else:
        xInRange = (x >= xnode2) & (x <= xnode1)
    if ynode2 >= ynode1:
        yInRange = (y >= ynode1) & (y <= ynode2)
    else:
        yInRange = (y >= ynode2) & (y <= ynode1)
    if not checkDiag:
        diag_lgl = False
    return xInRange & yInRange & (horVert_lgl | diag_lgl)
findIntersects = lambda xnode1, ynode1, xnode2, ynode2, gridTest, checkDiag : list(
    map(partial(isOnLine,
                gridTest,
                checkDiag = checkDiag),
        xnode1,
        ynode1,
        xnode2,
        ynode2))
countCoordIntersects = lambda gridTest, coordinates, checkDiag : sum(findIntersects(coordinates["x1"],
                                                                         coordinates["y1"],
                                                                         coordinates["x2"],
                                                                         coordinates["y2"],
                                                                         gridTest,
                                                                         checkDiag))
isMultipleIntersect = lambda count : count > 1
def countVentOverlaps(path, checkDiag = False):
    start, end = read_data(path)
    start = convertToDict(start, "x1", "y1")
    end = convertToDict(end, "x2", "y2")
    coordinates = {**start, **end}
    xmin = min(min(coordinates["x1"]), min(coordinates["x2"]))
    xmax = max(max(coordinates["x1"]), max(coordinates["x2"]))
    ymin = min(min(coordinates["y1"]), min(coordinates["y2"]))
    ymax = max(max(coordinates["y1"]), max(coordinates["y2"]))
    xRange = range(xmin, xmax + 1)
    yRange = range(ymin, ymax + 1)
    grid = list(map(lambda y : list(map(lambda x : (x, y), xRange)), yRange))
    gridList = list(chain(*grid))
    multipleIntersects = map(isMultipleIntersect,
                             map(partial(countCoordIntersects,
                                         coordinates = coordinates,
                                         checkDiag = checkDiag),
                                 gridList))
    multiIntersectCoords = list(compress(gridList, multipleIntersects))
    return len(multiIntersectCoords)

### Part 1
## Example
path = "Inputs/Day 05 Example.txt"
countVentOverlaps(path) # 5
## Solution
path = "Inputs/Day 05.txt"
countVentOverlaps(path) # 5690
### Part 2
## Example
path = "Inputs/Day 05 Example.txt"
countVentOverlaps(path, checkDiag = True) # 12
## Solution
path = "Inputs/Day 05.txt"
countVentOverlaps(path, checkDiag = True) # 17741

### Alternative
## Part 1 (Works for small inputs, but it is very, very slow for large inputs)
def drawLine(x1, y1, x2, y2):
    # Assumed Horixontal or Vertical
    if x2 >= x1:
        x = list(range(x1, x2 + 1))
    else:
        x = list(range(x2, x1 + 1))
    if y2 >= y1:
        y = list(range(y1, y2 + 1))
    else:
        y = list(range(y2, y1 + 1))
    if (x1 != x2) & (y1 != y2):
        x = None
        y = None
    elif (len(x) == 1) & (len(y) == 1):
        return x, y
    elif len(x) == 1:
        x *= len(y)
    else:
        y *= len(x)
    return x, y
filterNoneCoords = lambda x : x[0] is not None
pairCoords = lambda x : list(zip(*x))
def countOccurance(test, input, counter = 0):
    if input[0] == test:
        counter += 1
    if len(input) == 1:
        return counter
    else:
        input = input[1:len(input)]
        return countOccurance(test, input, counter)
def countVentOverlaps(path):
    start, end = read_data(path)
    start = convertToDict(start, "x1", "y1")
    end = convertToDict(end, "x2", "y2")
    coordinates = {**start, **end}
    
    line = list(map(pairCoords,
                    filter(filterNoneCoords,
                           map(drawLine,
                               coordinates["x1"],
                               coordinates["y1"],
                               coordinates["x2"],
                               coordinates["y2"]))))
    ventCoords = list(chain(*line))
    uniqueVentCoords = list(set(ventCoords))
    coordCoveredCount = list(map(partial(countOccurance, input = ventCoords),
                                 uniqueVentCoords))
    
    ventOverlaps = list(compress(uniqueVentCoords, filter(lambda x : x >= 2, coordCoveredCount)))
    return len(ventOverlaps)