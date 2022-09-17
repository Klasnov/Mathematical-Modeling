import matplotlib.pyplot as plt
import numpy as np

from Q1 import *

prc = 10
fM = 4890
omg = 2.2143
M_cw = 167.8395
M_add = 1165.992

cycle = 2 * pi / omg
tmSlc = 0.1
tmTol = int(10 * cycle) + 1
N = int(tmTol / tmSlc)

c_dp_min = 0
c_dp_max = 100000
c_dp_stp = 1000
stp_n = int((c_dp_max - c_dp_min) / c_dp_stp)

e_dp_min = 0
e_dp_

class dmp_q2_1(damper):
    t_delta = 0
    p = 0
    w = 0
    e = 0
    p_ave = 0

    def __init__(self, c, isStd, tm, e):
        super().__init__(c, isStd)
        self.t_delta = tm
        self.e = e

    def calFDamp(self, v_M, v_m):
        v_dif = v_M - v_m
        if self.std:
            self.f = round(self.c * v_dif, prc)
        else:
            self.f = round(self.c * pow(abs(v_dif), self.e) * v_dif, prc)

    # 计算瞬时功率
    def calPow(self, v_M, v_m):
        self.p = round(self.c * (v_M - v_m) * (v_M - v_m) / 2, prc)

    # 计算瞬时做功
    def calWrk(self):
        self.w = round(self.w + self.p * self.t_delta, prc)

    # 计算平均功率
    def calPAve(self):
        self.p_ave = round(self.w / tmTol, prc)

    # 获取平均功率
    def getPAve(self):
        return self.p_ave

shl = shell(tmSlc, M_cw, M_add)
dis = shl.d
spg = spring()
vbt = vibrator(shl, spg, dis, tmSlc)

cs = np.linspace(c_dp_min, c_dp_max, stp_n)
std = True
ps = np.zeros([stp_n])
ch = np.zeros([stp_n])

def prb1():
    for i in range(stp_n):
        dmp = dmp_q2_1(cs[i], std, tmSlc, 0.5)
        flag = false
        for j in range(N):
            print("### 系数编号%d/%d，计算轮数%d/%d ###" % (i + 1, stp_n, j + 1, N))
            shl.calAcl(spg.getF(), dmp.getFDamp(), f_wave(j * tmSlc, fM, omg))
            shl.calVel()
            vM = shl.getVel()
            shl.calDes()
            xM = shl.getDes()
            vbt.calAcl(spg.getF(), dmp.getFDamp())
            vbt.calVel()
            vm = vbt.getVel()
            vbt.calDes()
            xm = vbt.getDes()
            spg.calF(xM, xm, dis)
            if spg.x <= 0 or spg.x >= 3:
                ch[i] = 1
                flag = true
                break
            dmp.calFDamp(vM, vm)
            dmp.calPow(vM, vm)
            dmp.calWrk()
        if flag:
            continue
        dmp.calPAve()
        ps[i] = dmp.getPAve()
    cs_vld = list()
    ps_vld = list()
    for i in range(stp_n):
        if ch[i] == 0:
            cs_vld.append(cs[i])
            ps_vld.append(ps[i])
    n = len(cs_vld)
    cs_vld = np.asarray(cs_vld)
    ps_vld = np.asarray(ps_vld)

    f = open("Q2Data1_stp1000.txt", 'w')
    f.write(str(n))
    f.write('\n')
    wrtFil(f, cs_vld)
    wrtFil(f, ps_vld)
    f.close()


