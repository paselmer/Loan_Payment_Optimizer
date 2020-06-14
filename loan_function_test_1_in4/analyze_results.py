""" Code to analyze results of loan_function_test_1_in4 """

import numpy as np
from matplotlib import pyplot as plt
import pdb

# The total number of simulations run
nSims = 10271580

# These are lists of the names of the files that contain the "wins" and "losses"
losses_files = ['losses_1of4.txt', 'losses_2of4.txt', 'losses_3of4.txt', 'losses_4of4.txt']
wins_files = ['win_1of4.txt', 'win_2of4.txt', 'win_3of4.txt', 'win_4of4.txt']

# Read in all the loss margins from all the loss files
loss_margin = []
for losses_file in losses_files:
    line = True
    with open(losses_file,'r') as f_obj:
        while(line):
            line = f_obj.readline()
            split_line = line.split(',')
            try:
                loss_margin.append(float(split_line[3]))
            except:
                # This isn't a CSV line, so just advance to next iteration
                pass
    print('Done with file:\n'+losses_file)
loss_margin = np.asarray(loss_margin)

# Read in all the win margins from all the win files
win_margin = []
for wins_file in wins_files:
    line = True
    with open(wins_file,'r') as f_obj:
        while(line):
            line = f_obj.readline()
            split_line = line.split(',')
            try:
                win_margin.append(float(split_line[3]))
            except:
                pass
    print('Done with file:\n'+wins_file)    
win_margin = np.asarray(win_margin)

if (loss_margin.shape[0] + win_margin.shape[0]) != nSims:
    print('The number of records in the files and the number of simulations')
    print('does not match.')

percent_wins = float(win_margin.shape[0])/float(nSims)
percent_losses = float(loss_margin.shape[0])/float(nSims)
print('% wins:        {0:5.2f}'.format(percent_wins))
print('% losses:      {0:5.2f}'.format(percent_losses)) 
print('mean win ($):  {0:5.2f}'.format(win_margin.mean()))
print('mean loss ($): {0:5.2f}'.format(loss_margin.mean()))
print('max win ($):   {0:5.2f}'.format(win_margin.min()))
print('max loss ($):  {0:5.2f}'.format(loss_margin.max()))
print('min win ($):   {0:5.2f}'.format(win_margin.max()))
print('min loss ($):  {0:5.2f}'.format(loss_margin.min()))
fig, ax = plt.subplots(1,2,figsize=(8,6.5))
ax[0].hist(win_margin,bins='auto')
ax[0].set_title('win margins')
ax[0].set_xlabel('margin in dollars')
ax[0].set_ylabel('frequency of occurrence')
ax[1].hist(loss_margin,bins='auto')
ax[1].set_title('loss margins')
ax[1].set_xlabel('margin in dollars')
fig.suptitle('Margin - Total cost using gradient descent\n minus total cost\
using descending interest')
plt.savefig('margins_histogram.png')
plt.show()

pdb.set_trace()

