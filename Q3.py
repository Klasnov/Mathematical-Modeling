from Q1 import *
import math

f_h = 3640
f_p = 1690
omg = 1.7152
M_add = 3640
k_vil = 80000
k_rad = 250000
zeta_h = 683.4558
zeta_p = 654.3383

c_dmp = 10000
dmp_isStd = True

cycle = 2 * pi / omg
tmSlc = 0.001
tmTol = int(40 * cycle) + 1
N = int(tmTol / tmSlc)

t = Symbol('t')
prc = 20

def getBetaAndC(l, d, epsilon) -> list:
    c = ((d - abs(math.cos(epsilon)) * l) ** 2 + (math.sin(epsilon) * l) ** 2) ** 0.5
    if epsilon >= 0:
        bt = math.degrees(math.acos((l * l - d * d - c * c) / (-2 * d * c))) - 90
    else:
        bt = 90 - math.degrees(math.acos((l * l - d * d - c * c) / (-2 * d * c)))
    return [bt, c]

class shl_shake(shell):
    delta = 0
    delta_d = 0
    delta_dd = 0
    w = 0
    z = 0
    z_d = 0
    z_dd = 0
    fz = 0
    M = 0

    def __init__(self, timeSpace, cw, add):
        super().__init__(timeSpace, cw, add)
        self.z = self.x0
        self.x = 0
        self.d = (self.h_clid / 2) - self.d

    def cal_fz(self, f_wv_h):
        self.fz = round(f_wv_h + zeta_h * self.z_d + self.f_float(), prc)

    def cal_M(self, f_wv_p):
        self.M = round(f_wv_p + zeta_p * self.delta_d + k_vil * self.delta_dd, prc)

    def cal_zdd(self, m_fx, m_fz, epsilon):
        self.z_dd = round((m_fx * sin(self.delta + epsilon) - m_fz * cos(self.delta + epsilon) + self.fz
                           - self.M * g) / self.M, prc)

    def cal_zd(self):
        self.z_d = round(self.z_d + self.z_dd * self.t_delta, prc)

    def cal_z(self):
        self.z = round(self.z + self.z_d * self.t_delta, prc)

    def cal_deltaDd(self, m_fx, m_d, J_add, epsilon):
        self.delta_dd = round((m_fx * m_d * cos(epsilon) + k_rad * epsilon + self.M) / J_add, prc)

    def cal_deltaD(self):
        self.delta_d = round(self.delta_d + self.delta_dd * self.t_delta, prc)

    def cal_delta(self):
        self.delta = round(self.delta + self.delta_d * self.t_delta, prc)

class vbt_shake(vibrator):
    l = 0
    I = 0
    a_px = 0
    a_pz = 0
    c = 0
    beta = 0
    epsilon = 0
    epsilon_d = 0
    epsilon_dd = 0
    vz = 0
    fx = 0
    fz = 0

    def __init__(self, M: shell, s: spring, d, time):
        super().__init__(M, s, d, time)
        self.c = self.x - M.x

    def updateCAndBeta(self, cAndBetaList):
        self.beta = cAndBetaList[0]
        self.c = cAndBetaList[1]

    def cal_apx(self, c, delta, delta_dd, x_dd, z_dd, bt):
        self.beta = bt
        self.a_px = round(x_dd * cos(delta + self.epsilon) - z_dd * sin(delta + self.epsilon) + c * delta_dd *
                          cos(self.beta) + self.l * self.epsilon, 10)

    def cal_apz(self, x_dd, delta, delta_dd, z_dd, f_els, f_dmp):
        self.a_pz = round(x_dd * sin(delta + self.epsilon) + z_dd * sin(delta + self.epsilon) +
                          self.c * delta_dd * (sin(self.beta) - cos(self.beta)) -
                          self.l * self.epsilon_dd + f_els / self.m + f_dmp / self.m, prc)

    def cal_fx(self, delta):
        self.fx = round(self.m * g * sin(delta + self.epsilon) - self.m * self.a_px, prc)

    def cal_fz(self, delta):
        self.fz = round(self.m * g * cos(delta + self.epsilon) + self.m * self.a_pz, prc)

    def cal_epsilonDd(self, delta_dd):
        self.epsilon_dd = round((-self.fx * self.l - k_rad * self.epsilon) / I - delta_dd, prc)

    def cal_epsilonD(self):
        self.epsilon_d = round(self.epsilon_d + self.epsilon_dd * self.t_delta, prc)

    def cal_epsilon(self):
        self.epsilon = round(self.epsilon + self.epsilon_d * self.t_delta, prc)

    def calWp(self):
        self.vz = round(self.vz + self.a_pz * self.t_delta, prc)

    def calL(self):
        self.l = round(self.l + self.vz * self.t_delta, prc)

def run():
    shl = shl_shake(tmSlc, zeta_h, M_add)
    dis = shl.d
    spg = spring()
    vbt = vbt_shake(shl, spg, dis, tmSlc)
    dmp = damper(c_dmp, dmp_isStd)
    print(shl.x0)
    print(vbt.x)

run()
