import pygame 
import sys
from sudoku_solver import *
import time

FPS = 60
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 640

board = [
    [0,0,0,0,0,1,0,0,3],
    [0,0,6,2,8,5,0,0,7],
    [4,0,2,3,0,0,0,0,0],
    [5,7,0,0,0,6,3,0,0],
    [0,8,0,0,7,0,0,2,0],
    [0,0,9,1,0,0,0,6,8],
    [0,0,0,0,0,9,5,0,2],
    [3,0,0,5,4,8,9,0,0],
    [9,0,0,6,0,0,0,0,4],
]

board1 = [
    [0,0,0,0,0,1,0,0,3],
    [0,0,6,2,8,5,0,0,7],
    [4,0,2,3,0,0,0,0,0],
    [5,7,0,0,0,6,3,0,0],
    [0,8,0,0,7,0,0,2,0],
    [0,0,9,1,0,0,0,6,8],
    [0,0,0,0,0,9,5,0,2],
    [3,0,0,5,4,8,9,0,0],
    [9,0,0,6,0,0,0,0,4],
]

board2 = [
    [0,0,0,0,0,1,0,0,3],
    [0,0,6,2,8,5,0,0,7],
    [4,0,2,3,0,0,0,0,0],
    [5,7,0,0,0,6,3,0,0],
    [0,8,0,0,7,0,0,2,0],
    [0,0,9,1,0,0,0,6,8],
    [0,0,0,0,0,9,5,0,2],
    [3,0,0,5,4,8,9,0,0],
    [9,0,0,6,0,0,0,0,4],
]

class GUI:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.start_time = time.time()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
        pygame.display.set_caption('Sudoku')
        self.game_over = False
        self.grid = (10,50)
        self.cell_size = 580/9
        self.cell = 0
        self.grid_size = self.cell_size*9
        self.selected = None
        self.number = 0
        self.mouse_position = None
        self.sudoku_board = board1
        self.initial_board = board2
        self.solved_board = board
        self.sudoku_solved = False
        self.font = pygame.font.SysFont('Arial',(SCREEN_WIDTH//9)//2)    
        self.font_small = pygame.font.SysFont('Arial',(SCREEN_WIDTH//9)//4)    
        self.locked_cells = []
        self.locked_flag = False
        self.all_cell_filled = set()
        self.is_locked()
        self.result = PrintOnConsole(board)
        self.solver = Solver(board)
        self.solver.solve(board)
        self.end = None

    def run(self):
        while not self.game_over:
            self.get_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit

    def get_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE:
                    self.game_over = True
                if event.key == pygame.K_SPACE:
                    self.sudoku_board = self.initial_board
                    self.solve_board()
                if self.selected:
                    if self.isInt(event.unicode):
                        self.number = self.sudoku_board[self.selected[0]][self.selected[1]] = int(event.unicode)
                        self.all_cell_filled.add((self.selected[0],self.selected[1]))
            if event.type == pygame.MOUSEBUTTONDOWN:
                selected = self.mouse_on_grid()
                if selected not in self.locked_cells:
                    self.selected = selected
                else:
                    self.selected = None
                
    def update(self):
        self.mouse_position = pygame.mouse.get_pos()
        if len(self.all_cell_filled) == 81:
            self.end = self.is_correct(self.solved_board,self.sudoku_board)
            
    def draw(self):
        self.screen.fill((255,255,255))
        if self.selected:
            self.draw_box(self.selected)
        self.draw_grid()
        self.draw_numbers()
        self.number = 0
        self.current_time = round(time.time() - self.start_time)
        text = self.font.render("Time: " + self.timer(self.current_time), 1, (0,0,0))
        self.screen.blit(text, (280 + (SCREEN_WIDTH / 4),10))
        if self.end == True:
            self.draw_endscreen('Win')
        if self.sudoku_solved == True:
            self.draw_endscreen()
        pygame.display.update()

    def draw_grid(self):
        pygame.draw.rect(self.screen,(0,0,0),(10,50,SCREEN_WIDTH-20,SCREEN_HEIGHT-60),5)
        for i in range(9):
            if i % 3 == 0 and i != 0:
                pygame.draw.line(self.screen,(0,0,0),(self.grid[0] + (i*self.cell_size),self.grid[1]),(self.grid[0] + (i*self.cell_size),self.grid[1] + SCREEN_HEIGHT-60),4)
                pygame.draw.line(self.screen,(0,0,0),(self.grid[0],self.grid[1] + (i*self.cell_size)),(self.grid[0] + SCREEN_HEIGHT-60,self.grid[1] + (i*self.cell_size)),4)
            else:
                pygame.draw.line(self.screen,(0,0,0),(self.grid[0] + (i*self.cell_size),self.grid[1]),(self.grid[0] + (i*self.cell_size),self.grid[1] + SCREEN_HEIGHT-60),2)
                pygame.draw.line(self.screen,(0,0,0),(self.grid[0],self.grid[1] + (i*self.cell_size)),(self.grid[0] + SCREEN_HEIGHT-60,self.grid[1] + (i*self.cell_size)),2)
        
    def draw_box(self,position):
        pygame.draw.rect(self.screen,((72,255,72)),(self.grid[0] + (position[0]*self.cell_size+1),self.grid[1] + (position[1]*self.cell_size+1),self.cell_size,self.cell_size))

    def draw_numbers(self):
        for row in range(9):
            for col in range(9):
                if self.sudoku_board[row][col] != 0:
                    position = [self.grid[0] + (row*self.cell_size),self.grid[1] + (col*self.cell_size)]
                    self.text_on_screen(str(self.sudoku_board[row][col]),position)

    def draw_endscreen(self,end='Default'):
        if end == 'Win': 
            fnt = pygame.font.SysFont('Arial',(SCREEN_WIDTH//14))    
            font = fnt.render('You Won',False,(0,0,0))
            pygame.draw.circle(self.screen,(0,255,0),(SCREEN_WIDTH//2,SCREEN_HEIGHT//2),150)
        else:
            fnt = pygame.font.SysFont('Arial',(SCREEN_WIDTH//18))    
            font = fnt.render('Sudoku Solved',False,(255,255,255))
            pygame.draw.circle(self.screen,(255,140,0),(SCREEN_WIDTH//2,SCREEN_HEIGHT//2),150)
        self.screen.blit(font,(SCREEN_WIDTH//2 - 100,SCREEN_HEIGHT//2 - 25))

    def mouse_on_grid(self):
        if self.mouse_position[0] < self.grid[0] or self.mouse_position[1] < self.grid[1]:
            return False
        if self.mouse_position[0] > self.grid[0]+self.grid_size or self.mouse_position[1] > self.grid[1]+self.grid_size:
            return False
        return (int((self.mouse_position[0]-self.grid[0])//self.cell_size), int((self.mouse_position[1]-self.grid[1])//self.cell_size))

    def text_on_screen(self,text,position):
        font = self.font.render(text,False,(0,0,0))
        font_width = font.get_width()
        font_height = font.get_height()    
        position[0] += (self.cell_size - font_width) // 2
        position[1] += (self.cell_size - font_height) // 2
        self.screen.blit(font,position)    

    def is_locked(self):
        for row in range(len(self.sudoku_board[0])):
            for col in range(len(self.sudoku_board[0])):
                if self.sudoku_board[row][col] != 0:
                    self.locked_cells.append((row,col)) 
                    self.all_cell_filled.add((row,col))

    def isInt(self,string):
        try:
            if int(string) == 0:
                return False
            return True
        except:
            return False

    def is_correct(self,board,user_board):
            for i in range(9):
                for j in range(9):
                    if board[i][j] != user_board[i][j]:
                        return False
            return True

    def solve_board(self):
        find = self.solver.is_empty(self.sudoku_board) 
        if not find:
            return True
        row,col = find      
        for i in range(1,10):
            if self.solver.is_valid(self.sudoku_board,i,(row,col)):
                self.sudoku_board[row][col] = i
                self.set((row,col),i)
                self.draw_change(1,(row,col),i,True)
                pygame.display.update()
                pygame.time.delay(100)
                if self.solve_board():
                    return True
                self.sudoku_board[row][col] = 0
                self.set((row,col),0)
                self.draw_change(0,(row,col),i,False)
                pygame.display.update()
                pygame.time.delay(100)
        self.sudoku_solved = True
        
        return False

    def set(self,position,val):
        self.sudoku_board[position[0]][position[1]] = val

    def draw_change(self,val,position,num,g=True):
        text = self.font.render(str(num), 1, (0, 0, 0))
        text_width = text.get_width()
        text_height = text.get_height()

        location = [self.grid[0] + (position[0]*self.cell_size),self.grid[1] + (position[1]*self.cell_size)]
        location[0] += (self.cell_size - text_width) // 2
        location[1] += (self.cell_size - text_height) // 2

        pygame.draw.rect(self.screen,(255,255,255),(self.grid[0] + (position[0]*self.cell_size+1),self.grid[1] + (position[1]*self.cell_size+1),self.cell_size,self.cell_size),0)
        self.screen.blit(text,location)  
        if g:
            pygame.draw.rect(self.screen,((0,255,0)),(self.grid[0] + (position[0]*self.cell_size+1),self.grid[1] + (position[1]*self.cell_size+1),self.cell_size,self.cell_size),3)
        else:
            pygame.draw.rect(self.screen,((255,0,0)),(self.grid[0] + (position[0]*self.cell_size+1),self.grid[1] + (position[1]*self.cell_size+1),self.cell_size,self.cell_size),3)

    def timer(self,time):
        sec = time % 60
        minute = time // 60
        hour = minute // 60
        if sec < 10:
            return (" " + str(minute) + ":" + str(0)+str(sec))
        else:
            return (" " + str(minute) + ":" + str(sec))
