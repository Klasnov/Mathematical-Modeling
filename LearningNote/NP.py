"""
非线性规划使用拉格朗日乘数法和scipy库进行求解的代码笔记
作者：邵彦铭
时间：2022年9月4日
编译器：Python 3.9
"""

'''
拉格朗日乘数法，运用sympy包进行求导和方程组的求解
'''
# f(x) = 60 - 10 * x1 - 4 * x2 + x1 ** 2 + x2 ** 2 - x1 * x2
# 等式约束为 x1 + x2 - 8 = 0

from sympy import *
x1 = Symbol('x1')
x2 = Symbol('x2')
alpha = Symbol('alpha')
# 构造拉格朗日函数
L = 60 - 10 * x1 - 4 * x2 + x1 * x1 + x2 * x2 - x1 * x2 - alpha * (x1 + x2 - 8)
diffyL_x1 = diff(L, x1)
diffyL_x2 = diff(L, x2)
diffyL_alpha = diff(L, alpha)
result_L = solve([diffyL_x1, diffyL_x2, diffyL_alpha], [x1, x2, alpha])

'''
spicy库，其使用方法如下：
    使用的函数为 scipy.optimize.minimize()
'''
from scipy.optimize import minimize
import numpy as np

def Obj(x):
    return 60 - 10 * x[0] - 4 * x[1] + x[0] * x[0] + x[1] * x[1] - x[0] * x[1]

def Cons1(x):
    return x[0] + x[1] - 8

# 如果是不等式约束条件，将type修改为ineq即可
cons1 = {'type': 'eq', 'fun': Cons1}
cons = cons1
x0 = np.asarray([2.0, 1.0])
res = minimize(Obj, x0, constraints=cons)
print(res.fun)
print(res.x)
