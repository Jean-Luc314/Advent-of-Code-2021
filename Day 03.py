### Function
from compose import compose
from functools import partial
from itertools import compress
read_data = lambda path : list(map(lambda string : string.replace("\n", ""), open(path)))
splitData = lambda binaryDigits : list(map(lambda string : list(string), binaryDigits))
collectDigits = lambda digits : list(zip(*digits))
to_int = lambda listOfStrings : list(map(lambda string : int(string), listOfStrings))
binToDec = lambda listOfDigits : list(map(lambda x, i : x * 2 ** i, listOfDigits, reversed(range(len(listOfDigits)))))
## Part 1
def findMostCommon(listOfBits):
    digitsCount = len(listOfBits)
    onesCount = sum(listOfBits)
    zerosCount = digitsCount - onesCount
    if onesCount > zerosCount:
        return 1
    else:
        return 0
extractBinaryColumns = lambda path : compose(lambda x : list(x), partial(map, to_int), collectDigits, splitData, read_data)(path)
find_gamma = lambda binaries : compose(lambda x : list(x), partial(map, findMostCommon))(binaries)
find_epsilon = lambda binaries : list(map(lambda x : (x + 1) % 2, find_gamma(binaries)))
def part1(path):
    binaryColumns = extractBinaryColumns(path)
    gamma = find_gamma(binaryColumns)
    epsilon = find_epsilon(binaryColumns)
    powerConsumption = sum(binToDec(gamma)) * sum(binToDec(epsilon))
    return powerConsumption
## Part 2
def findMostCommonOxy(listOfBits):
    digitsCount = len(listOfBits)
    onesCount = sum(listOfBits)
    zerosCount = digitsCount - onesCount
    if onesCount >= zerosCount:
        return 1
    else:
        return 0
def findLeastCommonCO2(listOfBits):
    digitsCount = len(listOfBits)
    onesCount = sum(listOfBits)
    zerosCount = digitsCount - onesCount
    if onesCount >= zerosCount:
        return 0
    else:
        return 1
filterFactory = lambda filterType, binaryColumns : lambda predicateDepth : list(map(lambda bit : bit == filterType(binaryColumns[predicateDepth]), binaryColumns[predicateDepth]))
delist = lambda listofLists : list(map(lambda x : x[0], listofLists))
def decodeReport(binaryColumns, ratingType = "Oxygen", depth = 0):
    maxDepth = len(binaryColumns)
    if ratingType == "Oxygen":
        binaryFilter = filterFactory(findMostCommonOxy, binaryColumns)(predicateDepth = depth)
    elif ratingType == "CO2":
        binaryFilter = filterFactory(findLeastCommonCO2, binaryColumns)(predicateDepth = depth)
    else:
        return "ratingType must be either 'Oxygen' or 'CO2'."
    binaryColumns = list(map(lambda binaryFilter, binaryColumn : list(compress(binaryColumn, binaryFilter)), [binaryFilter] * len(binaryColumns), binaryColumns))
    depth += 1
    if (len(binaryColumns[0]) == 1) | (depth == maxDepth):
        return delist(binaryColumns)
    else:
        return decodeReport(binaryColumns, ratingType, depth)

def part2(path):
    binaryColumns = extractBinaryColumns(path)
    Oxygen = compose(sum, binToDec, partial(decodeReport, ratingType = "Oxygen"))(binaryColumns)
    CO2 = compose(sum, binToDec, partial(decodeReport, ratingType = "CO2"))(binaryColumns)
    return Oxygen * CO2

### Part 1
## Example
path = "Inputs/Day 03 Example.txt"
part1(path) # 198
## Solution
path = "Inputs/Day 03.txt"
part1(path) # 2640986

### Part 2
## Example
# life support = oxygen * CO2 scrubber
path = "Inputs/Day 03 Example.txt"
part2(path) # 230
## Solution
path = "Inputs/Day 03.txt"
part2(path) # 6822109
