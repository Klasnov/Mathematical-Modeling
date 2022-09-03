"""
SymPy库的学习与使用笔记
作者：邵彦铭
时间：2022年9月3日
编译器：Python 3.9
"""

from sympy import *

'''
1. 表达式与表达式的求值
'''
# 定义表达式变量
x = Symbol('x')
y = Symbol('y')
fx = 5 * x + 4
z = x * x + y * y
# 使用evalf()函数向表达式传值
fx_result = fx.evalf(subs={x: 6})
z_result = z.evalf(subs={x: 3, y: 4})

'''
2. 函数方程的求解
'''
# 根的求解
fx = x * 3 + 9
fx_root = solve(fx, x)
# 根的变量关系式求解
fx = x * 3 + y * y
root_x_y = solve(fx, x, y)
# 方程组的求解
f1 = x + y - 3
f2 = x - y + 5
x_y = solve([f1, f2], [x, y])

'''
3. 大型求和
'''
# 大型求和的运算，例如计算Sigma 2n，n从1到100
n = Symbol('n')
f = 2 * n
s = summation(f, (n, 1, 100))
# 求解带有大型求和的方程，例如Sigma x（i从1到5） + 10 * x = 15
i = Symbol('i')
f = summation(x, (i, 1, 5)) + 10 * x - 15
x_result = solve(f, x)

'''
4. 求极限
'''
# 求极限使用limit()方法，其三个参数分别为函数、变量和趋向值
# 注意：使用sympy包中的sin函数，并且无穷大使用sympy.oo表示
f = (1 + 1 / x) ** x
lim = limit(f, x, oo)

'''
5. 函数求导
'''
# 使用diff()方法求导和求偏导，两个参数分别是函数和变量
f1 = 2 * x ** 4 + 3 * x + 6
f2 = 2 * x ** 2 + 3 * y ** 4 + 2 * y
f1_ = diff(f1, x)
f2_y = diff(f2, y)

'''
6. 求解积分
'''
# 比较难的积分用sympy算会罢工，可以使用scipy进行求解
# 定积分的求解
f = 2 * x
f_int = integrate(f, (x, 0, 1))
f_pri = integrate(f, x)

'''
8. 数学符号的补充
'''
# 虚数单位
i = I
# 自然对数
e = E
# 无穷大
infinity = oo
# 圆周率
p = pi
