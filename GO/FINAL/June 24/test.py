import model1 
import numpy as np
import nn
import main 
import models
import logging as log
import tools as tl 
import matplotlib.pyplot as plt

log.basicConfig(level=log.WARNING)

model1 = models.model1()
model2 = models.model1()

def play():
    Loss = 0
    Reward = 0
    player = 1
    state = np.zeros((5,5))
    value = model.forward(state)
    action = np.argmax(value)
    for i in range(24):
        state, reward  = main.go(state,action,player)
        temp1 = model.forward(state)
        moves = np.reshape(np.where(state==0,1,0),-1)
        temp2 = np.argmax(temp1*moves)
        dx = np.zeros(25)
        log.debug('index {}, action {}, value {},reward {},temp2 {}'.format(i,action, value, reward, temp2))
        dx[action] = value[action] - (reward/50 - temp1[temp2])
        loss = (np.abs(dx[action]))**2
        model.backward(dx)
        model.update()
        
        player = 3-player
        action = temp2
        Loss = Loss + loss
        Reward += reward
        #print('loss {:4f}, action {}, reward {}'.format(loss, action, reward))
        #print(state)
    return Loss/25, Reward/25

L = []
R = []
for j in range(1000):
    loss, reward = play()
    L.append(loss)
    R.append(reward)

    tl.cprint('index = {:4f} LOSS = {:4f} , Reward {:4f}'.format(j, np.mean(L), np.mean(R)))
np.save('loss.npy', L)
np.save('reward.npy', R)
plt.plot(L)
plt.savefig('loss.png')
plt.close()
plt.plot(R)
plt.savefig('reward.png')
W = model.get_weights()
np.save('weights.npy',W)


    
    
    
