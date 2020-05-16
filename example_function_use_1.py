import numpy as np
import pdb
from loan_functions import *

max_iters = 9000
a = 100.0
ndec = 2
L0 = np.array([18000.0, 18000.0, 20000.0])
I = np.array([0.002358333, 0.002875, 0.00313333333])
mp = np.array([202.2696720577595, 207.36999373455785, 134.73627186327587])


#x0 = compute_monthly_loan_payment(18000.0,0.002358333,100.0)
#x1 = compute_monthly_loan_payment(18000.0,0.002875,100.0)
#x2 = compute_monthly_loan_payment(20000.0,0.00313333333,200.0)
#print(x0,x1,x2)

algo1_out = optimize_algo1(L0, I, mp, a, max_iters, ndec)

pdb.set_trace()
