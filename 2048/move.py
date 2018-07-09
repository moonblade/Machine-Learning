from enum import Enum
class Move(Enum):
	UP = 0
	DOWN = 1
	LEFT = 2
	RIGHT = 3
	# RESTART = 4
	# UNDO = 5

if __name__ == '__main__':
	print(list(Move))