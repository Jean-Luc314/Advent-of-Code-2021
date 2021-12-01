### Functions
from compose import compose
didIncrease = lambda x, y : y > x
countIncreases = lambda data : sum(list(map(didIncrease, data[0:len(data)-1], data[1:len(data)])))
def read_data(path):
    measurements_str = list(open(path))
    measurements = list(map(lambda string : int(string.replace("\n", "")), measurements_str))
    return measurements
sumTriples = lambda measurements : list(map(lambda i : sum(measurements[i:i + 3]), range(len(measurements) - 2)))

### Part 1

## Example
measurements = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
countIncreases(measurements)

## Solution
compose(countIncreases, read_data)("Inputs/Day 01.txt")

### Part 2
# Need to iterate over all triples, summing each one e.g.
#[
#    sum(measurements[0:3]),
#    sum(measurements[1:4]),
#    ...,
#    sum(measurements[len(measurements)-3:len(measurements)])
#]


## Example
measurements = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
countIncreases(sumTriples(measurements))

## Solution
compose(countIncreases, sumTriples, read_data)("Inputs/Day 01.txt")
