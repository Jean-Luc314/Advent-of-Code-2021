# Functions
from functools import partial, reduce
from compose import compose
from itertools import compress

def detectError(line, openingCharacter = " ", closingCharacter = " ", detectComplete = False):
    closedCharacter = {"(" : ")", "[" : "]", "{" : "}", "<" : ">",
                       ")" : ")", "]" : "]", "}" : "}", ">" : ">"}
    firstCharacter = line[0]
    isClosedCharacter = firstCharacter == closedCharacter[firstCharacter]
    
    if isClosedCharacter:
        matchLastClosingCharacter = closedCharacter[openingCharacter[-1]] == firstCharacter
    else:
        matchLastClosingCharacter = True
    
    if not matchLastClosingCharacter:
        if not detectComplete:
            return firstCharacter
    elif isClosedCharacter & matchLastClosingCharacter:
        if len(line) == 1:
            if not detectComplete:
                return None
            else:
                return closingCharacter[0:-1]
        else:
            line = line[1:len(line)]
            openingCharacter = openingCharacter[0:-1]
            closingCharacter = closingCharacter[0:-1]
            return detectError(line, openingCharacter, closingCharacter, detectComplete)
    else:
        if len(line) == 1:
            if not detectComplete:
                return None
            else:
                return closingCharacter + closedCharacter[firstCharacter]
        else:
            line = line[1:len(line)]
            openingCharacter += firstCharacter
            closingCharacter += closedCharacter[firstCharacter]
            return detectError(line, openingCharacter, closingCharacter, detectComplete)


def convertToSyntaxPoints(error):
    syntaxPoints = {")" : 3, "]" : 57, "}" : 1197, ">" : 25137}
    return syntaxPoints[error]

def convertToAutoCompletePoints(missing):
    autoCompletePoints = {")" : 1, "]" : 2, "}" : 3, ">" : 4}
    return autoCompletePoints[missing]

def notNone(x):
    return x is not None

def isNone(x):
    return x is None

def sumScore(path):
    subsytem = list(map(lambda string : string.replace("\n", ""),
                        open(path)))
    totalScore = compose(sum,
                         partial(map, convertToSyntaxPoints),
                         partial(filter, notNone),
                         partial(map, detectError))(subsytem)
    return totalScore

def reverse(string):
    return string[::-1]

def cutLast(string):
    return string[0:-1]

def prependSpace(string):
    return " " + string

def autoCompleteScore(flush, missing):
    if flush == " ":
        flush = 0
    return 5 * flush + convertToAutoCompletePoints(missing)

def calcAutoScore(path):
    subsytem = list(map(lambda string : string.replace("\n", ""),
                        open(path)))
    
    errors = map(detectError, subsytem)
    incompleteFilter = map(isNone, errors)
    
    scores = compose(sorted,
                     partial(map, partial(reduce, autoCompleteScore)),
                     partial(map, prependSpace),
                     partial(map, cutLast),
                     partial(map, reverse),
                     partial(map, partial(detectError, detectComplete = True)),
                     partial(compress, selectors = incompleteFilter)) (subsytem)
    
    return scores[int((len(scores) - 1) / 2)]

# Part 1
## Example
path = "Inputs/Day 10 Example.txt"
sumScore(path) # 26397
## Solution
path = "Inputs/Day 10.txt"
sumScore(path) # 319329
# Part 2
## Example
path = "Inputs/Day 10 Example.txt"
calcAutoScore(path) # 288957
## Solution
path = "Inputs/Day 10.txt"
calcAutoScore(path) # 3515583998