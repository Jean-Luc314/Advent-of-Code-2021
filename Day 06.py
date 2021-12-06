### Functions
from itertools import chain
from functools import reduce, partial
## Part 1 Very inefficient
def splitString(string, sep = ","):
    return string.split(sep)

class laternfish:
    timer = 8

def spawnFish(timer):
    fish = laternfish()
    fish.timer = timer
    return fish

def ageFish(fish):
    fish.timer -= 1
    if fish.timer == -1:
        fish.timer = 6
        babyFish = laternfish()
        return fish, babyFish
    else:
        return fish

def isNotNone(x):
    return x is not None

def totuple(var):
    if isinstance(var, tuple):
        return var
    else:
        return (var,)

def populateFish(fish, flush):
    return list(chain(*map(totuple, map(ageFish, fish))))

def countFish(path, nDays):
    fishTimers = list(map(int, splitString(list(open(path))[0])))
    myFish = list(map(spawnFish, fishTimers))
    days = list(range(nDays))
    days = [myFish] + days
    
    myFish = reduce(populateFish, days)
    return len(myFish)
## Part 2
def countClocks(clock, timers):
    return sum(map(lambda t : t == clock, timers))

def iterateGeneration(fishClockCounts, flush, maxClock):
    fishRespawnCount = fishClockCounts[0]
    fishClockCounts[7] += fishRespawnCount
    fishClockCounts = fishClockCounts[1:maxClock + 1] + [fishRespawnCount]
    return fishClockCounts

def countFishFast(path, nDays):
    fishTimers = list(map(int, splitString(list(open(path))[0])))
    maxClock = 8
    fishClocks = list(range(maxClock + 1))
    fishClockCounts = list(map(partial(countClocks, timers = fishTimers), fishClocks))
    days = list(range(nDays))
    days = [fishClockCounts] + days
    
    fishClockCounts = reduce(partial(iterateGeneration, maxClock = 8), days)
    return sum(fishClockCounts)

### Part 1
## Example
path = "Inputs/Day 06 Example.txt"
countFish(path, 18) # 26
countFish(path, 80) # 5934
## Solution
path = "Inputs/Day 06.txt"
countFish(path, 80) # 359344
### Part 2
## Example
path = "Inputs/Day 06 Example.txt"
countFishFast(path, 256) # 26984457539

## Solution
path = "Inputs/Day 06.txt"
countFishFast(path, 256) # 1629570219571