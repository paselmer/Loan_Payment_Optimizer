""" 

The point of this code is to prove that the descending interest method
is not always the optimal method.

The code computes the grand total cost of using the "gradient descent"
method and the "descending interest" method to pay 2 loans, assuming there
are $100 to apply above the loans' minimum payment.

The starting principal of loan X varies. It varies from being equal to the
other loan's starting principal to + $10000 greater. All other parameters
are held constant: the interests, the length (term), the extra money (a).
NOTE though, that the changing the starting principal changes the minimum
payment as per the "present value" equation used in creating amortized loans.

Each variation of loan X's principal yeilds a different total cost.
The total cost as a function of difference in starting principal is plotted
to compare methods.

"""

import numpy as np
import matplotlib.pyplot as plt
from loan_functions import *

# Interests
IA = 0.35/12.0
IB = 0.10/12.0

# Term of loans (# of timesteps)
# B loan's min payment will be computed within loop
N = 100.0 

x = 10000.0
nx = 800
max_iters = 9000
a = 100.0
L0A = 500.0
L0B = L0A + np.linspace(0.0, x, nx)
dL0 = L0B - L0A

mp1 = compute_monthly_loan_payment(L0A,IA,N) 

Tgd = []
Tdi = []
for LB in L0B:
    
    L = np.array( [L0A, LB] )
    I = np.array( [IA, IB] )
    mpB = compute_monthly_loan_payment(LB, IB, N)
    mp = np.array( [mp1, mpB] )
    
    w, n, grand_total_paid = gradient_descent_algo1(L, I, mp, a, max_iters, 0.01)
    grand_total, tsteps = descending_interest_method(L, I, mp, a, 2)
    Tgd.append(grand_total_paid)
    Tdi.append(grand_total)
    

Tgd = np.array(Tgd)
Tdi = np.array(Tdi)

fig, ax = plt.subplots(2,1,figsize=(9,9),sharex=True)
ax[0].plot(dL0,Tdi,color='green',label='descending interest')
ax[0].plot(dL0,Tgd,color='orange',label='gradient descent')
ax[0].legend()
#ax[0].set_xlabel('difference between loan principals ($)')
ax[0].set_ylabel('total amount paid ($)')
ax[1].plot(dL0,(Tdi-Tgd),color='blue')
ax[1].set_xlabel('difference between loan starting principals ($)')
ax[1].set_ylabel('difference in total amount paid ($)\n descending interest minus gradient descent')
fig.suptitle('Comparison of methods using 2-loan scenario, varying only the starting\n principal of one of the loans.')
plt.show()


