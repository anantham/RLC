import nn
import tools as tl
import numpy as np

# model = nn.sequential(
# 	layers=
# 		self.conv1 = nn.convolve3d(shape =(5,1,3,3), mode = 'valid', param = 'he'),
# 		self.add1 = nn.add(),
# 		self.conv2 = nn.convolve3d(shape=(25,5,3,3), mode = 'valid', param = 'he'),
# 		self.add2 = nn.add(),
# 		self.lin = nn.linear(shape=(25,25), param = 'he'),
# 		self.add3 = nn.add(),
# 		self.sig = nn.sigmoid(),
# 		self.mse = nn.mse()

# )

class model1():

	def __init__(self):
		# noOfFilters, input dim, shape of filter
		self.conv1 = nn.convolve3d(shape =(5,1,3,3), mode = 'valid', param = 'he')
		self.add1 = nn.add()
		self.conv2 = nn.convolve3d(shape=(25,5,3,3), mode = 'valid', param = 'he')
		self.add2 = nn.add()
		self.lin = nn.linear(shape=(25,25), param = 'he')
		self.add3 = nn.add()
		self.softmax = nn.softmax()
		self.mse = nn.mse()
		
		self.layers = [self.conv1,self.add1,self.conv2,self.add2,self.lin,self.add3,self.softmax]

	def forward(self, x, y = None, update = True):
		if(x.ndim == 2):
			n, m = x.shape
			x = x.reshape([-1,n,m])

		for layer in self.layers:
			x = layer.forward(x)

		# x is now a probability distribution 

		
		if(update):
			loss = self.mse.forward(x,y)
			dx = self.mse.backward()

			for layer in reversed(self.layers):
				dx = layer.backward(dx)
				layer.update()
			return loss
		#print('forward pass caculated,{}'.format(np.shape(x)))			
		return x
