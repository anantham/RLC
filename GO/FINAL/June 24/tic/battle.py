import model1 
import numpy as np
import nn
import main 
import models
import logging as log
import tools as tl 
import matplotlib.pyplot as plt

modelList = [15,16,17,18,19,20,57,58,59]

def randAction(state):
	rand = np.random.rand(value.shape[0])
	moves = np.reshape(np.where(state==0,1,0),-1)
	action = np.argmax(moves*rand)
	return action

log.basicConfig(level=log.WARNING)

for m1 in modelList:
	for m2 in [42,43,44]:

		model1 = models.model1()
		model2 = models.model2()

		#print("Pick weights for player 1")
		#one = input()
		#print("Pick weights for player 2")
		#two = input()

		# 15 is eps, 16 = stochastic, 17 = greedy deterministic 1k games
		# 18 is eps, 19 = stochastic, 20 = greedy deterministic 10k games

		# model2 = 42, 43, 44 

		# eps = 0.1, 0.4, 0.9 in model1 = 57,58,59

		w1 = np.load('weights'+str(m1)+'.npy', allow_pickle= True)
		model1.set_weights(w1)

		w2 = np.load('weights'+str(m2)+'.npy', allow_pickle= True)
		model2.set_weights(w2)

		state = np.zeros((5,5))
		player = 1
		value = model1.forward(state)

		action = np.argmax(value)

		# Let this model1 always take random moves
		action = randAction(state)

		wins1 = 0
		wins2 = 0

		for i in range(10**2):
			totalR1 = 0
			totalR2 = 0
			state = np.zeros((5,5))

			# 12 moves for each player
			for j in range(12):
				state, reward  = main.go(state,action,player)
				val1 = model2.forward(state)
				moves = np.reshape(np.where(state==0,1,0),-1)
				action1 = np.argmax(moves*val1)
				#print("Model chooses to play at "+str(action1))
				#print('next state {}, reward = {} \n \n '.format(state,reward))
				totalR1 += reward
				player = 3 - player

				# Let this model2 always take random moves
				#action1 = randAction(state)

				state, reward  = main.go(state,action1,player)
				val2 = model1.forward(state)
				moves = np.reshape(np.where(state==0,1,0),-1)

				
				rand = np.random.rand(value.shape[0])
				action = np.argmax(rand)

				#print("Model chooses to play at "+str(action))
				action = np.argmax(moves*val2)
				totalR2 += reward
				player = 3 - player
				#print('next state {}, reward = {} \n \n '.format(state,reward))

				# Let this model1 always take random moves
				#action = randAction(state)

			if(totalR1>totalR2):
				#print("Model 1 wins!")
				wins1 += 1
			else:
				#print("Model 2 wins!")
				wins2 += 1

		print("total wins by "+str(m1)+" is  "+ str(wins1) +"  and "+str(m2)+" is "+ str(wins2))