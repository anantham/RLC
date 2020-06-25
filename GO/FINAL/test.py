import model1 
import numpy as np
import nn
import main 

md1  = model1.model1()
md2 = model1.model1()

#Initial board state
x = np.zeros((5,5))


for i in range(50):

    t = np.ones(25)
    #first player
    print(x,'\n')
    v1 = md1.forward(x,update=True)
    t[np.reshape(x,25)>0] = 0
    a1 = np.argmax(v1*t)
    x,r1 = main.go(x,a1,1)
    print('action {}, reward {}, player {}, index {}'.format(a1,r1,1,i))
    
    print( x,'\n')
    v2 = md2.forward(x,update=True)
    t[np.reshape(x,25)>0] = 0
    a2 = np.argmax(v2*t)
    x,r2 = main.go(x,a2,2)
    print('action {}, reward {}, player {}, index {}'.format(a2,r2,2,i+1))
    