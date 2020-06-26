import numpy as np
import nn

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

def model2():
    model = nn.sequential(
    layers=
    [nn.temp1(),
    nn.convolve3d(shape =(5,1,3,3), mode = 'valid', param = 'he'),
    nn.add(),
    nn.convolve3d(shape=(15,5,2,2), mode = 'valid', param = 'he'),
    nn.add(),
    nn.convolve3d(shape=(25,15,2,2), mode = 'valid', param = 'he'),
    nn.add(),
    nn.linear(shape=(25,25), param = 'he'),
    nn.add(),
    nn.sigmoid()]

    )
    return model

# Let input be 7*7
def model3():
    model = nn.sequential(
    layers=
    [nn.temp1(),
    nn.convolve3d(shape =(5,1,5,5), mode = 'valid', param = 'he'),
    nn.add(),
    nn.convolve3d(shape=(15,5,3,3), mode = 'valid', param = 'he'),
    nn.add(),
    nn.convolve3d(shape=(49,15,3,3), mode = 'valid', param = 'he'),
    nn.add(),
    nn.linear(shape=(441,49), param = 'he'),
    nn.add(),
    nn.sigmoid()]

    )
    return model

