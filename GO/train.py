import nn
import main 
import pm
import sys
import os
import tools as tl
from itertools import product
import numpy as np

import model1 as Model1
import model2 as Model2

board = {1:[], 2:[]}
board[0] = list(set(list(product(range(pm.size), repeat = 2))))

# values of states
v = []
# actions chosen in this episode
a = []
# states traversed in this episode
s = []
# rewards gained in this episode
r = []

loss = []

index = tl.index('index.npy')
print(index)

def normalize(r):
	return r/(2*pm.size**2) + 0.5

def play(s1):
	turn = 0

	v1 = model1.forward(s1, update=False)
	a1 = np.argmax(v1) # \in [0,24]
	s2, r1 = main.go(s1,a1, 1)

	v2 = model2.forward(s2, update=False)
	a2 = np.argmax(v2)
	s3, r2 = main.go(s2,a2,2)

	v3 = model1.forward(s3, update=False)
	a3 = np.argmax(v3)
	s4, r3 = main.go(s3,a3,1)

	v4 = model2.forward(s4, update=False)

	v.append(v1)
	v.append(v2)
	v.append(v3)
	v.append(v4)

	a.append(a1)
	a.append(a2)
	a.append(a3)

	s.append(s1)
	s.append(s2)
	s.append(s3)
	s.append(s4)

	r.append(normalize(r1))
	r.append(normalize(r2))
	r.append(normalize(r3))

	v1[a1] = normalize(r1) - normalize(r2) + pm.discount_factor*max(v3)
	loss.append(model1.forward(s1,v1))

	turn += 1 # s1 v1 has been taught

	v2[a2] = normalize(r2) - normalize(r3) + pm.discount_factor*max(v4)
	loss.append(model2.forward(s2,v2))

	turn += 1 # s2 v2 has been taught

	for i in range(21):
		# get a4 from v4
		ai = np.argmax(v[turn+1])
		# s5 r4 from s4 and a4
		sj, ri = main.go(s[turn+1],ai, 2)

		# v5 from s5
		vj = model1.forward(sj, update=False)
		aj = np.argmax(vj) # a5
		# we have s6
		sk, rj = main.go(sj,aj,1)

		# v6 from s6
		vk = model2.forward(sk, update=False)
		ak = np.argmax(vk) # a6
		# s7 from s6
		sl, rk = main.go(sk,ak,2)

		# v5, v6
		v.append(vj)
		v.append(vk)

		# a4, a5
		a.append(ai)
		a.append(aj)

		# s5, s6
		s.append(sj)
		s.append(sk)

		# r4, r5
		r.append(normalize(ri))
		r.append(normalize(rj))

		# turn = 2, v3[a3] needs r4 and v5
		v[turn][a[turn]] = r[turn] - r[turn+1] + pm.discount_factor*max(v[turn+2])
		loss.append(model1.forward(s[turn],v[turn]))

		turn += 1

		# turn = 3, v4[a4] needs r5 and v6!
		v[turn][a[turn]] = r[turn] - r[turn+1] + pm.discount_factor*max(v[turn+2])
		loss.append(model2.forward(s[turn],v[turn]))

		turn += 1


model1 = Model1.model1()
model2 = Model1.model1()

#load_index = input('enter input index')
load_index = index-1

W1 = tl.load_Q('data/param/W1'+str(load_index))
W2 = tl.load_Q('data/param/W1'+str(load_index))

for l, n in zip(model1.layers,W1):
	l.set_param(n)

for l, n in zip(model2.layers,W2):
	l.set_param(n)

for i in range(10**4):
	# start the game
	play(main.boardToState(board))
	tl.fprint('ptp 1lin1 = {:4f}, std 2lin1 = {:4f}, ptp 2lin2 ={:4f}'.format(np.ptp(model1.lin.w),  np.std(model2.conv1.w), np.ptp(model2.lin.dw)))


W1 = [l.w for l in model1.layers]
W2 = [l.w for l in model2.layers]


tl.dump_Q(W1,'data/param/W1'+str(index))
tl.dump_Q(W2,'data/param/W2'+str(index))

print('Trained weights saved at data/param/W1 and W2 {}'.format(index))  


	
