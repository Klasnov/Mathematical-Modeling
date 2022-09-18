from Q1 import *
import math

prc = 20
f_h = 3640
f_p = 1690
omg = 1.7152
M_cw = 683.4558
M_add = 3640
k_vil = 80000
k_rad = 250000

zeta_h = 683.4558
zeta_p = 654.3383

delta = 0
delta_d = 0
delta_dd = 0
beta = 0


def getBetaAndC(l, d, Ipsilon) -> list:
    c = ((d - abs(math.cos(Ipsilon)) * l) ** 2 + (math.sin(Ipsilon) * l) ** 2) ** 0.5
    if Ipsilon >= 0:
        return [math.degrees(math.acos((l * l - d * d - c * c) / (-2 * d * c))) - 90, c]
    else:
        return [90 - math.degrees(math.acos((l * l - d * d - c * c) / (-2 * d * c))), c]

def chgAxl(x_dd, z_dd, m_c, m_l, f_els, f_dmp, m, M, v_M, f_wv_h, f_wv_p, f_flt, d, epsilon, epsilon_dd):
    aglAdd = round(delta + epsilon, prc)
    a_px = round(x_dd * cos(aglAdd) - z_dd * sin(aglAdd) + m_c * delta_dd * (cos(beta) + sin(beta)) + m_l * epsilon_dd,
                 prc)
    a_pz = round(x_dd * sin(aglAdd) + z_dd * sin(aglAdd) + m_c * delta_dd * (sin(beta) - cos(beta)) - m_l * epsilon_dd
                 + f_els / m + f_dmp / m, prc)
    f_x = round(m * g * sin(aglAdd) - m * a_px, prc)
    f_z = round(m * g * cos(aglAdd) + m * a_pz, prc)
    I_p = round((-f_x * m_l - k_rad * epsilon) / (delta_dd + epsilon_dd), prc)
    f_wz = round(f_wv_h + zeta_h * v_M + f_flt, prc)
    M_wy = round(f_wv_p + zeta_p * delta_d + k_vil * delta_dd, prc)
    z_dd = round((f_x * sin(aglAdd) - f_z * cos(aglAdd) + f_wz - M * g) / M, prc)
    J_add = round((-f_x * d * cos(epsilon) + k_rad * epsilon + M_wy) / delta_dd, prc)
    return [a_px, a_pz, f_x, f_z, I_p, f_wz, M_wy, z_dd, J_add]

class vib_shake(vibrator):
    l = 0
    a_px = 0
    a_pz = 0
    c = 0
    wx = 0
    epsilon = 0
    epsilon_d = 0
    epsilon_dd = 0
    vz = 0

    def __init__(self, M: shell, s: spring, d, time):
        super().__init__(M, s, d, time)
        self.c = self.x - M.x

    def setAPx(self, apx):
        self.a_px = apx

    def setAPz(self, apz):
        self.a_pz = apz

    def calWx(self):
        self.wx = round(self.wx + self.a_px * self.t_delta, prc)

    def calWp(self):
        self.vz = round(self.vz + self.a_pz * self.t_delta, prc)

    def calX(self):
        self.epsilon = round(self.epsilon + self.wx * self.t_delta, prc)

    def calL(self):
        self.l = round(self.l + self.vz * self.t_delta, prc)

