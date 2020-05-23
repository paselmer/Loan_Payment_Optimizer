import numpy as np
import pdb
from itertools import permutations as perm

def compute_present_value(j,I,p):
    """ Computes Present Value (PV) or an ordinary annuity """
    
    # NOTES:
    # Any ONE of the input arguments can be an array, but the others 
    # must be scalar.
    
    
    # INPUTS:
    # p -> Periodic payment amount
    # I -> Interest, as annual rate. If 9%, enter 0.09.
    # j -> The number of payments
    
    # OUTPUT:
    # PV -> The present value of the annuity
    
    PV = p * ( ( 1 - (1+I)**(-j) )/I )
    
    return PV
    
def compute_future_value(j,I,p):
    """ Computes Future Value (FV) or an ordinary annuity """
    
    # NOTES:
    # Any ONE of the input arguments can be an array, but the others 
    # must be scalar.
    
    
    # INPUTS:
    # p -> Periodic payment amount
    # I -> Interest, as annual rate. If 9%, enter 0.09.
    # j -> The number of payments
    
    # OUTPUT:
    # FV -> The future value of the annuity
    
    FV = p * (((1+I)**j - 1)/I) * (1+I)
    
    return FV   

def compute_monthly_loan_payment(PV,I,j):
    """ Computes the monthly payment on a loan given neccessary inputs """
    
    # INPUTS:
    # PV -> Present value ($)
    # I -> Interest, as annual rate. If 9%, enter 0.09.
    # j -> Number of payments
    
    # [10/8/18] PV ordinary annuity only
    
    p = PV / ( ( 1 - (1+I)**(-j) )/I )
    
    return p

def compute_n_payments(L0, I, p):
    """ Compute the number of payments required to pay a loan off to a 
        balance of zero.
        Any ONE of the input arguments can be an array, but the others 
        must be scalar.
    """
    
    # INPUTS:
    # L0 -> The initial loan amount borrowed.
    # I -> Interest, as annual rate. If 9%, enter 0.09.
    # p -> The periodic payment amount
    
    # OUTPUT:
    # n -> number of payments, either a single number (if all inputs are
    #      scalars), or an array of n's (if one of the inputs is an array)
    
    # Eq. for # of payments, n, as a function of payment amount, p
    n = -1*( np.log( 1 - ((L0*I)/p) )  /  np.log(1+I) )
    return n


def compute_total_cost(L, I, p, ndec, ntsteps=0):
    """ This function uses an old-fashioned loop to compute the total cost
        of a loan.
    """
    
    # INPUTS:
    # L      -> current inital/principal of the loan
    # I      -> interest (presumably annual) of the loan
    # p      -> the payment at each timestep (presumably monthly)
    # nsteps -> optional. compute the total cost only out to this many timesteps,
    #           except if = 0. in this case, compute total cost for entire loan
    #           lifetime (default)
    # If you set ntsteps != 0 then only the total out to nsteps will be
    # computed.
    
    # OUTPUTS:
    # total  -> the total cost of the loan
    # tsteps -> the total number of timesteps it took to pay off the loan
    # L      -> the running principal of the loan, which is returned in its last
    #           state, representing the amount leftover as a negative
    
    # NOTES:
    # [1/30/19] All inputs are assumed to be scalar. 
    
    
    total = 0.0
    tsteps = 0
    leftover = 0.0

    while L > 0:
        leftover = 0.0
        L = np.round( L + np.round(L*I,ndec) - p, ndec )
        total = total + p
        if L < 0: leftover = abs(L)
        tsteps += 1
        if ntsteps == tsteps: break

    total = total - leftover

    return total, tsteps, L

def descending_interest_method(L0, I, p0, a0, ndec):
    """ This function will return the total cost using the method of
        paying off loans in order of descending interest.
    """
    
    # NOTES:
    #
    # [1/21/19]
    # After each payoff, leftover is applied to next iteration.
    # Payment is kept constant at every iteration, save any leftover from
    # previous iteration. So, even after a loan is paid off, the code
    # continues to use that loans minimum payment to pay off
    # remaining loans.
    
    # Test if all values of I are equal
    if (I == np.roll(I,1)).sum() == I.shape[0]:
        #print("!!!! WARNING !!!!")
        #print("Descending interest method results not meaningful in case")
        #print("where all interest rates are the same.")
        #print("!!!!!!!!!!!!!!!!")
        pass
        
    
    L = np.copy(L0)
    p = np.copy(p0)
    nL = L0.shape[0]
    includeLmask = np.ones(nL,dtype=np.bool)
    payedoff_mask = np.zeros(nL,dtype=np.bool)
    a = np.zeros(nL,dtype=np.float64)
    total = 0.0
    rem  = L0.sum()
    tsteps = 0
    leftover = 0.0

    while rem > 0:
        maxI_indx = I[includeLmask].argmax()
        a[:] = 0
        a[maxI_indx] = a0 + leftover + p0[payedoff_mask].sum()
        leftover = 0.0
        L = np.round( L + np.round(L*I,ndec) - (p + a), ndec )
        #print('sum = ',(p0).sum()+p)
        #print('L= ',L,maxI_indx)
        payedoff_mask = L <= 0.0
        if payedoff_mask.sum() > 0:
            leftover = np.abs(L[payedoff_mask].sum())
            includeLmask[payedoff_mask] = False
            p[payedoff_mask] = 0.0
            L[payedoff_mask] = 0.0
        total = total + p0.sum() + a0
        #print('iter: ',tsteps)
        #print('a= ',a)
        #print(payedoff_mask)
        #pdb.set_trace()
        rem = L.sum()
        tsteps += 1
        
    grand_total = total - leftover

    return grand_total, tsteps
        

def gradient_descent_algo1(L0, I, p0, a, max_iters, x = 0.01):
    """ This algorithm determines the weights and the grand total of 
        applying those weights to an amount, a, over the minimum payment
        of an arbitrary number of fixed interest annuities (loans).
        The way the weights are determined are described in the DESCRIPTION
        below.
    """
    
    # DESCRIPTION:
    # This algorithm repeatedly checks which loan's grand total cost is
    # reduced the most by applying the same amount over the minimum fixed
    # payment (a) to each loan. Let's call this loan the "winner."
    # At the end of each iteration, the winner's payment amount is increased
    # by x (fraction of 1, input, defined below). The next iteration begins. 
    # Iterations continue until 100% of "a" (input, defined) below is allocated. 
    # The winner will sometimes change as the payments change, as the code 
    # iterates. At the end of iterations, you're left with an array that 
    # contains the "optimal" fractions (called weights in output) of "a" 
    # to apply to each of the loans.
    # [5/17/20] Like "descending_interest_method" function...
    # Payment is kept constant at every iteration, save any leftover from
    # previous iteration. So, even after a loan is paid off, the code
    # continues to use that loan's minimum payment to pay off
    # remaining loans.
    
    # INPUTS:
    # L0        -> The initial principal loan amount [numpy 1D array]
    # I         -> The interest [numpy 1D array]
    # p0        -> The minimum payment amounts [numpy 1D array]
    # a         -> extra amount over the minimum payments willing to be paid [scalar]
    # max_iters -> maximum iterations to try allocating a [scalar]
    # x         -> fraction by which to increment weights [scalar]
    
    # OUTPUTS:
    # w -> the weights optimizing the allocation of a to each loan [numpy 1D array]
    # n -> the resultant number of payments made for each loan [numpy 1D array]
    # grand_total_paid -> the resultant grand total paid [scalar]
    
    p = np.copy(p0)
    nL = L0.shape[0]
    w = np.zeros(nL)
    delta = np.zeros(nL)
    j = 0
    wrem = 1.0 # represents the remainding % of 'a' to allocate
    
    while (wrem > 0.0):
        delta_last = 0.0
        isave = None
        for i in range(len(L0)):
            n0 = compute_n_payments(L0[i], I[i], p[i])
            t0 = n0 * p[i]
            pmod = p[i] + x*a
            n1 = compute_n_payments(L0[i], I[i], pmod)
            t1 = n1 * pmod
            delta[i] = t0 - t1 # diff in totals b4 & after modification
            if delta[i] > delta_last:
                isave = i
            delta_last = delta[i]
        if isave is None:
            pdb.set_trace()
        else:
            wrem = wrem - x
        w[isave] = w[isave] + x
        p[isave] = p[isave] + x*a
        if j > max_iters: 
            print('Max iterations reached...')
            pdb.set_trace()
            break
        j += 1
    
    paid = []
    n = []
    for i in range(len(L0)): 
        nt = compute_n_payments(L0[i], I[i], p0[i]+w[i]*a)
        paid.append(p[i] * nt)
        n.append(nt)
    grand_total_paid = sum(paid)
    return w, np.asarray(n), grand_total_paid
    
    
def optimize_algo1(L0, I, p, a0, max_iters, ndec, x = 0.01):
    """ Uses  gradient_descent_algo1 to compute total loan cost """
    
    # DESCRIPTION:
    # The "gradient_descent_algo1" function defined above is run using
    # the input loans. This yields a somewhat optimized array of weights
    # and # of timesteps (n). These are the timesteps required to payoff
    # each of the input loans. The total cost is computed by paying all
    # loans to n.min() timesteps. Unless every element of n is the same,
    # you'll still have remaining debt to pay off. Therefore 
    # "gradient_descent_algo1" is called iteratively in a 'while' loop 
    # until the principle of all remaining loans goes to zero. 
    
    # INPUTS:
    # L0        -> The initial principal loan amount [numpy 1D array]
    # I         -> The interest [numpy 1D array]
    # p0        -> The minimum payment amounts [numpy 1D array]
    # a         -> extra amount over the minimum payments willing to be paid [scalar]    
    # max_iters -> maximum iterations to try allocating a [scalar]
    # ndec      -> number of decimal places to round to when computing total cost [scalar]
    # x         -> fraction by which gradient_descent_algo1 should increment weights [scalar]
    
    # OUTPUTS:
    # tot_all     -> total amount paid [scalar]
    # tot_ts      -> total number of timesteps taken to payoff all loans [scalar]
    # all_w       -> list of numpy arrays containing the "best" weights for each iteration
    # all_ntsteps -> list of timesteps taken at each iteration
    
    # NOTES:
    #
    # [1/21/19]
    # Leftover gets applied on next iteration.
    # [4/19/20]
    # Patch put in for condition where >= 2 loans are zero and rest are neg.
    
    nL = L0.shape[0]
    L = np.copy(L0)
    mask = np.ones(nL,dtype=np.bool)
    tot_all = 0.0
    tot_ts = 0
    a = a0
    leftover = 0.0
    all_w = []      # all weights, for all iterations
    all_ntsteps = []# all num of tsteps, for all iterations
    
    while (mask.sum() > 1):
        
        nloans_toploop = mask.sum()
        L = L[mask]
        I = I[mask]
        p = p[mask]
        #print("This many L remain: ",L.shape)
        
        # IF the remainder to be paid on all loans is less than leftover,
        # or the minimum payments, then quit. But be sure to increase  I
        # loans by 1 ts worth of before making this comparison.
        # Do this--> L = np.round( L + np.round(L*I,ndec) - p, ndec )
        L_nts = np.round( L + np.round(L*I,ndec), ndec)
        if (L_nts.sum() < a) | ((L_nts >= p).sum() == 0):
            # First subtract the minimum payments from the remaining loan
            # amounts. The results will likely be negative.
            payment_step = L_nts - p
            # If min payments weren't enough, then apply extra amount 'a'
            after_payment = payment_step.sum()
            if after_payment > 0:
                leftover = a - after_payment
            else: # <= 0
                leftover = a + np.fabs(after_payment)
            L = L*0.0
            mask = np.zeros(L.shape, dtype=np.bool)
            break # done with this while loop
        
        w, n, grand_total_paid = gradient_descent_algo1(L, I,
                                 p, a, max_iters, x)
        
        n = np.ceil(n) # round up to nearest int
        ntsteps = n.min()
        all_ntsteps.append(ntsteps)
        tot_ts = tot_ts + ntsteps
        all_w.append(w)
        #print(w)
        #print(n)
        #print('a : ',a)
        
        for i in range(0,nloans_toploop):
            tot, ts, Lout = compute_total_cost(L[i], I[i], p[i]+a*w[i], ndec, ntsteps)
            tot_all = tot_all + tot
            L[i] = Lout
        
        mask = L >= 0
        # Put a patch in here so that if every value in L is <= 0, mask.sum() == 0
        if (L > 0).sum() == 0: 
            mask = np.zeros(mask.shape,dtype=np.bool)
        invmask = L < 0
        leftover = np.abs(L[invmask]).sum()
        a = p[invmask].sum() + a0 + leftover # keeps total payment amount constant
        #print('******************************\n')
        #print(L,'\n',leftover)
        #print('******************************\n')
    
    # Compute cost of paying off rest of the remaining loan, if applicable 
    if mask.sum() > 0:
        L = L[mask]
        I = I[mask]
        p = p[mask]
        tot, ts, Lout = compute_total_cost(L[0], I[0], p[0]+a, ndec)
        tot_all = tot_all + tot + Lout # Lout should be neg here
        tot_ts = tot_ts + ts
        all_ntsteps.append(ts)
        all_w.append(1.0)
    else:
        #print('All loans must have been paid off in same # of timesteps')
        #print('Timesteps: ',n)
        #print('Weights: ',w)
        tot_all = tot_all - leftover

    return tot_all, tot_ts, all_w, all_ntsteps
            

def partition_permutations(number):
    """ Compute the permutations of the partitions of the input number.
    """
    answer = set()
    answer.add((number, ))
    for x in range(1, number):
        for y in partition(number - x):
            answer.add((x, ) + y)
    return answer
    
def partition(number):
    """ Compute the of the partitions of the input number.
    """
    answer = set()
    answer.add((number, ))
    for x in range(1, number):
        for y in partition(number - x):
            answer.add(tuple(sorted((x, ) + y)))
    return answer    

    
def gradient_descent_algo2(L0, I, p, a, n, m):
    """ This algorithm finds the m lowest costs produced by running weights
        created using combinatorics and permutations to test the full range
        of possibilities.
    """
    
    # DESCRIPTION:
    # This algorithm 
    
    # INPUTS:
    # L0        -> The initial principal loan amount [numpy 1D array]
    # I         -> The interest [numpy 1D array]
    # p         -> The minimum payment amounts [numpy 1D array]
    # a         -> extra amount over the minimum payments willing to be paid [scalar]
    # n         -> defines the resolution of the combinatorics
    # m         -> the m lowest total cost combinations will be returned
    
    # OUTPUTS:
    # w                -> the weights resulting in the m lowest total costs [numpy array]
    # n_pay            -> the resultant number of payments made for each 
    #                     loan, corrresponding to w [numpy array]
    # grand_total_paid -> the resultant grand totals paid, corresponding to w [numpy array]    
    
    # Google: partitions, compositions, number theory, combinatorics
    
    nL = L0.shape[0]
    
    partitions = list(partition(n))
    # pared_partitions will be a list of tuples. Each tuple will be a set
    # of no more than nL numbers that add up to n. This set should include
    # every possible combo of nL (or less) numbers that sums to n.
    pared_partitions = list(filter(lambda x: len(x) <= nL, partitions))
    samp_arr = np.zeros(nL,dtype=np.float64)
    
    m_lowest_costs = []
    n_of_low_costs = []
    tup_of_low_costs = []
    
    for pt in pared_partitions:
        samp_arr[:] = 0.0
        partlen = len(pt)
        samp_arr[:partlen] = np.array(pt)
        all_vals_eq = (samp_arr[1:] == samp_arr[:-1]).sum() == (nL-1)
        # At least get rid of the repeats in cases where every value is equal
        if all_vals_eq:
            permu_tup_list = [tuple(samp_arr)]
        else:
            permu_tup_list = list(perm(samp_arr))
        for tup in permu_tup_list:
            i = 0
            tot_cost = 0.0
            n_pay_list = []
            for val in tup:
                w = float(val)/float(n)
                pmod = p[i]+w*a
                n_pay = compute_n_payments(L0[i], I[i], pmod)
                total = n_pay * pmod
                tot_cost = tot_cost + total
                n_pay_list.append(n_pay)
                i += 1
            # Keep m lowest values in m_lowest_costs list.
            if len(m_lowest_costs) >= m:
                list_max = max(m_lowest_costs)
                if tot_cost < list_max:
                    max_indx = m_lowest_costs.index(list_max)
                    m_lowest_costs[max_indx] = tot_cost
                    n_of_low_costs[max_indx] = n_pay_list
                    tup_of_low_costs[max_indx] = tup
                    #print(tot_cost)
                    #print(m_lowest_costs)
                    #print(n_of_low_costs)
                    #print(tup_of_low_costs)
                    #pdb.set_trace()
            else:
                m_lowest_costs.append(tot_cost)
                n_of_low_costs.append(n_pay_list)
                tup_of_low_costs.append(tup)
            if i < nL:
                pdb.set_trace()
            
    w = np.array(tup_of_low_costs,dtype=np.float64)
    w = w / float(n)
    n_pay = np.array(n_of_low_costs)
    grand_total_paid = np.array(m_lowest_costs)       
    return w, n_pay, grand_total_paid
    
    
    
    
    
def brute_force_minimizer(L0, I, p, a, set_sum, min_cost):
    """ This function will try nearly all combinations of amount 
        apportionments and return the combination that minimizes the
        total cost over the lifetime of all annuities (loans).
    """
    
    cost = []
    
    for i in range(0,set_sum+1):
        for j in range(0,set_sum+1):
            for k in range(0,set_sum+1):
                if (i+j+k) == set_sum:
                    ifl = float(i)/set_sum
                    jfl = float(j)/set_sum
                    kfl = float(k)/set_sum
                    pmod0 = p[0]+ifl*a
                    pmod1 = p[1]+jfl*a
                    pmod2 = p[2]+kfl*a
                    n0 = compute_n_payments(L0[0], I[0], pmod0)
                    n1 = compute_n_payments(L0[1], I[1], pmod1)
                    n2 = compute_n_payments(L0[2], I[2], pmod2)
                    total_spent = pmod0*n0 + pmod1*n1 + pmod2*n2
                    cost.append(total_spent)
                    if total_spent < min_cost:
                        isave = i
                        jsave = j
                        ksave = k
                        n0save = n0
                        n1save = n1
                        n2save = n2
                        min_cost = total_spent
    
    iportion = (isave/set_sum)*a
    jportion = (jsave/set_sum)*a
    kportion = (ksave/set_sum)*a
    
    ans_list = [iportion, jportion, kportion, n0, n1, n2]
    
    return np.asarray(cost), min_cost, ans_list
    
        
