import model1 
import numpy as np
import nn
import main 
import models
import logging as log
import tools as tl 
import matplotlib.pyplot as plt

index = tl.index('index.npy')
index = str(index)
tl.cprint('index = {}'.format(index))

log.basicConfig(level=log.WARNING)

model = models.model1()

softmax = nn.softmax()
def Action(value):
    # value = softmax.forward(value)
    rand = np.random.rand(value.shape[0])
    action = np.argmax(rand*value)
    return action


def play():
    Loss = 0
    Reward = []
    player = 1
    state = np.zeros((5,5))
    value = model.forward(state)
    action = np.argmax(value)
    for i in range(24):
        state, reward  = main.go(state,action,player)
        temp1 = model.forward(state)
        moves = np.reshape(np.where(state==0,1,0),-1)
        temp2 = Action(moves*temp1)
        dx = np.zeros(25)
        log.debug('index {}, action {}, value {},reward {},temp2 {}'.format(i,action, value, reward, temp2))
        dx[action] = (value[action] - (reward/50 - temp1[temp2]))
        loss = (np.abs(dx[action]))**2
        model.backward(dx)
        model.update()
        
        player = 3-player
        action = temp2
        Loss = Loss + loss
        Reward.append(reward)
        # print('loss {:4f}, action {}, reward {}'.format(loss, action, reward))
        # print(state)
    return Loss/25, np.mean(Reward[2:])

L = []
R = []
for j in range(1000):
    loss, reward = play()
    L.append(loss)
    R.append(reward)

    tl.cprint('index = {} LOSS = {:4f} , Reward {:4f}'.format(j, np.mean(L), np.mean(R)))
np.save('data/loss'+ index +'.npy', L)
np.save('data/reward'+ index +'.npy', R)
plt.plot(L)
plt.xlabel('no. of games')
plt.ylabel('average loss in a game')
plt.title('softmax greedy, on policy')
plt.savefig('data/loss'+ index +'.png')
plt.close()
plt.plot(R)
plt.xlabel('no. of games')
plt.ylabel('average reward per step in a game')
plt.title('softmax greedy, on policy')
plt.savefig('data/reward'+ index +'.png')
W = model.get_weights()
np.save('data/weights'+ index +'.npy',W)


    
    
    
