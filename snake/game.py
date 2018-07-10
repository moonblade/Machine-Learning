import numpy as np
import pygame
import time

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
class Game():
	def __init__(self):
		# up down left right
		self.nActions = 4
		self.board = Board()

class Snake():
	# 0 right, 1 left, 2 up, 3 down
	def __init__(self, board):
		self.board = board
		self.reset()

	def reset(self):
		self.direction = 0
		choices = self.board.getEmptyCells(True)
		self.snake=choices[:4]
		self.dead = False

	def changeDirection(self, direction):
		if self.direction==0 and direction==1 or self.direction==1 and direction==0 or self.direction==2 and direction==3 or self.direction==3 and direction==2:
			return
		self.direction = direction
		
	def step(self, direction):
		self.changeDirection(direction)
		self.move()

	def getNextTile(self):
		head = self.snake[-1, :]
		nextTile = None
		if self.direction == 0:
			nextTile = [head[0], head[1]+1]
		if self.direction == 1:
			nextTile = [head[0], head[1]-1]
		if self.direction == 2:
			nextTile = [head[0]-1, head[1]]
		if self.direction == 3:
			nextTile = [head[0]+1, head[1]]
		if nextTile[0]>self.board.size or nextTile[0]<0 or nextTile[1]>self.board.size or nextTile[1]<0:
			self.dead = True
			return None
		return nextTile

	def move(self):
		if self.dead:
			return
		tile = self.getNextTile()
		if tile is not None:
			self.snake = np.vstack([self.snake, tile])
		# eat increases length by one
		if self.board.board[tile[0]][tile[1]] != 3:
			self.snake = self.snake[1:, :]

class Board():
	# 1 is snake
	# 2 is snakeHead
	# 3 is food
	def __init__(self, size=20):
		self.width = 10
		self.margin = 1
		self.size = size
		self.WINDOW_SIZE = [self.size*(self.width+self.margin), self.size*(self.width+self.margin)]
		self.screen = None
		self.reset()

	def getEmptyCells(self, ignoreSnake=False):
		return np.argwhere(self.board==0) if ignoreSnake else ([x for x in np.argwhere(self.board==0).tolist() if x not in self.snake.snake.tolist()])

	def getState(self):
		state[self.snake.snake.tolist()]=2
		return state

	def render(self):
		if self.screen == None:
			self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
		self.screen.fill(BLACK)
		for row in range(self.size):
		    for column in range(self.size):
		        color = WHITE
		        if self.board[row][column] == 1:
		            color = GREEN
		        if (self.snake.snake == np.array([row, column])).all(1).any():
		        	color = RED
		        pygame.draw.rect(self.screen,
		                         color,
		                         [(self.margin + self.width) * column + self.margin,
		                          (self.margin + self.width) * row + self.margin,
		                          self.width,
		                          self.width])
		pygame.display.flip()

	def reset(self):
		self.board = np.zeros(shape=(self.size, self.size), dtype=np.int32)
		self.board[0][4] = 3
		self.snake = Snake(self)


if __name__ == '__main__':
	pygame.init()
	b = Board()
	print(b.snake.snake)
	b.snake.move()
	print(b.snake.snake)
	b.snake.move()
	print(b.snake.snake)
	b.snake.changeDirection(3)
	b.snake.move()
	print(b.snake.snake)
	print(b.getState())
	# b.render()
	pygame.quit()