import numpy as np

#n = 2000 # number of time periods
#L0 = 17421.08 # initial loan amount (initial principal)
#L0save = L0
#P = L0
#I = 0.019/12.0 # periodic interest
#p = 304.59  # fixed periodic payment

# This case runs fine.
L0 = np.asarray([17421.08, 18000.00, 19900.00])
p = np.asarray([304.59, 321.67, 375.0])
I = np.asarray([0.019/12.0, 0.021/12.0, 0.025/12.0])
a = 390.74

# Need to fix algo1 for this case too
L0 = np.asarray([20000.08, 18000.08, 17000.08])
p = np.asarray([305.00, 305.00, 305.00])
I = np.asarray([0.021/12.0, 0.021/12.0, 0.021/12.0])
a = 390.74

# Case where algo1 is clear winner over "avalanche"
L0 = np.asarray([17421.08, 18000.00, 199900.00])
p = np.asarray([304.59, 321.67, 555.0])
I = np.asarray([0.019/12.0, 0.021/12.0, 0.025/12.0])
a = 390.74


# All principals the same. Interests vary.
L0 = np.asarray([17000.08, 17000.08, 17000.08])
p = np.asarray([305.00, 305.00, 305.00])
I = np.asarray([0.124/12.0, 0.023/12.0, 0.022/12.0])
a = 390.74

# All principals the same. Interests vary.
L0 = np.asarray([17000.08, 17000.08, 17000.08])
p = np.asarray([305.00, 305.00, 305.00])
I = np.asarray([0.024/12.0, 0.023/12.0, 0.022/12.0])
a = 390.74

# All principals the same. Interests vary.
L0 = np.asarray([17000.08, 17000.08, 17000.08])
p = np.asarray([305.00, 305.00, 305.00])
I = np.asarray([0.002      ,0.00191667 ,0.00183333])
a = 390.74

# Need to fix algo1 for this case since all loans get paid off @ once
L0 = np.asarray([17000.08, 17000.08, 17000.08])
p = np.asarray([305.00, 305.00, 305.00])
I = np.asarray([0.021/12.0, 0.021/12.0, 0.021/12.0])
a = 390.74
