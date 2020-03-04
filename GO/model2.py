import nn
import tools as tl
import numpy as np

class model2():

	def __init__(self):
		# noOfFilters, input dim, shape of filter
		self.conv1 = nn.convolve3d((5,1,2,2), mode = 'same')
		self.add1 = nn.add()
		self.conv2 = nn.convolve3d((5,5,2,2), mode = 'same')
		self.add2 = nn.add()
		self.lin1 = nn.linear()
		self.add3 = nn.add()
		self.lin2 = nn.linear()
		self.add4 = nn.add()
		self.sig = nn.sigmoid()
		self.mse = nn.mse()

		self.layers = [self.conv1,self.add1,self.conv2,self.add2,self.lin1,self.add3,self.lin2,self.add4,self.sig]

		self.conv1.set_param(np.random.randn(5,1,2,2)/(np.sqrt(1*2*2)))
		self.conv2.set_param(np.random.randn(5,5,2,2)/(np.sqrt(5*2*2)))
		self.lin1.init_param((25*5,50))
		self.lin2.init_param((50,25))

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