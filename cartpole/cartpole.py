import gym
import neat
import visualize
import os
import numpy as np
import pickle 

maxFit = 195
perNet = 5            
env = gym.make('CartPole-v0')
def eval_genome(genome, config, render=False):
	net = neat.nn.FeedForwardNetwork.create(genome, config)
	fitnesses = []
	for x in range(perNet):
		observation = env.reset()
		step = 0
		while step < maxFit:
			if (render):
				env.render()
			step+=1
			action = np.argmax(net.activate(observation))
			observation, reward, done, info = env.step(action)
			if done:
				break
		fitnesses.append(step)
	return min(fitnesses)

def eval_genomes(genomes, config, render=False):
	for genome_id, genome in genomes:
		genome.fitness = eval_genome(genome, config, render)

def run(path):
	config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, path)
	p = neat.Population(config)

	p.add_reporter(neat.StdOutReporter(True))
	stat = neat.StatisticsReporter()
	p.add_reporter(stat)
	p.add_reporter(neat.Checkpointer(5))

	pe = neat.ParallelEvaluator(4, eval_genomes)
	winner = p.run(eval_genomes, 300)

	print('\nBest genome:\n{!s}'.format(winner))
	winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
	pickle.dump(winner_net, open('winner', 'wb'))

	# node_names = {-1:'A', -2: 'B', -3: 'C', -4: 'D', 0:'action'}
	# visualize.draw_net(config, winner, True, node_names=node_names)
	# visualize.plot_stats(stat, ylog=False, view=True)
	# visualize.plot_species(stat, view=True)


def main():
	local_dir = os.path.dirname(__file__)
	config_path = os.path.join(local_dir, 'config')
	run(config_path)

if __name__ == '__main__':
	main()