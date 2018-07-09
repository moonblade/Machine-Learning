import gym
import neat
import pickle
import numpy as np
from game import Game
env = Game()
def run(episodes, net):
	observation = env.reset()
	step=0
	while True:
		step+=1
		env.render()
		action = np.argmax(net.activate(observation))
		observation, reward, done = env.step(action)
		print(action, reward)
		if done:
			break
	print(step)
	env.close()

if __name__ == '__main__':
	net = pickle.load(open('winner', 'rb'))
	run(10, net)