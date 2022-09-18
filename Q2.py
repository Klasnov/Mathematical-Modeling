from Q1 import *
import numpy as np


prc = 20
fM = 4890
omg = 2.2143
M_cw = 167.8395
M_add = 1165.992

cycle = 2 * pi / omg
tmSlc = 0.01
tmTol = int(8 * cycle) + 1
N = int(tmTol / tmSlc)

shl = shell(tmSlc, M_cw, M_add)
dis = shl.d
spg = spring()
vbt = vibrator(shl, spg, dis, tmSlc)

class dmp_q2(damper):
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

def cal(s: shell, v: vibrator, sp: spring, dmp: damper, tm: int) -> list:
    rlt = list()
    s.calAcl(sp.getF(), dmp.getFDamp(), f_wave(tm * tmSlc, fM, omg))
    s.calVel()
    rlt.append(s.getVel())
    s.calDes()
    rlt.append(s.getDes())
    v.calAcl(sp.getF(), dmp.getFDamp())
    v.calVel()
    rlt.append(v.getVel())
    v.calDes()
    rlt.append(v.getDes())
    return rlt

def prb1():
    c_dp_min = 0
    c_dp_max = 100000
    c_dp_stp = 1000
    c_stp_n = int((c_dp_max - c_dp_min) / c_dp_stp)
    cs = np.linspace(c_dp_min, c_dp_max, c_stp_n)
    std = True
    ps = np.zeros([c_stp_n])
    ch = np.zeros([c_stp_n])
    for i in range(c_stp_n):
        dmp = dmp_q2(cs[i], std, tmSlc, 0.5)
        flag = false
        for j in range(N):
            print("### 系数编号%d/%d，计算轮数%d/%d ###" % (i + 1, c_stp_n, j + 1, N))
            vM, xM, vm, xm = cal(shl, vbt, spg, dmp, j)
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
    for i in range(c_stp_n):
        if ch[i] == 0:
            cs_vld.append(cs[i])
            ps_vld.append(ps[i])
    n = len(cs_vld)
    cs_vld = np.asarray(cs_vld)
    ps_vld = np.asarray(ps_vld)

    f = open("data/Q2Data1_rgh.txt", 'w')
    f.write(str(n))
    f.write('\n')
    wrtFil(f, cs_vld)
    wrtFil(f, ps_vld)
    f.close()

def prb2():
    c_dp_min = 0
    c_dp_max = 100000
    c_stp_n = 15

    e_dp_min = 0
    e_dp_max = 1
    e_stp_n = 15

    cs = np.linspace(c_dp_min, c_dp_max, c_stp_n)
    es = np.linspace(e_dp_min, e_dp_max, e_stp_n)
    std = False
    ps = np.zeros([c_stp_n, e_stp_n])
    ch = np.zeros([c_stp_n, e_stp_n])
    for i in range(c_stp_n):
        for j in range(e_stp_n):
            dmp = dmp_q2(cs[i], std, tmSlc, es[j])
            flag = false
            for k in range(N):
                print("### 系数编号%d/%d，幂指编号%d/%d，计算轮数%d/%d ###" % (i + 1, c_stp_n, j + 1, e_stp_n, k + 1, N))
                vM, xM, vm, xm = cal(shl, vbt, spg, dmp, k)
                spg.calF(xM, xm, dis)
                if spg.x <= 0 or spg.x >= 3:
                    ch[i, j] = 1
                    flag = true
                    break
                dmp.calFDamp(vM, vm)
                dmp.calPow(vM, vm)
                dmp.calWrk()
            if flag:
                continue
            dmp.calPAve()
            ps[i, j] = dmp.getPAve()
    f = open("data/Q2Data2_rgh.txt", 'w')
    f.write(str(c_stp_n))
    f.write('\n')
    f.write(str(e_stp_n))
    f.write('\n')
    wrtFil(f, cs)
    wrtFil(f, es)
    f.write('\n')
    for i in range(len(cs)):
        wrtFil(f, ps[i])
    f.close()

prb2()
