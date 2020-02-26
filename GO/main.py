# Plotting, printing output, calling other function

import networkx as nx
from itertools import product
import graphic, pm
import numpy as np
import matplotlib.pyplot as plt
import random


size = pm.size

G = nx.grid_graph([size,size])

#c = G.subgraph([(0,0),(0,1),(1,1),(2,1),(3,2),(3,3),(4,3)])
#cc = nx.node_connected_component(c,(0,0))
#print()

#board = {1: [(4,0),(4,1),(4,2),(1,4),(0,4),(2,4)], 2: [(0,0),(0,1),(1,1),(2,1),(3,2),(3,3),(4,3)]}


def plot(board,turn):
	state = np.zeros((size,size))
	for i,j in board[1]:
		state[i][j] = 1
	for i,j in board[2]:
		state[i][j] = 2
	img = graphic.go(state, turn, points) # or you can pass points if you want to display area too

	# Display board state
	plt.close()
	plt.imshow(img)
	plt.show(block=False)


# capture pieces that that now covered due to move played at pos
def capture(player, boardTemp, pos):
	pieces = 0

	#  no need to check
	# check if empty spaces nearby have been covered due to this move
	changed = list(G.neighbors(pos))+[pos] # The only positions that can be effected
	for n in changed:
		# consider the subgraph formed by pieces placed by enemy, what is the connected
		# component of node n in this subgraph
		enemy = 1 if player == 2 else 2
		
		sub = G.subgraph(boardTemp[enemy])
		if(n in sub):
			cc = nx.node_connected_component(sub,n)
			print("===")
			print("The connected components of "+str(n)+" in the following enemy subgraph is")
			print(sub)
			print(cc)
			boundary = nx.node_boundary(G,cc) # get all the liberties of this CC of your enemy
			print("the boundary for this cc is")

			# check if you cover this cc
			if(boundary.issubset(set(boardTemp[player]))):
				print("The cc has been captured by you!!")
				boardTemp[enemy] =  [e for e in boardTemp[enemy] if e not in cc] # capture the pieces
				points[player] += len(cc) # update points
				piecesCaptured[player] += len(cc)
				boardTemp[0] += list(cc) # update that new positions have been emptied up
				pieces += len(list(cc))
			

		# Optional Rule 7A NOT IN EFFECT - (Self-capture) is allowed
		sub = G.subgraph(boardTemp[player])
		if(n in sub):
			cc = nx.node_connected_component(sub,n)
			print("===")
			print("The connected components of "+str(n)+" in the player subgraph is")
			print(sub)
			print(cc)
			boundary = nx.node_boundary(G,cc) # get all the liberties of this CC
			print("the boundary for this cc is")

			if(boundary.issubset(set(boardTemp[enemy]))):
				print("Your cc has been captured by SELF CAPTURE!!")
				boardTemp[player] =  [e for e in boardTemp[player] if e not in cc] # capture the pieces
				points[enemy] += len(cc) # update points
				piecesCaptured[enemy] += len(cc)
				boardTemp[0] += list(cc) # update that new positions have been emptied up
				pieces -= len(list(cc))

	return pieces

def updatePoints(player, boardTemp, pos):
	# check if empty spaces nearby have been covered due to this move
	changed = list(G.neighbors(pos))+[pos]
	enemy = 1 if player == 2 else 2

	reward = 0

	# if you fill in your already captured SINGLE point area
	for oldArea in captured_area[player]:
		if((oldArea == set([pos]))):
			captured_area[player].remove(oldArea)
			points[player] -= len(oldArea)
			reward -= len(oldArea)

	# if you capture an enemy by filling in the single point they used to hold
	for oldArea in captured_area[enemy]:
		if((oldArea == set([pos]))):
			captured_area[enemy].remove(oldArea)
			# no need to update reward since the blank area thus formed will have player as boundary
			points[enemy] -= len(oldArea)

	for n in changed:
		sub = G.subgraph(boardTemp[0])
		if(n in sub):
			cc = nx.node_connected_component(sub,n)
			print("===")
			print("The connected components of "+str(n)+" in the subgraph of empty spaces is")
			print(sub)
			print(cc)
			boundary = nx.node_boundary(G,cc)
			if(boundary.issubset(set(boardTemp[enemy]))):
				not_tabulated = True
				print("This cc is covered by player "+str(enemy))
				for oldArea in captured_area[enemy]:
					if(cc.issubset(oldArea)):
						# old territory can shrink, should run only once for a single oldArea
						captured_area[enemy].remove(oldArea)
						points[enemy] -= len(oldArea)
						reward += len(oldArea)
						
						captured_area[enemy].append(cc)
						points[enemy] += len(cc)
						reward -= len(cc)

						not_tabulated = False
						print("cc is a subset of Old area ->")
						print(oldArea)

				if(not_tabulated):
					captured_area[enemy].append(cc)
					points[enemy] += len(cc)
					reward -= len(cc) # since enemy gained
					print("fresh entry into captured_area")

			elif(boundary.issubset(set(boardTemp[player]))):
				not_tabulated = True
				print("This cc is covered by player "+str(player))

				for oldArea in captured_area[player]:
					if(cc.issubset(oldArea)):
						# old territory can shrink,
						captured_area[player].remove(oldArea)
						points[player] -= len(oldArea)
						reward -= len(oldArea)

						captured_area[player].append(cc)
						points[player] += len(cc)
						reward += len(cc)

						not_tabulated = False
						print("cc is a subset of Old area ->")
						print(oldArea)

				if(not_tabulated):
					captured_area[player].append(cc)
					points[player] += len(cc)
					reward += len(cc)
					print("fresh entry into captured_area")
			else:
				# if this connected commponent is now under contention
				# we need to remove it from captured_area if it used to exist.
				for oldArea in captured_area[player]:
					if(cc.issubset(oldArea)):
						# old territory can shrink!! no new owner
						captured_area[player].remove(oldArea)
						points[player] -= len(oldArea)
						reward -= len(oldArea)

				for oldArea in captured_area[enemy]:
					if(cc.issubset(oldArea)):
						# old territory can shrink!! no new owner
						captured_area[enemy].remove(oldArea)
						points[enemy] -= len(oldArea)
						reward += len(oldArea)

	print("\n\nPlayer "+str(player)+" played at position "+str(pos)+" and got a reward of ")
	return reward

	# One more case is if the single blank spot is now taken over by a colored piece
	# no longer blank so, no subgraph formed.
	for oldArea in captured_area[player]:
		if(oldArea == set([pos])):
			captured_area[player].remove(oldArea)
			points[player] -= len(oldArea)
	for oldArea in captured_area[enemy]:
		if(oldArea == set([pos])):
			captured_area[enemy].remove(oldArea)
			points[enemy] -= len(oldArea)

# player can be 1 or 2, white or black, pos is a tuple of (i,j)
def play(player, pos):
	global board,turn # ensure these variables is treated as a global variable
	print("\n\nTurn Number "+ str(turn) +" player "+str(player)+" is trying to play at position "+str(pos))
	print(points)
	
	# check if position is free of any other piece
	if(pos in board[0]):
		boardTemp = board # making copy might take time? needed for Rule 8
		boardTemp[0].remove(pos)
		boardTemp[player].append(pos)
		rewardPieces = capture(player, boardTemp, pos)
		rewardArea = updatePoints(player, boardTemp, pos)
		print(str(rewardArea+rewardPieces))

		# Rule 8 Prohibition of repetition TO DO
		hist.append(boardTemp)
		board = boardTemp
		plot(board,turn)
		print("\n\nThe following is the captured area currently")
		print(captured_area)
		turn += 1
		return True
	print("You can only play on empty positions")
	return False


board = {1:[], 2:[]}
points = {1:0, 2:0} # pieces captured + total area under control right now 
piecesCaptured = {1:0, 2:0}

# list of sets of nodes currently under control of respective player
captured_area = { 1:[], 2:[]}

turn = 1
hist = [] # history of board positions

'''
total = list(set(list(product(range(size), repeat = 2))))

board[1] = random.sample(total,size*size//3)
board[2] = random.sample(list(set(total) - set(board[1])),size*size//3)
# initially all positions belong to blank - set(board[1]) - set(board[2]))
board[0] = list(set(total) - set(board[1]) - set(board[2]))
'''
board[0] = list(set(list(product(range(size), repeat = 2))))

move = 'y'
player = 2
	
while(move!='q'):
	move = input()
	if(not(play(player%2+1, tuple(map(int,move.split(' ')))))):
		continue # invalid move same player tries again
	player += 1 
	print("\n\n")
	print(points)
	print("=======")



''' RANDOM GAME
gameNumber = 1

for i in range(100000):
	text_file = open(pm.myHomeFolder + "\\data\\gameNumber"+str(gameNumber)+".txt", "w")
	player = 1
	gameNumber += 1
	turn = 1
	board = {1:[], 2:[]}
	points = {1:0, 2:0}
	turn = 0 
	hist = [] # history of board positions

	# initially all positions belong to blank - set(board[1]) - set(board[2]))
	board[0] = list(set(list(product(range(size), repeat = 2))))
	
	while(turn<size**2):
		randMove = board[0][np.random.randint(len(board[0]))]
		if(not(play(player, randMove))):
			continue
		player = 3 - player 
		state = np.zeros((size,size))
		for i,j in board[1]:
			state[i][j] = 1
		for i,j in board[2]:
			state[i][j] = 2

		string = ''
		for i in state.astype(int).flatten():
			string += str(i)
		string += '\n'
		text_file.write(string)
	
	print("Done writing the data of game number "+str(gameNumber) + " to disk! \n")
	print(points)

	text_file.close()
'''