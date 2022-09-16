"""
2022年数学建模A题第1问求解
作者：Klasnov
时间：2022年9月16日
"""

from sympy import *
import matplotlib.pyplot as plt
import numpy as np

'''
全局量的定义
'''
rho = 1025
g = 9.8
t = Symbol('t')

'''
激励力的大小计算
'''
def f_wave(time):
    f = 6250
    omega = 1.4005
    return f * cos(omega * time)

'''
外壳类
'''
class shell:
    m = 4866
    m_add = 1335.535
    r = 1
    h_clid = 3
    h_cone = 0.8
    Cw = 656.3616
    x0 = 0
    x = 0
    v = 0
    a = 0

    # 初始化得到起始位置
    def __init__(self):
        V = Symbol('V')
        h = Symbol('h')
        F = (rho * g * V) - (shell.m * g + vibrator.m * g)
        V = solve(F, V)[0]
        f = pi * self.r * self.r * self.h_cone / 3 + pi * self.r * self.r * h - V
        h = solve(f, h)[0]
        self.x0 = self.h_clid / 2 - h
        self.x = self.x0

    # 计算外壳所受的浮力大小
    def f_float(self):
        v = pi * self.r ** 2 * (self.h_clid / 2 - self.x) + pi * self.r ** 2 * self.h_cone / 3
        return rho * g * v

    # 计算当前加速度
    def calAcl(self, f_elas, f_damp, f_wv):
        self.a = (self.f_float() - self.m * g - f_elas - f_damp + f_wv + (self.Cw * self.v)) / (self.m + self.m_add)

    # 获取当前的加速度
    def getAcl(self):
        return self.a

    # 计算当前速度
    def calVel(self):
        self.v = integrate(self.a, t)

    # 获取当前速度
    def getVel(self):
        return self.v

    # 计算当前位置
    def calDes(self):
        self.x = self.x + integrate(self.v, t)

    # 获取当前位置
    def getDes(self):
        return self.x

'''
弹簧类
'''
class spring:
    k = 80000
    l = 0.5
    f = 0
    delta = 0
    x = 0

    # 计算弹簧初始长度
    def __init__(self):
        delta = Symbol("delta")
        f_elas = self.k * delta - vibrator.m * g
        self.delta = solve(f_elas, delta)[0]
        self.f = self.delta * self.k
        self.x = self.l - self.delta

    # 计算当前弹力
    def calF(self, x_M, x_m):
        self.x = (x_m - vibrator.h / 2) - (x_M - shell.h_cone / 2)
        self.delta = self.l - self.x
        self.f = self.k * self.delta

    # 获取当前弹力
    def getF(self):
        return self.f

    # 获取当前形变量
    def getDelta(self):
        return self.delta

    # 获取当前长度
    def getLen(self):
        return self.x

'''
阻尼器类
'''
class damper:
    c = 10000
    f = 0

    def calFDamp(self, v_M, v_m):
        self.f = 10000 * (v_M - v_m)

    def getFDamp(self):
        return self.f

'''
振子类
'''
class vibrator:
    m = 2433
    r = 0.5
    h = 0.5
    x0 = 0
    x = 0
    v = 0
    a = 0

    # 计算初始化位置
    def __init__(self, M: shell, s: spring):
        self.x0 = M.x - M.h_clid / 2 + s.x + self.h / 2

    # 计算当前加速度
    def calAcl(self, f_els, f_dmp):
        self.a = (f_els + f_dmp - self.m * g) / self.m

    # 获取当前加速度
    def getAcl(self):
        return self.a

    # 计算当前速度
    def calVel(self):
        self.v = integrate(self.a, t)

    # 获取当前速度
    def getVel(self):
        return self.v

    # 计算当前位置
    def calDes(self):
        self.x = self.x + integrate(self.v, t)

    # 获取当前位置
    def getDes(self):
        return self.x

def update(iShell: shell, iSpring: spring, iVibrator: vibrator, iDamper: damper, time: Symbol):
    iShell.calAcl(iSpring.getF(), iDamper.getFDamp(), f_wave(time))
    iShell.calVel()
    iShell.calDes()
    iVibrator.calAcl(iSpring.getF(), iDamper.getFDamp())
    iVibrator.calVel()
    iVibrator.calDes()
    iSpring.calF(iShell.getDes(), iVibrator.getDes())
    iDamper.calFDamp(iShell.getVel(), iVibrator.getVel())

shl = shell()
spg = spring()
vbt = vibrator(shl, spg)
dmp = damper()

print("浮子的质心初始位置：%.5f" % shl.x0)
print("弹簧的初始长度：%.5f" % spg.x)
print("振子的质心初始位置：%.5f\n" % vbt.x0)

update(shl, spg, vbt, dmp, t)

a = shl.getAcl()
a_value = a.evalf(subs={t: 0})
print("a_M =", a)
print(a_value)
'''print("v_M =", shl.getVel())
print("x_M =", shl.getDes())
print("a_m =", vbt.getAcl())
print("v_m =", vbt.getVel())
print("x_m =", vbt.getDes())
print("F_elastic =", spg.getF())
print("F_damper =", dmp.getFDamp())'''
