# Loan_Payment_Optimizer

## Descripton:
Python code to determine how to allocate extra money to minimize the total cost paid on debt in the form of amortized loans.

## Brief explanation:

Let's say you have a bunch of debts. They are probably in the form of loans paid off
in installments over time. These are known as amortized loans.

Examples of amortized loans include student loans, mortgages, 
and credit card debts.

The mantra I've seen over and over again, is that the optimal way to pay
off these debts is something called the "higher rate" or "descending interest" 
method by which you pay off your debts by interest rate from highest to
lowest [1][2].

I wanted to test to see if the descending interest method was always optimal.
To test this hypothesis, I coded up a simple algorithm I call the "gradient
descent" method which I thought might be a worthy competitor. It operates on a 
set of loans by seeing which loan's total cost (the interest + principal you pay over life of the loan) is
reduced the most by applying a fixed amount of money over the fixed
minimum payment. You can read more about the function in its comments
within the _loan_function.py_ file.

I hypothesized that the "gradient descent" method would result in a lower total cost
paid in at least some scenarios, compared to the "descending interest" method.

I put the hypothesis to the test in two separate ways:  
_1_ - By running a bunch of debt scenarios through each of the algorithms.  
_2_ - By a simple total cost plot made varying only one loan parameter for a two-loan scenario.

The bottom line is the descending interest method is not always optimal,
although I do think it's a good rule of thumb.

To see the results of _1_, see README.md in the _loan_function_test_1_in4_
sub-directory.

The results of _2_ are shown below. Please look at the simple code
_method_compare_1.py_ to see how I made these plots.

![Method Compare](method_compare_1.png)

The figure above shows how the gradient descent method reduces the total cost 
paid over the life of two loans assuming the following...  
1. The annual interest of _Loan A_ is 35%.
2. The annual interest of _Loan B_ is 10%.
3. The term of both loans is 100 months.
4. The TOTAL amount of money applied above the minimum payments is $100. **The way this $100 is split between Loans A & B is what is determined by the gradient descent algorithm.** The descending interest algorithm ALWAYS applies the $100 to the loan with the higher interest rate until it's paid off.
5. The starting principal of _Loan A_ is $500.
6. The starting principal of _Loan B_ varies. It varies from being equal to _Loan A's_
starting principal to + $10000 greater.

The top plot in the figure compares the total cost of the two methods as a function
of the increases in _Loan B's_ starting principal. The bottom plot explicitly shows how much
money you would save using the same x-axis.

Granted, I picked a case where I knew the gradient descent method would win.
But the point is that the descending interest method is not always optimal
if you are trying to reduce your total cost paid.

If you look at the results of _1_, the many debt scenarios, you'll see that
the majority of the time the gradient descent outperforms the descending interest
method, and in cases where it does not, it doesn't "lose" by much.

## System requirements:
- Python 3.X
- No obscure Python libraries required. 

## References:
[1] https://www.khanacademy.org/college-careers-more/personal-finance/pf-interest-and-debt/debt-repayment/v/high-rate-vs-snowball-method</br>
[2] https://www.reddit.com/r/personalfinance/comments/zzoxu/calculator_to_optimize_loan_payoff/ {last accessed 9/9/20}

## Notes:

{17 Aug 2020}</br>
First draft complete.

{09 Sep 2020}</br>
Considering the time value of money is beyond the scope of this project. For example, it could sometimes be better to
put some extra money towards high-return investments rather than paying off some debts.
