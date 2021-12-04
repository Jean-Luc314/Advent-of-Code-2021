### Functions
from functools import partial
from itertools import compress
notEmpty = lambda x : x != ""
def read_data(path):
    boardsAndDraws = list(map(lambda string : string.replace("\n", ""), open(path)))
    numbersDrawn = list(map(lambda string : int(string), boardsAndDraws[0].split(",")))
    boards = list(filter(notEmpty, boardsAndDraws[1:]))
    boards = list(map(lambda i : boards[5*i:5*(i + 1)], range(int(len(boards) / 5))))
    boards = list(map(lambda board : list(map(lambda row : row.split(" "), board)), boards))
    boards = list(map(lambda board : list(map(lambda row : list(map(int, filter(notEmpty, row))), board)), boards))
    return numbersDrawn, boards
playDraw = lambda scoreCard, draw, board : list(map(
    lambda rowBoard, rowScore : list(map(lambda valueBoard, valueScore : True if valueBoard == draw else valueScore,
                                         rowBoard,
                                         rowScore)),
    board,
    scoreCard))
detectWinningRow = lambda rowScores, board : list(compress(board, filter(lambda row : all(row), rowScores)))
findMarkedNumbers = lambda board, scoreCard : list(map(lambda rowBoard, rowScore : list(compress(rowBoard, rowScore)), board, scoreCard))
sumBoard = lambda board : sum(map(sum, board))
def scoreCardResult(numbersDrawn, board, scoreCard = [[False] * 5] * 5, drawTurn = 0):
    drawTurn += 1
    draw = numbersDrawn[0]
    numbersDrawn = numbersDrawn[1:len(numbersDrawn)]
    finalDraw = numbersDrawn[len(numbersDrawn) - 1]
    scoreCard = playDraw(scoreCard, draw, board)
    winningRow = detectWinningRow(scoreCard, board)
    winningColumn = detectWinningRow(zip(*scoreCard), board)
    markedNumbers = findMarkedNumbers(board, scoreCard)
    unmarkedSum = sumBoard(board) - sumBoard(markedNumbers)
    if len(winningRow) != 0:
        return unmarkedSum, draw, drawTurn
    elif len(winningColumn) != 0:
        return unmarkedSum, draw, drawTurn
    elif draw == finalDraw:
        return 0, draw, drawTurn
    else:
        return scoreCardResult(numbersDrawn, board, scoreCard, drawTurn)
delist = lambda x : x[0]
def bingo(path, strategy = "Win"):
    numbersDrawn, boards = read_data(path)
    unmakredSums, draw, times = list(zip(*map(partial(scoreCardResult, numbersDrawn), boards)))
    if strategy == "Win":
        stratFilter = list(map(lambda t : t == min(times), times))
    elif strategy == "Lose":
        stratFilter = list(map(lambda t : t == max(times), times))
    unmarkedSum = delist(list(compress(unmakredSums, stratFilter)))
    draw = delist(list(compress(draw, stratFilter)))
    return unmarkedSum * draw
### Part 1
## Example
path = "Inputs/Day 04 Example.txt"
bingo(path) # 4512
## Solution
path = "Inputs/Day 04.txt"
bingo(path) # 11536
### Part 2
## Example
path = "Inputs/Day 04 Example.txt"
bingo(path, strategy = "Lose") # 1924
## Solution
path = "Inputs/Day 04.txt"
bingo(path, strategy = "Lose") # 1284