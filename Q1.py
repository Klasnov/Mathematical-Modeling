"""
2022年数学建模A题第1问求解
作者：Klasnov
时间：2022年9月16日
"""
import io

from sympy import *
import matplotlib.pyplot as plt
import numpy as np

'''
全局量的定义
'''
rho = 1025
g = 9.8
t = Symbol('t')
prc = 25

'''
激励力的大小计算
'''
def f_wave(time):
    f_max = 6250
    omega = 1.4005
    fWv = round(f_max * cos(omega * time), prc)
    return fWv

'''
外壳类
'''
class shell:
    t_delta = 0
    m = 4866
    r = 1
    h_clid = 3
    h_cone = 0.8
    cw = 656.3616
    m_add = 1335.535
    d = 0
    x0 = 0
    x = 0
    v = 0
    a = 0

    # 初始化得到起始位置
    def __init__(self, timeSpace):
        # 变量定义
        V = Symbol('V')
        h = Symbol('h')
        self.t_delta = timeSpace
        # 排开液体体积的求解
        F = (rho * g * V) - (shell.m * g + vibrator.m * g)
        V = solve(F, V)[0]
        # 圆柱体浸泡在水中的深度
        fh = pi * self.r * self.r * self.h_cone / 3 + pi * self.r * self.r * h - V
        h = solve(fh, h)[0]
        # 求解浮子的质心位置
        l = sqrt(self.r ** 2 + self.h_cone ** 2)
        x = Symbol('x')
        fx = (2 * pi * self.r * self.h_clid * x) - (pi * l * self.r * (self.h_clid / 2 + self.h_cone / 4 - x))
        self.d = solve(fx, x)[0]
        # 计算浮子起始时刻的坐标
        self.x0 = self.h_clid / 2 - h - self.d
        self.x = self.x0

    # 获取圆柱重心与浮子重心的距离
    def getD(self):
        return self.d

    # 计算外壳所受的浮力大小
    def f_float(self):
        h_cld_hlf = self.h_clid / 2
        h_cne = self.h_cone
        d = self.d
        x = self.x
        if x <= h_cld_hlf - d:
            v = pi * h_cne / 3 + (h_cld_hlf - (x + d)) * pi
        else:
            v = pi * (h_cne - ((x + d) - h_cld_hlf)) / 3
        f_flt = round(rho * g * v, prc)
        return f_flt

    # 计算当前加速度
    def calAcl(self, f_elas, f_damp, f_wv):
        self.a = round((self.f_float() - self.m * g - f_elas - f_damp +
                        f_wv + (self.cw * self.v)) / (self.m + self.m_add), prc)

    # 获取当前的加速度
    def getAcl(self):
        return self.a

    # 计算当前速度
    def calVel(self):
        self.v = round(self.v + self.a * self.t_delta, prc)

    # 获取当前速度
    def getVel(self):
        return self.v

    # 计算当前位置
    def calDes(self):
        self.x = round(self.x + self.v * self.t_delta, prc)

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
    def calF(self, x_M, x_m, d):
        self.x = round((x_m - vibrator.h / 2) - ((x_M + d) - shell.h_cone / 2), prc)
        self.delta = round(self.l - self.x, prc)
        self.f = round(self.k * self.delta, prc)

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
        self.f = round(self.c * (v_M - v_m), prc)

    def getFDamp(self):
        return self.f

'''
振子类
'''
class vibrator:
    t_delta = 0
    m = 2433
    r = 0.5
    h = 0.5
    x0 = 0
    x = 0
    v = 0
    a = 0

    # 计算初始化位置
    def __init__(self, M: shell, s: spring, d, time):
        self.x0 = (M.x + d) - M.h_clid / 2 + s.x + self.h / 2
        self.t_delta = time

    # 计算当前加速度
    def calAcl(self, f_els, f_dmp):
        self.a = round((f_els + f_dmp - self.m * g) / self.m, prc)

    # 获取当前加速度
    def getAcl(self):
        return self.a

    # 计算当前速度
    def calVel(self):
        self.v = round(self.v + self.a * self.t_delta, prc)

    # 获取当前速度
    def getVel(self):
        return self.v

    # 计算当前位置
    def calDes(self):
        self.x = round(self.x + self.v * self.t_delta, prc)

    # 获取当前位置
    def getDes(self):
        return self.x

N = 10000
tmTol = 20

tmSlc = tmTol / N
shl = shell(tmSlc)
dis = shl.d
spg = spring()
vbt = vibrator(shl, spg, dis, tmSlc)
dmp = damper()

print("浮子的质心初始位置：%.5f" % shl.x0)
print("弹簧的初始长度：%.5f" % spg.x)
print("振子的质心初始位置：%.5f" % vbt.x0)

timeSlice = np.linspace(0, tmTol, N)
aMs = np.zeros([N])
vMs = np.zeros([N])
xMs = np.zeros([N])
ams = np.zeros([N])
vms = np.zeros([N])
xms = np.zeros([N])
fel = np.zeros([N])
fdp = np.zeros([N])

for i in range(N):
    print("\n第 %d 轮" % (i + 1))
    shl.calAcl(spg.getF(), dmp.getFDamp(), f_wave(i * tmSlc))
    aMs[i] = shl.getAcl()
    print("aMs[%d] = [%f]" % (i + 1, aMs[i]))
    shl.calVel()
    vMs[i] = shl.getVel()
    print("vMs[%d] = [%f]" % (i + 1, vMs[i]))
    shl.calDes()
    xMs[i] = shl.getDes()
    print("xMs[%d] = [%f]" % (i + 1, xMs[i]))

    vbt.calAcl(spg.getF(), dmp.getFDamp())
    ams[i] = vbt.getAcl()
    print("ams[%d] = [%f]" % (i + 1, ams[i]))
    vbt.calVel()
    vms[i] = vbt.getVel()
    print("vms[%d] = [%f]" % (i + 1, vms[i]))
    vbt.calDes()
    xms[i] = vbt.getDes()
    print("xms[%d] = [%f]" % (i + 1, xms[i]))

    spg.calF(xMs[i], xms[i], dis)
    fel[i] = spg.getF()
    print("fel[%d] = [%f]" % (i + 1, fel[i]))

    dmp.calFDamp(vMs[i], vms[i])
    fdp[i] = dmp.getFDamp()
    print("fdp[%d] = [%f]" % (i + 1, fdp[i]))

def wrtFil(fl, a: np.ndarray):
    temp = a.astype(str)
    for elm in temp:
        fl.write(elm + " ")
    fl.write('\n')

f = open("data", 'w')
wrtFil(f, aMs)
wrtFil(f, vMs)
wrtFil(f, xMs)
wrtFil(f, ams)
wrtFil(f, vms)
wrtFil(f, xms)
wrtFil(f, fel)
wrtFil(f, fdp)
f.close()

plt.scatter(timeSlice, xMs, marker='+')
plt.show()