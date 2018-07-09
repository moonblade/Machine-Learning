from board import Board
from move import Move
import getch
class Game():
	def __init__(self):
		self.actionSpace = list(Move)
		self.nActions = len(self.actionSpace)
		self.reset()
		self.nFeatures = self.board.size * self.board.size
		self.deathScore = -100

	def step(self, move):
		move = Move(move)
		score, valid=self.board.move(move)
		if (valid):
			self.score+=score
			self.board.addRandomData()
		done = self.isGameOver()
		# print(score, move)
		return self.board.getState(), score if not done else self.deathScore, done				

	def makeMove(self, move):
		score, valid=self.board.move(move)
		if (valid):
			self.score+=score
			self.board.addRandomData()
			self.print()

	def move(self):
		char = getch.getch()
		if char == 'q':
			return True
		elif char == 'd':
			self.makeMove(Move.RIGHT)
		elif char == 'a':
			self.makeMove(Move.LEFT)
		elif char == 'w':
			self.makeMove(Move.UP)
		elif char == 's':
			self.makeMove(Move.DOWN)

	def render(self):
		self.print

	def reset(self):
		self.board = Board()
		self.score = 0
		return self.board.getState()

	def print(self):
		self.board.print()

	def isGameOver(self):
		return self.board.noMoreMoves()

if __name__ == '__main__':
	g = Game()
	g.print()
	while not g.isGameOver():
		if(g.move()):
			break
