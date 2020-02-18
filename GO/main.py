# Plotting, printing output, calling other function

import networkx as nx
from itertools import product
import graphic, pm
import numpy as np

size = pm.size

G = nx.grid_graph([size,size])

#c = G.subgraph([(0,0),(0,1),(1,1),(2,1),(3,2),(3,3),(4,3)])
#cc = nx.node_connected_component(c,(0,0))
#print()

#board = {1: [(4,0),(4,1),(4,2),(1,4),(0,4),(2,4)], 2: [(0,0),(0,1),(1,1),(2,1),(3,2),(3,3),(4,3)]}

board = {1:[], 2:[]}
points = {1:0, 2:0}
turn = 0 
hist = [] # history of board positions

# initially all positions belong to blank - set(board[1]) - set(board[2]))
board[0] = list(set(list(product(range(size), repeat = 2))))


def plot(board,turn):
	state = np.zeros((size,size))
	for i,j in board[1]:
		state[i][j] = 1
	for i,j in board[2]:
		state[i][j] = 2
	img = graphic.go(state,turn)
		
# capture pieces that that now covered due to move played at pos
def capture(player, boardTemp, pos):
	#  no need to check
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
				boardTemp[0] += list(cc) # update that new positions have been emptied up
			

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
				boardTemp[0] += list(cc) # update that new positions have been emptied up


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
		capture(player, boardTemp, pos)
		# Rule 8 Prohibition of repetition TO DO
		turn += 1
		hist.append(board)
		board = boardTemp
		#plot(board,turn)
		return True
	print("You can only play on empty positions")
	return False

'''
move = input()
player = 1
while(move!='q'):
	if(not(play(player%2+1, tuple(map(int,move))))):
		continue # invalid move same player tries again
	player += 1 
	move = input()
	print("\n\n")

'''
gameNumber = 1

while(True):
	string = ''
	player = 1
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
		
		for i in state.astype(int).flatten():
			string += str(i)
		string += '\n'

	# write the whole string to a file
	text_file = open(pm.myHomeFolder + "\\data\\gameNumber"+str(gameNumber)+".txt", "w")
	text_file.write(string)
	print("Done writing the data of game number "+str(gameNumber) + " to disk! \n")
	text_file.close()
