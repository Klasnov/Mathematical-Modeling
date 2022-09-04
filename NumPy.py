"""
NumPy库的学习与使用笔记
作者：邵彦铭
时间：2022年9月3日
编译器：Python 3.9
"""

import numpy as np

'''
1. NumPy中最重要的是Ndarray对象，其类似于一种数组数据类型
   np.array()方法可以将列表直接转化为Ndarray对象
   np.asarray()方法也有一样的功能
'''
a = np.array([1, 2, 3, 4])
b = np.asarray([[1, 2, 3], [4, 5, 6]])

'''
2. 数组属性
'''
# shape属性 返回数组维度的元组
size = a.shape
# ndim属性 返回数组维数
dime = b.ndim

'''
3. 特殊数组的创建
'''
# 零矩阵，np.zeros(shape)
zero = np.zeros(5)
# 全1矩阵，np.ones(shape)
one = np.ones((2, 2))
# 单位矩阵，np.eye(n)
e = np.eye(3)
# 随机矩阵，np.random.rand(shape)，0 <= a < 1
rd = np.random.rand(3, 2)

'''
4. 通过数据范围创造数组
'''
# 给定范围内的等间隔值，调用 np.arange() 方法
# 函数声明为 arange(start, stop, step)，其生成向量包含 start 但是不包含 stop
x = np.arange(10, 20, 2)
# 给定范围内，规定数量的等间隔值，调用linspace()
# 函数声明为 linspace(start, stop, num, endpoint)
# endpoint可以指定是否包含stop值，默认为true
y = np.linspace(10, 20, 5)

'''
5. 数组操作
'''
# reshape()方法 调整数组的大小
b = b.reshape(3, 2)
# transpose()方法 转置矩阵
b_T = b.transpose()
# np.ravel() 将多维数组数组
# 函数声明为 ravel(a, order)
# order 参数可为 'C'(按行)、'F'(按列)、'A'(原顺序)
b_rv = np.ravel(b)
# np.sort() 将数组进行排序，默认使用快速排序
b_st = np.sort(b)
# np.nonzero() 返回数组中非零元素的索引
index = np.nonzero(a)
print(a[index])
# np.where() 返回数组中符合条件的值的索引
index = np.where(a >= 3)
print(a[index])

'''
6. 统计函数
'''
# amin() 获取最小值
minNum = np.amin(b)
# amax() 获取最大值
maxNum = np.amax(b)
# median() 获取中位数
mid = np.median(b)
# mean() 获取算数平均数
ave = np.mean(b)
# average() 获取平均数，可以进行加权运算，但两个矩阵要求大小一致
wts = np.array([6, 5, 4, 3, 2, 1])
ave_wt = np.average(b_rv, weights=wts)
# std() 获取标准差
std = np.std(b)
# var() 获取方差
var = np.var(b)

'''
7. 线性代数运算
'''
# 两个矩阵的点积，np.dot(a, b)
a = np.arange(6).reshape(2, 3)
b = np.asarray([1, 2, 3]).reshape(3, 1)
mul = np.dot(a, b)
# 矩阵行列式的值，np.linalg.det(a)
a = np.eye(3)
delt = np.linalg.det(a * 3)
# 线性方程组的解，np.linalg.solve()
A = np.asarray([1, 1, 1, 0, 2, 5, 2, 5, -1]).reshape(3, 3)
b = np.asarray([6, -4, 27])
root = np.linalg.solve(A, b)
# 矩阵的逆矩阵，np.linalg.inv()
A_inv = np.linalg.inv(A)
