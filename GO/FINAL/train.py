import nn
import main 
import pm
import sys
import os
import tools as tl
from itertools import product
import numpy as np
import logging

logging.basicConfig(level=logging.DEBUG)

import model1 as Model1
import model2 as Model2

# pick greedy choice 70% of the time
eps = 0.6

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

	logging.debug('dimension of input state = {}'.format(np.shape(s1)))

	v1 = model1.forward(s1)
	print('dimension of output pass {}, {}'.format(np.shape(v1), v1))
	print('value {}'.format(v1))
	a1 = np.argmax(v1) # in [0,24]
	if(np.random.uniform(0,1)>eps):
		zeros = np.where(s1==0)
		indexRand = np.random.randint(0,len(zeros[0]))
		a1 = zeros[0][indexRand]*5+zeros[1][indexRand]
	print('action {}'.format(a1))
	s2, r1 = main.go(s1,a1,1)
	print('next state {}, reward = {}'.format(s2,r1))
	v2 = model1.forward(s2)
	
	a2 = np.argmax(v2)
	if(np.random.uniform(0,1)>eps):
		zeros = np.where(s2==0)
		indexRand = np.random.randint(0,len(zeros[0]))
		a2 = zeros[0][indexRand]*5+zeros[1][indexRand]
	print('action {}'.format(a2))
	s3, r2 = main.go(s2,a2,2)
	print('next state {}, reward = {}'.format(s3,r2))
	print("s3 done \n\n")

	v3 = model1.forward(s3)
	a3 = np.argmax(v3)
	if(np.random.uniform(0,1)>eps):
		zeros = np.where(s3==0)
		indexRand = np.random.randint(0,len(zeros[0]))
		a3 = zeros[0][indexRand]*5+zeros[1][indexRand]
	print('action {}'.format(a3))
	s4, r3 = main.go(s3,a3,1)
	print('next state {}, reward = {}'.format(s4,r3))

	v4 = model1.forward(s4)

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
	loss.append(model1.fit(s1,v1))

	turn += 1 # s1 v1 has been taught

	v2[a2] = normalize(r2) - normalize(r3) + pm.discount_factor*max(v4)
	loss.append(model2.fit(s2,v2))

	turn += 1 # s2 v2 has been taught

	print("starting for loop \n\n")
	player = 1
	# 3 moves played. 22 moves left. 22/2 loops left.
	while(turn<=pm.size**2):
		player = 3-player
		# get a4 from v4
		ai = np.argmax(v[turn+1])
		print('dimension of output pass {}, {}'.format(np.shape(v[turn+1]), v[turn+1]))
		if(np.random.uniform(0,1)>eps):
			zeros = np.where(s[turn+1]==0)
			indexRand = np.random.randint(0,len(zeros[0]))
			ai = zeros[0][indexRand]*5+zeros[1][indexRand]
		print('action {}'.format(ai))
		# s5 r4 from s4 and a4
		sj, ri = main.go(s[turn+1],ai,player)
		print('next state {}, reward = {}'.format(sj,ri))

		player = 3-player
		# v5 from s5
		vj = model1.forward(sj)
		aj = np.argmax(vj) # a5
		if(np.random.uniform(0,1)>eps):
			zeros = np.where(sj==0)
			indexRand = np.random.randint(0,len(zeros[0]))
			aj = zeros[0][indexRand]*5+zeros[1][indexRand]
		print('action {}'.format(aj))	
		# we have s6
		sk, rj = main.go(sj,aj,player)
		print('next state {}, reward = {}'.format(sk,rj))

		player = 3-player
		# v6 from s6
		vk = model2.forward(sk)
		ak = np.argmax(vk) # a6
		if(np.random.uniform(0,1)>eps):
			zeros = np.where(sk==0)
			indexRand = np.random.randint(0,len(zeros[0]))
			ak = zeros[0][indexRand]*5+zeros[1][indexRand]		
		print('action {}'.format(ak))
		# s7 from s6
		sl, rk = main.go(sk,ak,player)
		print('next state {}, reward = {}'.format(sl,rk))

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
		loss.append(model1.fit(s[turn],v[turn]))

		turn += 1

		# turn = 3, v4[a4] needs r5 and v6!
		v[turn][a[turn]] = r[turn] - r[turn+1] + pm.discount_factor*max(v[turn+2])
		loss.append(model2.fit(s[turn],v[turn]))

		turn += 1


model1 = nn.sequential(
    layers=
    [nn.convolve3d(shape=(5,1,3,3), mode = 'valid', param = 'he'),
    nn.add(),
    nn.convolve3d(shape=(25,5,3,3), mode = 'valid', param = 'he'),
    nn.add(),
    nn.linear(shape=(25,25), param = 'he'),
    nn.add(),
    nn.sigmoid()],
    loss = nn.mse()
    )

model2 = nn.sequential(
    layers=
    [nn.convolve3d(shape=(5,1,3,3), mode = 'valid', param = 'he'),
    nn.add(),
    nn.convolve3d(shape=(25,2,3,3), mode = 'valid', param = 'he'),
    nn.add(),
    nn.linear(shape=(25,25), param = 'he'),
    nn.add(),
    nn.sigmoid()],
    loss = nn.mse()
    )


#model1 = Model1.model1()
#model2 = Model1.model1()

load_index = input('enter input index')
#load_index = index-1
if(load_index != '0'):
	W1 = tl.load_Q('data/param/W1'+str(load_index))
	W2 = tl.load_Q('data/param/W2'+str(load_index))

	for l, n in zip(model1.layers,W1):
		if(type(n)==int):
			n = np.asarray(0)
		l.set_param(n)

	for l, n in zip(model2.layers,W2):
		if(type(n)==int):
			n = np.asarray(0)
		l.set_param(n)


print("Starting! \n\n")
for i in range(2):
	try:	
		# start the game
		play(main.boardToState(board))
		tl.fprint('ptp 1lin1 = {:4f}, std 2lin1 = {:4f}, ptp 2lin2 ={:4f}'.format(np.ptp(model1.layers[5].w),  np.std(model2.layers[0].dw), np.ptp(model2.layers[5].dw)))
	except KeyboardInterrupt:
		# If we notice delta -> 0 use control C to save and exit training
		W1 = [l.w for l in model1.layers]
		W2 = [l.w for l in model2.layers]


		tl.dump_Q(W1,'data/param/W1_index'+str(index)) #+"_NoOfGames"+str(i)+"_"+str(model1)[1:9])
		tl.dump_Q(W2,'data/param/W2_index'+str(index)) #+"_NoOfGames"+str(i)+"_"+str(model2)[1:9])

		print('Trained weights saved at data/param/W1 and W2 {}'.format(index))  
		 

tl.dump_Q(W1,'data/param/W1_index'+str(index)+"_NoOfGames"+str(i)+"_"+str(model1)[1:9])
tl.dump_Q(W2,'data/param/W2_index'+str(index)+"_NoOfGames"+str(i)+"_"+str(model2)[1:9])

print('Trained weights saved at data/param/W1 and W2 {}'.format(index))  

	
