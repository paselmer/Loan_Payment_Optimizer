import sys
sys.path.append('..\\')
import numpy as np
import matplotlib.pyplot as plt
import pdb
from itertools import combinations
from scipy.special import comb
from loan_functions import *

### Define the parameters of the test ###

nLoans = 3
a = 100.0
max_iters = 9000
ndec = 2
# Note to Patrick:
# Since you'll want nLoans (currently 3) loans for each test, you'll have
# to find every possible set of nLoans loans from full set P.
P = np.arange(10000.0,20001.0,2000.0) # Initial principle amounts
I = np.arange(0.019, 0.050, 0.031/10.0)/12.0     # Interest amounts
N = np.arange(100.0,360.0,50.0)            # Length (in timestep) of loan

# Full set of possible combinations of P,I,N
all_poss_combos = []
for p in P:
    for i in I:
        for n in N:
             all_poss_combos.append([p,i,n])
             
# n Choose r - nCr
# len(all_poss_combos) Choose nLoans
print(len(all_poss_combos))
# Array will be shape (combos, nLoans, PIN)
combos = np.array(list(combinations(all_poss_combos, nLoans)))
n2run = int(combos.shape[0]/4)
combos = combos[:n2run]
print('About to run {0:d} through {1:d}'.format(0,n2run))

# Record things here like # of wins, avg spread, um...something else
# Also, open some files to record results of each test?
# Open file to record losses.
loss_file = 'losses_1of4.txt'
win_file = 'win_1of4.txt'
f_obj = open(loss_file, 'w')
f_obj2 = open(win_file, 'w')
mp = np.zeros(nLoans)
wins = 0
c = 0
n_combos = combos.shape[0]
for combo in combos:
    for k in range(0,nLoans):
        mp[k] = compute_monthly_loan_payment(combo[k,0], combo[k,1], combo[k,2])
    # [0]
    algo1_out = optimize_algo1(combo[:,0], combo[:,1], mp, a, max_iters, ndec)
    descI_out = descending_interest_method(combo[:,0], combo[:,1], mp, a, ndec)
    if algo1_out[0] <= descI_out[0]:
        f_obj2.write('{0:d}, {1:20.3f}, {2:20.3f}, {3:20.3f}\n'.format(
                 c,algo1_out[0],descI_out[0],algo1_out[0]-descI_out[0]))
        # Don't write out combo for wins. You'll just have to ref c.        
        wins += 1
    else:
        f_obj.write('{0:d}, {1:20.3f}, {2:20.3f}, {3:20.3f}\n'.format(
                 c,algo1_out[0],descI_out[0],algo1_out[0]-descI_out[0]))
        f_obj.write(str(combo)+'\n\n')
    c += 1
    if c % 10000 == 0:
        print('{0:d} of {1:d} complete. {2:d} wins'.format(c,n_combos,wins)) 
    
f_obj.close()
f_obj2.close()
print('wins = ', wins)
print('total combos = ',combos.shape[0])
    
