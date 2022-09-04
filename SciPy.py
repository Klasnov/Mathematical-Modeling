"""
SciPy库的学习与使用笔记
作者：邵彦铭
时间：2022年9月4日
编译器：Python 3.9
"""

import numpy as np

'''
1. 函数插值
   使用 scipy.interpolate 包中的 interp1d() 函数实现
   函数声明为 interp1d(x, y, kind)
   kind 参数可以选取 nearest(最邻近插值)、zero(0阶插值)、linear(线性插值)、quadratic(二次插值)、cubic(三次插值)或更高阶直接用数字表示
'''
from scipy.interpolate import interp1d
x = np.linspace(0, 10, 20)
y = 3 * x * x + x - 3
f = interp1d(x, y)
exp = f(3)

'''
2. 最小化函数
   使用 scipy.optimize 包中的 minimize() 函数实现
   函数声明为 minimize(fun, x0, args)
   fun 为要优化的函数，默认将第一个参数作为要优化的变量，x0 为进行迭代的初值，args 为优化函数剩余参数的值
'''
from scipy.optimize import minimize

def ObliqueThrow(theta, v0):
    g = 9.8
    rad = np.pi * theta / 180
    return 2 * v0 * v0 * np.sin(rad) * np.cos(rad) / g

def MinusOT(theta, v0):
    return - ObliqueThrow(theta, v0)

result = minimize(MinusOT, np.asarray(40), np.asarray(1))
print(result.x)
