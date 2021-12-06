### Functions
from itertools import chain
from functools import reduce, partial

def splitString(string, sep = ","):
    return string.split(sep)

def countClocks(clock, timers):
    return sum(map(lambda t : t == clock, timers))

def iterateGeneration(fishClockCounts, flush, maxClock = 8, reCycle = 6):
    fishRespawnCount = fishClockCounts[0]
    fishClockCounts[reCycle + 1] += fishRespawnCount
    fishClockCounts = fishClockCounts[1:maxClock + 1] + [fishRespawnCount]
    return fishClockCounts

def countFish(path, nDays, maxClock = 8, reCycle = 6):
    fishTimers = list(map(int, splitString(list(open(path))[0])))
    fishClocks = list(range(maxClock + 1))
    fishClockCounts = list(map(partial(countClocks, timers = fishTimers), fishClocks))
    days = list(range(nDays))
    fishClockCounts = reduce(partial(iterateGeneration,
                                     maxClock = maxClock,
                                     reCycle = reCycle),
                             [fishClockCounts] + days)
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
countFish(path, 256) # 26984457539

## Solution
path = "Inputs/Day 06.txt"
countFish(path, 256) # 1629570219571

## Part 1 Original (Very inefficient)
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

def totuple(var):
    if isinstance(var, tuple):
        return var
    else:
        return (var,)

def populateFish(fish, flush):
    return list(chain(*map(totuple, map(ageFish, fish))))

def countFishSlow(path, nDays):
    fishTimers = list(map(int, splitString(list(open(path))[0])))
    myFish = list(map(spawnFish, fishTimers))
    days = list(range(nDays))    
    myFish = reduce(populateFish, [myFish] + days)
    return len(myFish)