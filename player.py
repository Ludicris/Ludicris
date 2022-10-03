from board import Direction, Rotation, Action
from random import Random


class Player:
    def choose_action(self, board):
        raise NotImplementedError


class SeunPlayer(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)
        self.weight_height = 0.5
        self.weight_bumpiness = 0.5
        self.weight_cleared_lines = 2
        self.weight_holes = -0.4

    def get_fitness(self,board):
        score = 0
        score += self.weight_height * (sum(self.getHeights(board))**2)
        return score

    def getHeights(self,board):
        heights = []
        for i in board.cells:
            x = board.cells
        if len(board.cells) != 0:
            count = 0
            while count < 10:
                x = []
                for (a,y) in board.cells:
                    if a == count:
                        x.append(y)
                if len(x) == 0:
                    x.append(24)

                x.sort()
                heights.append(x[0])
                count += 1
        return heights

    def clearedLines(self,board,diff):
        cleared = 0
        if diff == 4 or diff == 8:
            return cleared
        elif diff == 6:
            cleared = 1
            return cleared
        else:
            cleared = diff % 10
            return cleared


    def countBlock(self,board):
        count = 0
        for y in range(board.height):
            for x in range(board.width):
                if (x,y) in board.cells:
                    count += 1
        return count

    def score_position(self,board):
        miny = 24
        for (x,y) in board.cells:
            if y < miny:
                miny = y
        return miny

    def print_board(self,board):
        #Prints out the board in ASCII (debugging)
        print("--------------------")
        for y in range(board.height):
            s = ""
            for x in range(board.width):
                if board.falling is not None and (x,y) in board.falling.cells:
                    s = s + "*"
                elif (x,y) in board.cells:
                    s = s + "#"
                else:
                    s = s + "."
            print(s,y)

    #def getClearedLines(self,board,diff):


    def choose_action(self, board):
        if board.falling is not None:
            movements = self.moves(board)
            if len(movements) != 0:
                return movements

    def moves(self,board):
        count = 0
        xpos = board.falling.left
        bestx = 0
        bestscore = 0
        bestmoves = []

        #Loops for every rotation (checks every rotation)
        while count < 4:
            #Loops for every x position (checks for every x position)
            for x in range(0,10):
                height1 = self.countBlock(board)
                sandbox = board.clone()
                xpos = sandbox.falling.left
                moves = []
                landed = False
                for i in range(0,count):
                    if sandbox.falling is None:
                        break
                    else:
                        sandbox.rotate(Rotation.Anticlockwise)
                        moves.append(Rotation.Anticlockwise)
                if sandbox.falling is not None:
                    #Moves the block left if the xpos is greater the x position it needs to land at
                    while xpos > x:
                        sandbox.move(Direction.Left)
                        moves.append(Direction.Left)
                        if sandbox.falling is not None:
                            xpos = sandbox.falling.left
                        else:
                            landed = True
                            break
                if sandbox.falling is not None:
                    # Moves the block right if the xpos is less the x position it needs to land at
                    while xpos < x and landed is False:
                        sandbox.move(Direction.Right)
                        moves.append(Direction.Right)
                        if sandbox.falling is not None:
                            xpos = sandbox.falling.left
                        else:
                            landed = True
                            break
                if sandbox.falling is not None:
                    #Drops the block
                    if landed is False:
                        sandbox.move(Direction.Drop)
                        moves.append(Direction.Drop)
                height2 = self.countBlock(sandbox)
                self.print_board(sandbox)
                print("The difference is", abs(height1-height2))
                score = self.get_fitness(sandbox)
                print(count,x)
                if sandbox.falling is not None:
                    #Compares all the scores and returns the moves corresponding to the best score
                    if score > bestscore:
                        bestscore = score
                        bestx = x
                        bestmoves = moves
            count += 1
        return bestmoves




SelectedPlayer = SeunPlayer
