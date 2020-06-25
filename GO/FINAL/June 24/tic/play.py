import cv2
import pickle
import numpy as np
import tictac_graphic as gr
import matplotlib.pyplot as plt
import tools as tl
import time
import random
import sys
import os
import main
import nn


cwd = os.getcwd()

def load_state(filename):
    Q = pickle.load(open( cwd + "/data/" + filename, "rb"))
    print("load_state:- load_state:- state loaded")
    return Q

def plot(output):
    # cv2.destroyAllWindows()
    
    plt.close()
    plt.imshow(output)
    plt.show(block=False)
    # plt.pause(3)
    # cv2.imshow(state, output)
    # cv2.waitKey(2)

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

model = model1()
w = np.load('weights87.npy', allow_pickle= True)
model.set_weights(w)
state = np.random.randint(0,1,(5,5))

def Action(state):
    value = model.forward(state)
    empty = np.reshape(np.where(state==0,1,0),-1)  # legal moves
    action = np.argmax(value*empty)
    return action


def play():
    # filename = input('Enter Q file adrress')
    # Q = load_state(filename)
    toss = input('Do you want to start')
    # state = '000000000'
    state = np.random.randint(0,1,(5,5))
    output = gr.go(state)
    plot(output)

    tl.cprint('you are STAR')
    p2 = 2      
    p1 = 1
    if toss in {'y','Y', 'yes', 'Yes'}:
        while True :#tl.Result(state)[0]==0:
            
            print('Current state is {}'.format(state))
            action = input('Enter your action')
            state, reward = main.go(state,action, p2)
            output = gr.go(state)
            plot(output)
            
            print('Current state is {}'.format(state))
            action = Action(state)
            print('Computer chose action {}'.format(action))
            state, reward = main.go(state, action,p1)
            
            output = gr.go(state)
            plot(output)
            
    else :       
        while True: #tl.Result(state)[0]==0:
            print('Current state is {}'.format(state))
            action = Action(state)
            print('Computer choose action {}'.format(action))
            state, reward = main.go(state, action,p1)
            print('reward {}, action {}, p2 {}'.format(reward,action,p2))
            output = gr.go(tl.array_to_string(state))
            plot(output)
            print('Current state is {}'.format(state))
            action = input('Enter your action')
            #action = Action(state)
            state, reward = main.go(state, int(action), p2)
            print('reward {}, action {}, p2 {}'.format(reward,action,p2))
            output = gr.go(tl.array_to_string(state))
            plot(output)
            

play()
    
