from cmu_graphics import *
import math
import random

def onAppStart(app):
    app.rows = 15
    app.cols = 10
    app.boardLeft = 95
    app.boardTop = 50
    app.boardWidth = app.width - 95*2
    app.boardHeight = app.height- 50 - 30
    app.cellBorderWidth = 1
    reset(app)

def reset(app):
    app.board = [([None] * app.cols) for row in range(app.rows)]
    app.piece = None
    app.rowsPoped = 0
    app.paused = False
    app.count = 0
    app.gameOver = False
    app.points = 0
    loadTetrisPieces(app)
    loadNextPiece(app)
    
########################
#piece starts
########################

def loadTetrisPieces(app):
    iPiece = [[  True,  True,  True,  True ]]
    jPiece = [[  True, False, False ],
              [  True,  True,  True ]]
    lPiece = [[ False, False,  True ],
              [  True,  True,  True ]]
    oPiece = [[  True,  True ],
              [  True,  True ]]
    sPiece = [[ False,  True,  True ],
              [  True,  True, False ]]
    tPiece = [[ False,  True, False ],
              [  True,  True,  True ]]
    zPiece = [[  True,  True, False ],
              [ False,  True,  True ]] 
    app.tetrisPieces = [ iPiece, jPiece, lPiece, oPiece,
                         sPiece, tPiece, zPiece ]
    app.tetrisPieceColors = [ 'red', 'yellow', 'magenta', 'pink',
                              'cyan', 'green', 'orange' ]

def loadPiece(app, pieceIndex):
    app.piece = app.tetrisPieces[pieceIndex]
    pieceWidth = len(app.piece[0])
    app.pieceTopRow = 0
    if ((app.cols - pieceWidth) % 2 == 1) and (pieceWidth % 2 == 1):
        app.pieceLeftCol = app.cols//2 - pieceWidth//2 - 1
    else:
        app.pieceLeftCol = app.cols//2 - pieceWidth//2
    app.pieceColor = app.tetrisPieceColors[pieceIndex]

def loadNextPiece(app):
    pieceIndex = random.randrange(len(app.tetrisPieces))
    loadPiece(app, pieceIndex)
    if pieceIsLegal(app):
        return
    else:
        app.gameOver = True

##### moving piece helper functions
def rotatePieceClockwise(app):
    #reserve old parameters
    oldPiece = app.piece
    oldTopRow = app.pieceTopRow
    oldLeftCol = app.pieceLeftCol
    app.piece = rotate2dListClockwise(app.piece)
    #find the center of the piece for rotation
    oldRows = len(oldPiece)
    oldCols = len(oldPiece[0])
    centerRow = oldTopRow + oldRows//2
    centerCol = oldLeftCol + oldCols//2
    newRows = len(app.piece)
    newCols = len(app.piece[0])
    app.pieceTopRow = centerRow - newRows//2
    app.pieceLeftCol = centerCol - newCols//2
    #if piece is legal
    if pieceIsLegal(app):
        return
    else:
        app.piece = oldPiece
        app.pieceTopRow = oldTopRow
        app.pieceLeftCol = oldLeftCol

def rotate2dListClockwise(L):
    oldRows, oldCols = len(L), len(L[0])
    newRows, newCols = oldCols, oldRows
    M = []
    for oldCol in range(oldCols):
        newCurrRow = []
        for oldRow in range(oldRows-1, -1, -1): 
                            #from last one of old rows to 0
            newCurrRow.append(L[oldRow][oldCol])
        M.append(newCurrRow)
    return M

def hardDropPiece(app):
    while movePiece(app, +1, 0):
        pass

def movePiece(app, drow, dcol):
    app.pieceTopRow += drow
    app.pieceLeftCol += dcol
    if pieceIsLegal(app):
        return True
    else:
        app.pieceTopRow -= drow
        app.pieceLeftCol -= dcol
        return False

def pieceIsLegal(app):
    rows = len(app.piece)
    cols = len(app.piece[0])
    if app.pieceTopRow < 0:
        return False
    elif app.pieceLeftCol < 0:
        return False
    elif app.pieceTopRow + rows > app.rows:
        return False
    elif app.pieceLeftCol + cols > app.cols:
        return False
    else:
        for row in range(rows):
            for col in range(cols):
                if not app.piece[row][col] == False:
                    rowInBoard = app.pieceTopRow+row
                    colInBoard = app.pieceLeftCol+col
                    # if intersect with other pieces
                    if not app.board[rowInBoard][colInBoard] == None:
                        return False
    return True

def placePieceOnBoard(app):
    rows = len(app.piece)
    cols = len(app.piece[0])
    for row in range(rows):
        for col in range(cols):
            if not app.piece[row][col] == False:
                rowInBoard = app.pieceTopRow+row
                colInBoard = app.pieceLeftCol+col
                app.board[rowInBoard][colInBoard] = app.pieceColor
    
    

#piece ends
########################
#DRAW starts
########################

def redrawAll(app):
    if not app.gameOver:
        drawLabel('Tetris', app.width/2, 30, size=16)
        drawBoard(app)
        if not app.piece == None:
            drawPiece(app)
        drawBoardBorder(app)
        drawScore(app)
    else:
        drawRestart(app)

def drawScore(app):
    message = f'{app.points} points'
    drawLabel(message, 60, 30)

def drawRestart(app):
    drawLabel('GAME OVER!', app.width/2, app.height/2, size = 40)
    drawLabel(f'You have {app.points} points', app.width/2, app.height/2 + 50, size = 16)
    drawLabel("Press 'r' to restart", app.width/2, app.height/2 + 70, size = 16)

def drawPiece(app):
    rows = len(app.piece)
    cols = len(app.piece[0])
    for row in range (rows):
        for col in range (cols):
            if not app.piece[row][col] == False:
                drawCell(app, app.pieceTopRow+row, app.pieceLeftCol+col, app.pieceColor)

def drawBoard(app):
    for row in range(app.rows):
        for col in range(app.cols):
            color = app.board[row][col]
            drawCell(app, row, col, color)

def drawBoardBorder(app):
  # draw the board outline (with double-thickness):
  drawRect(app.boardLeft, app.boardTop, app.boardWidth, app.boardHeight,
           fill=None, border='black',
           borderWidth=2*app.cellBorderWidth)

def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = getCellSize(app)
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,
             fill=color, border='black',
             borderWidth=app.cellBorderWidth)

def getCell(app, x, y):
    dx = x - app.boardLeft
    dy = y - app.boardTop
    cellWidth, cellHeight = getCellSize(app)
    row = math.floor(dy / cellHeight)
    col = math.floor(dx / cellWidth)
    if (0 <= row < app.rows) and (0 <= col < app.cols):
      return (row, col)
    else:
      return None

def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = getCellSize(app)
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

def getCellSize(app):
    cellWidth = app.boardWidth / app.cols
    cellHeight = app.boardHeight / app.rows
    return (cellWidth, cellHeight)

#draw ends
########################
#INPUT starts
########################

def onMouseMove(app, mouseX, mouseY):
    selectedCell = getCell(app, mouseX, mouseY)
    if selectedCell != None:
        row, col = selectedCell
        if (0 <= col <= app.cols) and (0 <= row <= app.rows):
            app.selection = selectedCell

def onKeyPress(app, key):
    if key.isdigit() and (0 <= int(key) <= 6):
        pieceIndex = int(key)
        loadPiece(app, pieceIndex)
    elif key == 'left':
        movePiece(app, 0, -1)
    elif key == 'right':
        movePiece(app, 0, +1)
    elif key == 'down':
        movePiece(app, +1, 0)
    elif key == 'space':
        hardDropPiece(app)
    elif key == 'up':
        rotatePieceClockwise(app)
    elif key == 's': 
        takeStep(app)
    # elif key in ['a','b','c','d','e','f','g','h']:
    #     loadTestBoard(app, key)
    elif key == 'p':
        app.paused = not app.paused
    elif key == 'r':
        reset(app)

########################
#STEP starts
########################

def onStep(app):
    app.count += 1
    if app.count % 10 == 0:
        if not app.paused:
            takeStep(app)

def takeStep(app):
    if not movePiece(app, +1, 0):
        # We could not move the piece, so place it on the board:
        placePieceOnBoard(app)
        removeFullRows(app)
        loadNextPiece(app)

def removeFullRows(app):
    i = 0
    rowsPoped = 0
    while i < app.rows:
        if checkRowIsFull(app.board[i]):
            app.board.pop(i)
            app.board.insert(0, [None] * app.cols)
            rowsPoped += 1
        else:
            i += 1
    if not rowsPoped == 0:
        app.points += (10*rowsPoped + 2**rowsPoped)

def checkRowIsFull(row):
    for value in row:
        if value == None:
            return False
    return True

def resizeBoard(app, numRows, numCols, boardSize):
    app.rows = numRows
    app.cols = numCols
    app.boardLeft, app.boardWidth, app.boardHeight = boardSize
    app.board = [([None] * app.cols) for row in range(app.rows)]

def main():
    runApp()

main()