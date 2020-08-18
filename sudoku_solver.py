import random

sudoku_board1 = [
    [7,0,0,0,0,1,0,0,3],
    [0,0,6,2,8,5,0,0,7],
    [4,0,2,3,0,0,0,0,0],
    [5,7,0,0,0,6,3,0,0],
    [0,8,0,0,7,0,0,2,0],
    [0,0,9,1,0,0,0,6,8],
    [0,0,0,0,0,9,5,0,2],
    [3,0,0,5,4,8,9,0,0],
    [9,0,0,6,0,0,0,0,4],
]

sudoku_board2 = [
    [4,5,8,0,0,0,0,3,0],
    [0,0,0,0,0,3,0,0,4],
    [0,0,1,5,6,0,9,0,0],
    [2,0,0,0,0,0,3,0,0],
    [0,0,6,9,0,2,7,0,0],
    [0,0,3,0,0,0,0,0,6],
    [0,0,4,0,1,8,5,0,0],
    [7,0,0,6,0,0,0,0,0],
    [0,2,0,0,0,0,4,6,8],
]

sudoku_board3 = [
    [0,0,0,0,0,0,6,3,4],
    [0,0,0,1,3,5,9,0,0],
    [0,0,0,0,2,0,0,0,0],
    [0,3,0,0,0,0,0,9,0],
    [1,0,8,6,0,9,2,0,3],
    [0,7,0,0,0,0,0,5,0],
    [0,0,0,0,7,0,0,0,0],
    [0,0,5,9,4,2,0,0,0],
    [3,9,7,0,0,0,0,0,0],
]

sudoku_boards = [sudoku_board1,sudoku_board2,sudoku_board3]

class PrintOnConsole:
    def __init__(self,board):
        self.board = board
        
    def print_board(self):
        for i in range(len(self.board)):
            if i % 3 == 0 and i != 0:
                print('- - - - - - - - - - - - - - - - - -')
                print('- - - - - - - - - - - - - - - - - -')

            for j in range(len(self.board[0])):
                if j % 3 == 0 and j != 0:
                    print(' || ',end = ' ')

                if j == 8:
                    print(self.board[i][j])
                else:
                    print(str(self.board[i][j]) + ' ',end = ' ')

class Solver:
    def __init__(self,board):
        self.board = board

    def is_empty(self,board):
        # for i in range(len(self.board)):
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def is_valid(self,board,number,position):

        for i in range(9):
            if board[position[0]][i] == number:
                return False
        
        for i in range(9):
            if board[i][position[1]] == number:
                return False

        x = position[0] // 3
        y = position[1] // 3

        for i in range(x*3, x*3 + 3):
            for j in range(y*3, y*3 + 3):
                if board[i][j] == number:
                    return False
        
        return True

    def solve(self,board):
        find = self.is_empty(self.board)
        if not find:
            return True
        row, col = find
        for i in range(1,10):
            if self.is_valid(board,i,(row,col)):
                self.board[row][col] = i
                if self.solve(board):
                    return True
                self.board[row][col] = 0
        return False

if __name__ == "__main__":

    sudoku_board = random.choice(sudoku_boards)
    sudoku = PrintOnConsole(sudoku_board)
    solved = Solver(sudoku_board)

    print('Board')
    sudoku.print_board()
    solved.solve(sudoku_board)
    print('\n\n\n')
    print('Solved Board\n')
    sudoku.print_board()

