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
		self.lengthIncrease = 4
		self.length = 0

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
		return self.move()

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
		ate = False
		if tile is not None:
			self.snake = np.vstack([self.snake, tile])
		# eat increases length by one
		if np.array_equal(tile, self.board.dot.dot):
			ate = True
			self.length+=self.lengthIncrease
		if self.length == 0:
			self.snake = self.snake[1:, :]
		else:
			self.length-=1
		return ate

class Dot():
	def __init__(self, board):
		self.board =board
		self.reset()

	def reset(self):
		choices  = self.board.getEmptyCells()
		self.dot = choices[np.random.choice(choices.shape[0], 1, replace=False), :][0]

class Board():
	# 1 is snakeHead
	# 2 is snake
	# 3 is food
	def __init__(self, size=20):
		self.width = 10
		self.margin = 1
		self.size = size
		self.WINDOW_SIZE = [self.size*(self.width+self.margin), self.size*(self.width+self.margin)]
		self.screen = None
		self.reset()

	def getEmptyCells(self, ignoreSnake=False):
		return np.argwhere(self.board==0) if ignoreSnake else np.array([x for x in np.argwhere(self.board==0).tolist() if x not in self.snake.snake.tolist()])

	def getState(self):
		state = self.board
		snake = np.transpose(self.snake.snake)
		state[snake[0], snake[1]]=2
		state[self.snake.snake[-1][0], self.snake.snake[-1][1]]=1
		state[self.dot.dot[0]. self.dot.dot[1]] = 3
		state = state.flatten()
		return state

	def step(self, direction):
		ate = self.snake.step(direction)
		if ate:
			self.dot.reset()
		self.render()
		return ate

	def render(self):
		if self.screen == None:
			self.screen = pygame.display.set_mode(self.WINDOW_SIZE)
		self.screen.fill(BLACK)
		for row in range(self.size):
		    for column in range(self.size):
		        color = WHITE
		        if np.array_equal(np.array([row, column]), self.dot.dot):
		            color = GREEN
		        if (self.snake.snake == np.array([row, column])).all(1).any():
		        	color = RED
		        pygame.draw.rect(self.screen,
		                         color,
		                         [(self.margin + self.width) * column + self.margin,
		                          (self.margin + self.width) * row + self.margin,
		                          self.width,
		                          self.width])
		pygame.time.delay(50)
		pygame.display.flip()

	def reset(self):
		self.board = np.zeros(shape=(self.size, self.size), dtype=np.int32)
		self.snake = Snake(self)
		self.dot = Dot(self)


if __name__ == '__main__':
	pygame.init()
	b = Board()
	for x in range(16):
		b.step(0)
	b.step(3)
	for x in range(19):
		b.step(1)
	b.step(3)
	for x in range(19):
		b.step(0)
	b.step(3)
	for x in range(19):
		b.step(1)
	b.step(3)
	for x in range(19):
		b.step(0)
	b.step(3)
	for x in range(19):
		b.step(1)
	b.step(3)
	b.render()
	for x in range(19):
		b.step(0)
	b.step(3)
	b.render()
	for x in range(19):
		b.step(1)
	b.step(3)
	pygame.quit()