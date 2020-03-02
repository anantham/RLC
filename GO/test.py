import nn
import main 
import sys
import os
import tools as tl

def play(s1)

    v1 = model1(s1,update =False)
    a1 = np.argmax(v1)
    s2,r1 = main.go(s1,a1, 1)


    v2 = model2(s2, update=False)
    a2 = np.argmax(v2)
    s3, r2 = main.go(s2,a2,2)

    return everthing

start state = play(emtpy board)

while terminate:
    
