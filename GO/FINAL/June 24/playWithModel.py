import pm
import main
import numpy as np
import nn
import models


def model1():
    model = nn.sequential(
    layers=
    [nn.temp1(),
    nn.convolve3d(shape =(5,1,3,3), mode = 'valid', param = 'he'),
    nn.add(),
    nn.convolve3d(shape=(25,5,3,3), mode = 'valid', param = 'he'),
    nn.add(),
    nn.linear(shape=(25,25), param = 'he'),
    nn.add(),
    nn.sigmoid()]

    )
    return model

model = models.model2()
w = np.load('weights42.npy', allow_pickle= True)
model.set_weights(w)


player = 1

board = {1:[], 2:[]}
points = {1:0, 2:0}
turn = 0 
hist = [] # history of board positions

# initially all positions belong to blank - set(board[1]) - set(board[2]))
#board[0] = list(set(list(product(range(size), repeat = 2))))

state = np.zeros((pm.size,pm.size))

while(turn<pm.size**2):
    #randMove = board[0][np.random.randint(len(board[0]))]
    print("Enter your move")
    move = int(input())
    
    stateNew, r = main.go(state,move,player)
    player = 3 - player 
    
    print('next state {}, reward = {} \n \n '.format(stateNew,r))
    turn+=1
    
    value = model.forward(stateNew)
    flat = stateNew.flatten()
    empty = np.ones((pm.size,pm.size)).flatten()
    empty[flat>0] = 0
    print(value*empty)
    action = np.argmax(value*empty)
    print("Model chooses to play at "+str(action))
    state, r = main.go(stateNew,action,player)
    # rule against suicide
    if(r == -2):
        empty[np.argmax(value*empty)] = 0
        action = np.argmax(value*empty)
        state, r = main.go(stateNew,action,player)

    player = 3 - player 
    
    print('next state {}, reward = {} \n \n '.format(state,r))
    turn += 1