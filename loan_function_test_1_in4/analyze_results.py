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

percent_wins = float(win_margin.shape[0])/float(nSims) * 100
percent_losses = float(loss_margin.shape[0])/float(nSims) * 100
with open('margins_stats.txt', 'w') as f_obj:
    f_obj.write('% wins:        {0:5.2f}\n'.format(percent_wins))
    f_obj.write('% losses:      {0:5.2f}\n'.format(percent_losses)) 
    f_obj.write('mean win ($):  {0:5.2f}\n'.format(win_margin.mean()))
    f_obj.write('mean loss ($): {0:5.2f}\n'.format(loss_margin.mean()))
    f_obj.write('max win ($):   {0:5.2f}\n'.format(win_margin.min()))
    f_obj.write('max loss ($):  {0:5.2f}\n'.format(loss_margin.max()))
    f_obj.write('min win ($):   {0:5.2f}\n'.format(win_margin.max()))
    f_obj.write('min loss ($):  {0:5.2f}\n'.format(loss_margin.min()))
fig, ax = plt.subplots(1,2,sharey=True,figsize=(6.7,5.6))
plt.margins(0.1,tight=False)
ax[0].hist(win_margin,bins='auto')
ax[0].set_title('win margins')
ax[0].set_xlabel('margin in dollars')
ax[0].set_ylabel('frequency of occurrence')
ax[0].set_xlim(-12e3,0)
ax[1].hist(loss_margin,bins='auto')
ax[1].set_title('loss margins')
ax[1].set_xlabel('margin in dollars')
ax[1].set_xlim(0,12e3)
plt.subplots_adjust(top=0.8)
fig.suptitle('Margin - Total cost using gradient descent\n minus total cost \
using descending interest')
plt.savefig('margins_histogram.png')
plt.show()

pdb.set_trace()

