import matplotlib.pyplot as plt
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

class dmp_q2_1(damper):
    t_delta = 0
    p = 0
    w = 0
    p_ave = 0

    def __init__(self, c, isStd, tm):
        super().__init__(c, isStd)
        self.t_delta = tm

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

for i in range(stp_n):
    dmp = dmp_q2_1(cs[i], std, tmSlc)
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
        xm = shl.getDes()
        spg.calF(xM, xm, dis)
        dmp.calFDamp(vM, vm)
        dmp.calPow(vM, vm)
        dmp.calWrk()
    dmp.calPAve()
    ps[i] = dmp.getPAve()

f = open("Q2Data1_stp1000.txt", 'w')
f.write(str(stp_n))
f.write('\n')
wrtFil(f, cs)
wrtFil(f, ps)
f.close()

plt.plot(cs, ps)
plt.show()
