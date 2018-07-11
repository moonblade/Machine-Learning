import numpy as np
import pygame
import time
import neat
import pickle
import visualize

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

maxStep = 10000
perNet = 5
def eval_genome(genome, config):
	net = neat.nn.FeedForwardNetwork.create(genome, config)
	fitnesses = []
	for x in range(perNet):
		observation = env.reset()
		step = 0
		totReward = 0
		while True and step<maxStep:
			env.render()
			step+=1
			action = np.argmax(net.activate(observation))
			observation, reward, done = env.step(action)
			totReward += reward
			if done:
				break
		fitnesses.append(totReward+step*0.001)
	return min(fitnesses)

def eval_genomes(genomes, config):
	for genome_id, genome in genomes:
		genome.fitness = eval_genome(genome, config)

def run(path):
	config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, path)
	# p = neat.Population(config)
	p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-124')

	p.add_reporter(neat.StdOutReporter(True))
	stat = neat.StatisticsReporter()
	p.add_reporter(stat)
	p.add_reporter(neat.Checkpointer(50))

	pe = neat.ParallelEvaluator(20, eval_genome)
	# winner = p.run(pe.evaluate)
	winner = p.run(eval_genomes, 300)

	print('\nBest genome:\n{!s}'.format(winner))
	winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
	pickle.dump(winner_net, open('winner.net', 'wb'))

	# node_names = {0:'action'}
	# visualize.draw_net(config, winner, True)
	# visualize.plot_stats(stat, ylog=False, view=True)
	# visualize.plot_species(stat, view=True)


class Snake():
	# 0 right, 1 left, 2 up, 3 down
	def __init__(self, board):
		self.board = board
		self.startLength = 2
		self.reset()
		self.lengthIncrease = 1
		self.length = 0

	def reset(self):
		self.direction = 0
		choices = self.board.getEmptyCells(True)
		self.snake=choices[:self.startLength]
		self.dead = False

	def changeDirection(self, direction):
		if self.direction + direction == 1 or self.direction + direction==5 or self.dead:
			return
		self.direction = direction
		
	def step(self, direction):
		if not self.dead:
			self.changeDirection(direction)
			return self.move()
		else:
			return False, self.dead

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
		if nextTile[0]>=self.board.size or nextTile[0]<0 or nextTile[1]>=self.board.size or nextTile[1]<0:
			self.dead = True
			return None
		if nextTile in self.snake.tolist():
			self.dead = True
			return None
		return nextTile

	def move(self):
		tile = self.getNextTile()
		if self.dead:
			return False, self.dead
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
		return ate, self.dead

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
	def __init__(self, size=5):
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
		state[self.dot.dot[0], self.dot.dot[1]] = 3
		state = state.flatten().tolist() + [self.snake.direction]
		return state

	def step(self, direction):
		ate, dead = self.snake.step(direction)
		if ate:
			self.dot.reset()
			reward = 1
		else:
			reward = 0
		# self.render()
		return self.getState(), reward, dead

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
		        if (self.snake.snake[-1, :] == np.array([row, column])).all():
		        	color = BLUE
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
		return self.getState()


if __name__ == '__main__':
	pygame.init()
	env = Board()
	run('config')
	pygame.quit()