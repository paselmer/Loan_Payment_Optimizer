import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import pdb
from loan_samples import *
from loan_functions import *

mp_now = compute_monthly_loan_payment(372000.0,0.03875/12.0,360)
mp_new = compute_monthly_loan_payment(372000.0,0.03100/12.0,360)
print(mp_now,mp_new)
pdb.set_trace()

# Note: Algo 2 takes a long time to run!
#w, n, gt = gradient_descent_algo2(L0, I, p, a, 30, 3)
#pdb.set_trace()

Dtot, ts = descending_interest_method(L0, I, p, a, 2)
print('Descending interest method total: {:.2f} {:d}'.format( Dtot, ts))

tot, ts, w, nts = optimize_algo1(L0, I, p, a, 9000, 2, 0.001)
print('Algo1 method total: {:.2f} {:.1f}'.format( tot, ts))

print("Descending interest minus algo1 = {:.2f}\n".format(Dtot-tot))

print("******** ALGO1 SUMMARY ********")
for i in range(0,len(nts)):
    print("w:   ",w[i])
    print("nts: ",nts[i])

#w, n, Gtot = gradient_descent_algo1(L0, I, p, a, 9000)
#print('Gradient descent method total: {:.2f}'.format(Gtot))
#print('n = ',n)
#print('w = ',w)

#tot, ts = compute_total_cost(L0[2], I[2], p[2]+a, 2)

pdb.set_trace()
