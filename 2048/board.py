#!/usr/bin/env python3
import random
import numpy as np
from move import Move
from partialFormatter import fmt
from itertools import count, groupby, starmap
# import numpy

class Board():
	# size - size of side of square board
	# board - dictionary of cell -> value pairs
	# fourProbability - probability of a 4 showing up instead of 2
	def __init__(self, size=4, fourProbability=0.1):
		self.base = 2
		self.size = size
		self.board = [[None for x in range(self.size)] for y in range(self.size)]
		self.previousBoard = self.board[:]
		self.fourProbability=fourProbability
		self.addRandomData()
		self.addRandomData()

	def getEmptyCells(self):
		return [(x,y) for x in range(self.size) for y in range(self.size) if self.board[x][y] == None]

	def getEmptyCell(self):
		if (len(self.getEmptyCells())==0):
			return None
		return random.choice(self.getEmptyCells())

	def getState(self):
		return np.array([self.board[x][y]  if self.board[x][y] is not None else 0 for x in range(self.size) for y in range(self.size)])		

	def changeData(self, cell, number):
		if cell is None:
			return False
		else:
			self.board[cell[0]][cell[1]] = number
			return True

	# return base or base * 2 based on probability
	def getRandomData(self):
		chance = random.uniform(0, 1)
		if(chance <= self.fourProbability):
			return self.base * 2;
		else:
			return self.base;

	def undo(self):
		self.board = self.previousBoard[:]
		return (0, True)

	def noMoreMoves(self):
		rows = self.board + [[self.board[y][x] for y in range(self.size)] for x in range(self.size)]
		return self.getEmptyCell() is None and not any([rows[x][y]==rows[x][y+1] for x in range(self.size * 2) for y in range(self.size - 1)])

	def validMove(self):
		return self.board != self.previousBoard

	def addRandomData(self):
		self.changeData(self.getEmptyCell(), self.getRandomData())

	def print(self):
		for x in range(self.size):
			print(''.join([fmt.format('{0:<10}', self.board[x][y]) for y in range(self.size)]))
		print()

	def flip(self):
		self.board = [self.board[x][::-1] for x in range(self.size)]

	def transpose(self):
		self.board = [[self.board[y][x] for y in range(self.size)] for x in range(self.size)]

	def move(self, move):
		if move == Move.UP:
			return self.moveUp()
		elif move == Move.DOWN:
			return self.moveDown()
		elif move == Move.RIGHT:
			return self.moveRight()
		elif move == Move.LEFT:
			return self.moveLeft()
		elif move == Move.UNDO:
			return self.undo()

	def moveDown(self):
		self.previousBoard = self.board[:]
		self.transpose()
		score = self.squishRight()
		self.transpose()
		return score, self.validMove()
		
	def moveUp(self):
		self.previousBoard = self.board[:]
		self.transpose()
		score = self.squishLeft()
		self.transpose()
		return score, self.validMove()

	def moveRight(self):
		self.previousBoard = self.board[:]
		score = self.squishRight()
		return score, self.validMove()

	def squishRight(self):
		self.flip()
		score = self.squishLeft()
		self.flip()
		return score

	def moveLeft(self):
		self.previousBoard = self.board[:]
		score = self.squishLeft()
		return score, self.validMove()

	def squishLeft(self):
		score = 0
		for rowIndex in range(self.size):
			row = self.board[rowIndex]
			r = []
			for n,x in starmap(lambda n, a: (n, sum(map(bool,a))), groupby(filter(bool, row))):
				r += ([n*self.base] * (x//self.base)) + ([n] * (x%self.base))
				score += n*self.base*(x//self.base)
			self.board[rowIndex] = r + ([None] * (self.size - len(r)))
		return score
