# Description of test
- 10271580 scenarios were run. There were 3 loans per scenario.
- For each scenario, the total cost was computed using the 
"gradient descent" and "descending interest" methods.
- If the total cost using "gradient descent" was less than that of "descending
interest" then this was considered a "win"
- The scenarios were partitioned into 4 separate codes that could be run
simultaneously.
- A crude form a parallel processing.
- This was done out of laziness for not taking the time to actually learn
how to parallel process in Python.
