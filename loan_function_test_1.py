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
pdb.set_trace()

# Record things here like # of wins, avg spread, um...something else
# Also, open some files to record results of each test?
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
    if algo1_out[0] <= descI_out[0]: wins += 1
    c += 1
    if c % 10000 == 0:
        print('{0:d} of {1:d} complete. {2:d} wins'.format(c,n_combos,wins)) 
    
    
print('wins = ', wins)
print('total combos = ',combos.shape[0])
    
