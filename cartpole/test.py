import gym
import pickle
import neat
import numpy as np

env = gym.make('CartPole-v0')
def run(episodes, net):
	observation = env.reset()
	step=0
	while True:
		step+=1
		env.render()
		action = np.argmax(net.activate(observation))
		observation, reward, done, info = env.step(action)
		if done:
			break
	print(step)
	env.close()

if __name__ == '__main__':
	net = pickle.load(open('winner', 'rb'))
	run(10, net)