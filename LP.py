"""
线性规划使用scipy和PuLP两个库进行求解的代码笔记
作者：邵彦铭
时间：2022年9月3日
编译器：Python 3.9
"""

'''
scipy库，其使用方法如下：
    使用的函数为 scipy.optimize.linprog ()
    函数声明为 linprog(c, A_ub, b_ub, A_eq, b_eq, bounds)
    该函数用于求解目标函数 min z = c x
    在约束条件：
              A_ub x <= b_ub
              A_eq x == b_eq
              l <= x <= u
    其中，参数bounds是指决策变量的最小值和最大值
    各参数中，要求为一维数组的是c, b_ub, b_eq，要求为二维数组的是A_ub, A_eq
'''

# 示例
# 求解 z = 2x1 + 3x2 - 5x3 的最大值
# 约束条件为：
#        x1 +  x2 + x3  = 7
#       2x1 - 5x2 + x3 >= 10
#        x1 + 3x2 + x3 <= 12
#           x1, x2, x3 >= 0

import scipy.optimize as op
import numpy as np

z_s = np.array([-2, -3, 5])
A_ub_s = np.array([[-2, 5, -1], [1, 3, 1]])
b_ub_s = np.array([-10, 12])
A_eq_s = np.array([[1, 1, 1]])
b_eq_s = np.array([7])
bounds = [0, None], [0, None], [0, None]
res_s = op.linprog(z_s, A_ub_s, b_ub_s, A_eq_s, b_eq_s, bounds)
print("目标函数最大值 max z = {}\n此时目标函数的决策变量值为 {}\n".format(-res_s.fun, res_s.x))


'''
PuLP库，其求解过程如下：
    1. pulp.LpProblem 建立优化问题
        其函数声明为: LpProblem(name, sense)
        name: 线性规划问题的名称
        sense: 求解求解最大值(LpMaximize)或最小值(Minimize)
    2. pulp.LpVariable 创建问题变量
        其函数声明为 LpVariable(name, lowBound, upBound, cat, e)
        name: 变量名称
        lowBound: 变量下界
        upBound: 变量上界
        cat: 变量类型，可以是LpInteger、LpBinary或LpContinuous
        e: 指明变量是否在目标函数和约束条件中存在，不存在为None，存在可以设置此参数
    3. 通过 += 向问题添加目标函数和约束，并调用调用 solve() 函数进行求解
'''
# 示例
# 求解 z = 2x1 + 3x2 - 5x3 的最大值
# 约束条件为：
#        x1 +  x2 + x3  = 7
#       2x1 - 5x2 + x3 >= 10
#        x1 + 3x2 + x3 <= 12
#           x1, x2, x3 >= 0，且为整数

from pulp import *

prob = LpProblem("max_z", LpMaximize)
x1 = LpVariable("x1", 0, None, LpInteger)
x2 = LpVariable("x2", 0, None, LpInteger)
x3 = LpVariable("x3", 0, None, LpInteger)
prob += 2 * x1 + 3 * x2 - 5 * x3
prob += x1 + x2 + x3 == 7
prob += 2 * x1 - 5 * x2 + x3 >= 10
prob += x1 + 3 * x2 + x3 <= 12
prob.solve()
print("目标函数最大值为 max z = {}".format(value(prob.objective)))
print("此时目标函数的决策变量的值为：")
for v in prob.variables():
    print("{}: {}".format(v.name, v.value()))
