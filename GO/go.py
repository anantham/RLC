# GO Game engine functions
import pm # parameters

class state():
	def __init__():
		# 0 means pos is empty, 1 means captured by white, -1 means black
		self.P = np.zeros((pm.size,pm.size))
		# the size of the connected component that (i,j) belongs to, with 0 surrounding
		self.C = np.zeros((pm.size,pm.size))
		# L0 tells us number of liberties the CC(i,j) has
		# L1 considers white (1) to be the surroundings and this tells us how many
		# "liberties" CC's of 0 and -1 have. L2 counts black (-1) liberties.
		self.L = np.zeros((pm.size,pm.size,3))
		# This tracks the net score gained by white at that position (i,j)
		self.Z = np.zeros((pm.size,pm.size),2)
		#self.histP = np.zeros((pm.size,pm.size,2)) if we want to implement rule of KO

		# intially all zeros belong to 0 id group then all elements 
		# that form a connected component share a unique id 
		# (the move that placed the oldest piece of that group)
		self.U = np.zeros((pm.size,pm.size))

	

	# check if move played at pos by player is valid
	def validity(self, player, pos):
		if(self.P[pos[0]][pos[1]]):
			Ptemp = np.copy(self.P)
			Ptemp[pos[0]][pos[1]] = player
			Ltemp = capture(Ptemp, pos)
			if(Ltemp[0][pos[0]][pos[1]] != 0):
				return True
			else:
				return False


	def capture(self, P, pos):
		for p in nbd(pos):
			L = computeLiberty(P)
			if(L[0][p[0]][p[1]] == 0):
				P = remove(p, P)
		return computeLiberty(P)

	# returns the scalar reward that the player has accumulated till now
	def reward(self, player):
		# Area owned by me
		A1 = len()
		return (np.norm(self.Z[(player+1)/2],ord='0') + A1 - A2) # ADD AREAS TODO

	# remove all elements in the same connected component as pos from P
	def remove(self, pos, P):
		unique = U[pos]
		for p in nbd(pos):
			if(U[p] == unique):
				P = remove(p, P)
		P[pos] = 0
		return P







