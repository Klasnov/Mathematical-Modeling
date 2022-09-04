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
   其中，kind 参数可以选取 nearest(最邻近插值)、zero(0阶插值)、linear(线性插值)、quadratic(二次插值)、cubic(三次插值)或更高阶直接用数字
'''

from scipy.interpolate import interp1d
x = np.linspace(0, 10, 20)
y = 3 * x * x + x - 3
f = interp1d(x, y)
exp = f(3)
