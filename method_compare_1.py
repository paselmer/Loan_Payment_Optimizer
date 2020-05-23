""" The point of this code is to prove that the descending interest method
    is not always the optimal method.
"""

# Initial principal vs. Total cost
#
# 2 Lines:
# - descending interest
# - gradient descent
#
# 2 static loans, 1 dynamic
# dynamic loan add increasing amounts from 0 to x

import numpy as np
import matplotlib.pyplot as plt
from loan_functions import *
import pdb

# Interests
I1 = 0.35/12.0
Ix = 0.55/12.0#0.10/12.0

# Term of loans (# of timesteps)
# x loan's min payment will be computed within loop
N = 100.0 

x = 10000.0
nx = 800
max_iters = 9000
a = 100.0
L01 = 500.0
L0x = L01 + np.linspace(0.0, x, nx)
dL0 = L0x - L01

mp1 = compute_monthly_loan_payment(L01,I1,N) 

Tgd = []
Tdi = []
for Lx in L0x:
    
    L = np.array( [L01, Lx] )
    I = np.array( [I1, Ix] )
    mpx = compute_monthly_loan_payment(Lx, Ix, N)
    mp = np.array( [mp1, mpx] )
    
    w, n, grand_total_paid = gradient_descent_algo1(L, I, mp, a, max_iters, 0.01)
    grand_total, tsteps = descending_interest_method(L, I, mp, a, 2)
    Tgd.append(grand_total_paid)
    Tdi.append(grand_total)
    

Tgd = np.array(Tgd)
Tdi = np.array(Tdi)

fig, ax = plt.subplots(1,1,figsize=(9,6))
ax.plot(dL0,Tgd,color='orange',label='gradient descent')
ax.plot(dL0,Tdi,color='green',label='descending interest')
ax.legend()
ax.set_xlabel('difference between loan principals')
ax.set_ylabel('total amount paid')
plt.show()
pdb.set_trace()


