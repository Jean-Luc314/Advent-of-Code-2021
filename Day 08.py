# Functions
from functools import partial
import pandas as pd
from itertools import compress
import string
from compose import compose
## Part 1
def countUniqueSegments(output):
    uniqueDigitsLengths = [2, 4, 3, 7]
    fourDigitSignal = output.split(" | ")[1]
    fourDigitSignal = fourDigitSignal.split(" ")
    segCounts = list(map(len, fourDigitSignal))
    segFilter = pd.DataFrame({"seg" : segCounts})["seg"].isin(uniqueDigitsLengths)
    return len(list(compress(fourDigitSignal, segFilter)))

def countTotalUniqueSegments(path):
    outputValues = list(map(lambda str : str.replace("\n", ""), open(path)))
    return sum(map(partial(countUniqueSegments), outputValues))
## Part 2
def identity(x):
    return x

def splitString(string):
    return list(map(identity, string))

def filterUniqueLengths(patterns, desiredLengths):
    return sorted(filter(lambda x : any(map(lambda y : len(x) == y,
                                       desiredLengths)),
                    patterns), key = len)

def filterNonUniqueLengths(patterns, desiredLengths):
    return sorted(filter(lambda x : all(map(lambda y : len(x) != y,
                                       desiredLengths)),
                    patterns), key = len)

def detect_c_and_f(patterns, a, b_and_d, e_and_g):
    candidate1 = patterns[0] - a - b_and_d - e_and_g
    candidate2 = patterns[1] - a - b_and_d - e_and_g
    candidate3 = patterns[2] - a - b_and_d - e_and_g
    if len(candidate1) == 2:
        return candidate1
    elif len(candidate2) == 2:
        return candidate2
    else:
        return candidate3

def detect_f(patterns, a, b_and_d, e_and_g):
    candidate1 = patterns[3] - a - b_and_d - e_and_g
    candidate2 = patterns[4] - a - b_and_d - e_and_g
    candidate3 = patterns[5] - a - b_and_d - e_and_g
    if len(candidate1) == 1:
        return candidate1
    elif len(candidate2) == 1:
        return candidate2
    else:
        return candidate3

def detect_b(patterns, a, c, f, e_and_g):
    candidate1 = patterns[3] - a - c - f - e_and_g
    candidate2 = patterns[4] - a - c - f - e_and_g
    candidate3 = patterns[5] - a - c - f - e_and_g
    if len(candidate1) == 1:
        return candidate1
    elif len(candidate2) == 1:
        return candidate2
    else:
        return candidate3

def detect_g(patterns, a , c, d, f):
    candidate1 = patterns[0] - a - c - d - f
    candidate2 = patterns[1] - a - c - d - f
    candidate3 = patterns[2] - a - c - d - f
    if len(candidate1) == 1:
        return candidate1
    elif len(candidate2) == 1:
        return candidate2
    else:
        return candidate3

def decodePatterns(nonUniqueDigitPattern, a, b_and_d, e_and_g):
    c_and_f = detect_c_and_f(nonUniqueDigitPattern, a, b_and_d, e_and_g)
    f = detect_f(nonUniqueDigitPattern, a, b_and_d, e_and_g)
    c = c_and_f - f
    b = detect_b(nonUniqueDigitPattern, a, c, f, e_and_g)
    d = b_and_d - b
    g = detect_g(nonUniqueDigitPattern, a, c, d, f)
    e = e_and_g - g
    decoded = {list(a)[0] : "a",
               list(b)[0] : "b",
               list(c)[0] : "c",
               list(d)[0] : "d",
               list(e)[0] : "e",
               list(f)[0] : "f",
               list(g)[0] : "g"}
    return decoded

def decodeOutput(output):
    uniquePattern, fourDigitSignal = output.split(" | ")
    uniquePattern = uniquePattern.split(" ")
    fourDigitSignal = fourDigitSignal.split(" ")
    
    uniqueDigits = [1, 7, 4, 8]
    uniqueDigitsLengths = [2, 3, 4, 7]
    uniqueDigitPattern = list(map(set, filterUniqueLengths(uniquePattern, uniqueDigitsLengths)))
    nonUniqueDigitPattern = list(map(set, filterNonUniqueLengths(uniquePattern, uniqueDigitsLengths)))
    digitDict = dict(zip(uniqueDigits, uniqueDigitPattern))
    
    a = digitDict[7] - digitDict[1]
    b_and_d = digitDict[4] - digitDict[1]
    e_and_g = digitDict[8] - digitDict[4] - a
    
    decoded = decodePatterns(nonUniqueDigitPattern, a, b_and_d, e_and_g)
    
    decodedSignals = list(map(lambda signal : "".join(sorted(list(map(lambda x : decoded[x],
                                                                      signal)))),
                              fourDigitSignal))
    
    sevenSegDisplay = {
        "abcefg" : 0,
        "cf" : 1,
        "acdeg" : 2,
        "acdfg" : 3,
        "bcdf" : 4,
        "abdfg" : 5,
        "abdefg" : 6,
        "acf" : 7,
        "abcdefg" : 8,
        "abcdfg" : 9
        }
    
    outputValue = int("".join(list(map(lambda x : str(sevenSegDisplay[x]), decodedSignals))))
    return outputValue

def part2(path):
    outputValues = list(map(lambda str : str.replace("\n", ""), open(path)))
    return sum(map(decodeOutput, outputValues))
# Part 1
## Example
path = "Inputs/Day 08 Example.txt"
countTotalUniqueSegments(path)
## Solution
path = "Inputs/Day 08.txt"
countTotalUniqueSegments(path)
# Part 2
## Example
path = "Inputs/Day 08 Example.txt"
part2(path)
## Solution
path = "Inputs/Day 08.txt"
part2(path)

