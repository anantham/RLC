import nn
import tools as tl
import numpy as np

class model1():

	def __init__(self):
		# noOfFilters, input dim, shape of filter
		self.conv1 = nn.convolve3d((5,1,3,3), mode = 'valid')
		self.add1 = nn.add()
		self.conv2 = nn.convolve3d((25,5,3,3), mode = 'valid')
		self.add2 = nn.add()
		self.lin = nn.linear()
		self.add3 = nn.add()
		self.sig = nn.sigmoid()
		self.mse = nn.mse()

		self.layers = [self.conv1,self.add1,self.conv2,self.add2,self.lin,self.add3,self.sig]

		self.conv1.set_param(np.random.randn(5,1,3,3)/(np.sqrt(5*5*2)))
		self.conv2.set_param(np.random.randn(25,5,3,3)/(np.sqrt(5*4*4*2)))
		self.lin.init_param((25,25))


	def forward(self, x, y = None, update = True):
		for layer in self.layers:
			x = layer.forward(x)
		
		if(update):
			loss = self.mse.forward(x,y)
			dx = self.mse.backward()

			for layer in reversed(self.layers):
				dx = layer.backward(dx)
				layer.update()
			return loss
		return x
