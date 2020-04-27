
import nn

import tools as tl 


import numpy as np
from itertools import count
from collections import namedtuple


gamma = 0.5 #discount


#first develop

#suggestions : dummy linear dims have been made adjust for inputs : make on top of or inherit from  base model class 

#add optimizer , backprop ,  smooth_l1 loss in nn

#adjust for main func


SavedAction = namedtuple('SavedAction', ['log_prob', 'value'])


class Policy() :
	def __init__(self) :
		self.affine1 = nn.Linear(4, 128)

		#actor's layer

		self.action_head = nn.Linear(128, 2)

		#critic's layer 

		self.value_head = nn.Linear(128, 1)

		#Buffer to save rewards and actions 

		self.saved_actions = []
		self.rewards = []


	def forward(self , x) :

		#forward of both actor and critic

		x = nn.relu(self.affine1(x))

		# actor: choses action to take from state s_t 
		# by returning probability of each action

		action_prob = nn.softmax(self.action_head(x))




        # critic: evaluates being in the state s_t

        state_values = self.value_head(x)

        # return values for both actor and critic as a tuple of 2 values:
        # 1. a list with the probability of each action over the action space
        # 2. the value from state s_t 
        return action_prob, state_values

model = Policy()

#optimizer = add optimizer


eps = np.finfo(np.float32).eps.item()


def Categorical(probs) :

		A_as_numbers = np.argmax(np.log(probs) + np.random.gumbel(size=probs.shape), axis=1)
	    A_one_hot = np.eye(probs.shape[1])[A_as_numbers].reshape(probs.shape)

	    return A_one_hot



	

def sample(a) :
	length = int(a.shape[0])

	choice = random.choice(list(np.arange(length)))

	idx = choice

	val = a[choice]

	return val , idx



def select_action(state) :
	 probs, state_value = model(state)

	 # create a categorical distribution over the list of probabilities of actions
	 m = Categorical(probs)


	 # and sample an action using the distribution
	 action , idx = sample(m)

	 # save to action buffer

	 model.saved_actions.append(SavedAction(np.log(probs[idx]) , state_value))

	 #the action to take 
	 return action




def finish_episode():
    """
    Training code. Calculates actor and critic loss and performs backprop.
    """
    R = 0
    saved_actions = model.saved_actions
    policy_losses = [] # list to save actor (policy) loss
    value_losses = [] # list to save critic (value) loss
    returns = [] # list to save the true values

    # calculate the true value using rewards returned from the environment
    for r in model.rewards[::-1]:
        # calculate the discounted value
        R = r + gamma * R
        returns.insert(0, R)

        returns = (returns - np.mean(returns) ) / (np.std(returns) + eps)

    for (log_prob, value), R in zip(saved_actions, returns):

    	advantage = R - value

    	# calculate actor (policy) loss 
        policy_losses.append(-log_prob * advantage)

    

    # reset gradients here
    #optimizer.zero_grad()
        





    # calculate critic (value) loss using L1 smooth loss code should be updated for this in nn
    value_losses.append(nn.smooth_l1_loss(value, R))

    # sum up all the values of policy_losses and value_losses
    loss = np.sum(policy_losses) + np.sum(value_losses)

    #perform backprop here 
    #loss.backward()
    #optimizer.step()

    # reset rewards and action buffer
    del model.rewards[:]
    del model.saved_actions[:]



def main() :
	#define the main func here 
	print("main")



if __name__ == '__main__':
	main()



        








