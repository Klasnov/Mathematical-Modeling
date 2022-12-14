from sympy import *
import numpy as np


rho = 1025
g = 9.8

fM = 6250
omg = 1.4005
M_cw = 656.3616
M_add = 1335.535

c_dmp = 10000
dmp_isStd = True

cycle = 2 * pi / omg
tmSlc = 0.1
tmTol = int(40 * cycle) + 1
N = int(tmTol / tmSlc)

t = Symbol('t')
prc = 20

f_name = "data/Data_test.txt"

def f_wave(time, f_max, omega):
    fWv = round(f_max * cos(omega * time), prc)
    return fWv

def wrtFil(fl, a: np.ndarray):
    temp = a.astype(str)
    for elm in temp:
        fl.write(elm + " ")
    fl.write('\n')

class shell:
    t_delta = 0
    m = 4866
    r = 1
    h_clid = 3
    h_cone = 0.8
    cw = 0
    m_add = 0
    d = 0
    x0 = 0
    x = 0
    v = 0
    a = 0

    def __init__(self, timeSpace, cw, add):
        self.cw = cw
        self.m_add = add
        V = Symbol('V')
        h = Symbol('h')
        self.t_delta = timeSpace
        F = (rho * g * V) - (shell.m * g + vibrator.m * g)
        V = solve(F, V)[0]
        fh = (pi * self.h_cone / 3 + pi * h) - V
        h = solve(fh, h)[0]
        l = sqrt(self.r ** 2 + self.h_cone ** 2)
        x = Symbol('x')
        fx = (2 * pi * self.h_clid * x) - (pi * l * self.r * (self.h_clid / 2 + self.h_cone / 4 - x))
        self.d = solve(fx, x)[0]
        self.x0 = self.h_clid / 2 - h - self.d
        self.x = self.x0

    def getD(self):
        return self.d

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

    def calAcl(self, f_elas, f_damp, f_wv):
        if (self.x + self.d) - (self.h_clid / 2 + self.h_cone) < 0 and (self.x + self.d) + self.h_clid / 2 > 0:
            self.a = round((self.f_float() - self.m * g - f_elas - f_damp +
                            f_wv - (self.cw * self.v)) / (self.m + self.m_add), prc)
        else:
            self.a = round((self.f_float() - self.m * g - f_elas - f_damp
                            - (self.cw * self.v)) / (self.m + self.m_add), prc)

    def getAcl(self):
        return self.a

    def calVel(self):
        self.v = round(self.v + self.a * self.t_delta, prc)

    def getVel(self):
        return self.v

    def calDes(self):
        self.x = round(self.x + self.v * self.t_delta, prc)

    def getDes(self):
        return self.x

class spring:
    k = 80000
    l = 0.5
    f = 0
    delta = 0
    x = 0

    def __init__(self):
        delta = Symbol("delta")
        f_elas = self.k * delta - vibrator.m * g
        self.delta = solve(f_elas, delta)[0]
        self.f = self.delta * self.k
        self.x = self.l - self.delta

    def calF(self, x_M, x_m, d):
        self.x = round((x_m - vibrator.h / 2) - ((x_M + d) - shell.h_clid / 2), prc)
        self.delta = round(self.l - self.x, prc)
        self.f = round(self.k * self.delta, prc)

    def getF(self):
        return self.f

    def getDelta(self):
        return self.delta

    def getLen(self):
        return self.x

class damper:
    c = 0
    f = 0
    w = 0
    std = True

    def __init__(self, c, isStd):
        self.c = c
        self.std = isStd

    def calFDamp(self, v_M, v_m):
        v_dif = v_M - v_m
        if self.std:
            self.f = round(self.c * v_dif, prc)
        else:
            self.f = round(self.c * sqrt(abs(v_dif)) * v_dif, prc)

    def getFDamp(self):
        return self.f

class vibrator:
    t_delta = 0
    m = 2433
    r = 0.5
    h = 0.5
    x0 = 0
    x = 0
    v = 0
    a = 0

    def __init__(self, M: shell, s: spring, d, time):
        self.x0 = (M.x + d) - M.h_clid / 2 + s.x + self.h / 2
        self.t_delta = time
        self.x = self.x0

    def calAcl(self, f_els, f_dmp):
        self.a = round((f_els + f_dmp - self.m * g) / self.m, prc)

    def getAcl(self):
        return self.a

    def calVel(self):
        self.v = round(self.v + self.a * self.t_delta, prc)

    def getVel(self):
        return self.v

    def calDes(self):
        self.x = round(self.x + self.v * self.t_delta, prc)

    def getDes(self):
        return self.x

def run():
    shl = shell(tmSlc, M_cw, M_add)
    dis = shl.d
    spg = spring()
    vbt = vibrator(shl, spg, dis, tmSlc)
    dmp = damper(c_dmp, dmp_isStd)

    aMs = np.zeros([N])
    vMs = np.zeros([N])
    xMs = np.zeros([N])
    ams = np.zeros([N])
    vms = np.zeros([N])
    xms = np.zeros([N])
    fel = np.zeros([N])
    fdp = np.zeros([N])
    tms = []

    for i in range(N):
        print("### ?????????%d?????????????????????????????????%d??? ###" % (N, i + 1))
        tms.append(i * tmSlc)
        shl.calAcl(spg.getF(), dmp.getFDamp(), f_wave(i * tmSlc, fM, omg))
        aMs[i] = shl.getAcl()
        shl.calVel()
        vMs[i] = shl.getVel()
        shl.calDes()
        xMs[i] = shl.getDes()

        vbt.calAcl(spg.getF(), dmp.getFDamp())
        ams[i] = vbt.getAcl()
        vbt.calVel()
        vms[i] = vbt.getVel()
        vbt.calDes()
        xms[i] = vbt.getDes()

        spg.calF(xMs[i], xms[i], dis)
        fel[i] = spg.getF()

        dmp.calFDamp(vMs[i], vms[i])
        fdp[i] = dmp.getFDamp()

    f = open(f_name, 'w')
    f.write(str(tmTol) + '\n')
    f.write(str(N) + '\n')
    tms = np.array(tms)
    wrtFil(f, tms)
    wrtFil(f, aMs)
    wrtFil(f, vMs)
    wrtFil(f, xMs)
    wrtFil(f, ams)
    wrtFil(f, vms)
    wrtFil(f, xms)
    wrtFil(f, fel)
    wrtFil(f, fdp)
    f.close()

# run()