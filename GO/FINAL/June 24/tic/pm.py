# # define constants and other parameters
# size = 5
# board_pixel = 2000
# myHomeFolder = '' #'C:\\Users\\Aditya Prasad\\OneDrive - Indian Institute of Science\\Documents\\IISc\\Semester 2\\Robot\\Project\\GO'
# go_board_adress = 'blank.jpg' #'C:\\Users\\Aditya Prasad\\OneDrive - Indian Institute of Science\\Documents\\IISc\\Semester 2\\Robot\\Project\\GO\\blank.jpg'

                            #### TRAINING PARAMETERS##########

iterations = 1000*100     #number of iterations for training
alpha= 0.2       # update rate   a = a + ALPHA*(a'-a)
delta = 0
epsilon = 0
path_length = 4
symmetry_update = True
init_reward = 4
initial_Q = False
discount_factor = 0.9

               				#### NEURAL NETWORK PARAMETERS ########
momentum = 0.8
learning_rate = 0.01

class param:
    min = -1   # min  limit for clip
    max = 1   # upper limit for clip

size = 5
board_pixel = 2000
go_board_adress = 'C:\\Users\\Aditya Prasad\\OneDrive - Indian Institute of Science\\Documents\\IISc\\Semester 2\\Robot\\Project\\GO\\blank.jpg'#'/home/navdeep/TicTac/data/go/board.jpg'
imsize = 1000                      #must be less than shape of imagel
output_adress = 'C:\\Users\\Aditya Prasad\\OneDrive - Indian Institute of Science\\Documents\\IISc\\Semester 2\\Robot\\Project\\GO'#'/home/navdeep/TicTac/data/go' #state_in_string.jpg
