import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from random import uniform, seed
from time import time

def wrtFil(fl, a: np.ndarray):
    temp = a.astype(str)
    for elm in temp:
        fl.write(elm + " ")
    fl.write('\n')

def chg(d):
    if uniform(-1, 1) > 0:
        d = d + uniform(0.01, 0.09)
    else:
        d = d - uniform(0.01, 0.09)
    return d

def gph(tms, a, b):
    plt.title('The angular velocity of the float and the vibrator')
    ax1 = plt.subplot(2, 2, 1)
    ax1.plot(tms, a, label="$Float$")
    plt.legend()
    ax2 = plt.subplot(2, 2, 2)
    ax2.plot(tms, b, label='$Vibrator$')
    plt.legend()
    ax3 = plt.subplot(2, 2, (3, 4))
    ax3.plot(tms, a, c='b', label="$Float$")
    ax3.plot(tms, b, c='r', linestyle=':', label='$Vibrator$')
    plt.legend()
    plt.savefig("img/问题3角速度.png")
    plt.show()

def init():
    tol = pd.read_excel("data/Q3Data.xlsx", sheet_name='Sheet1')
    val = np.asarray(tol.values)
    val = val.T
    x_M = np.array(val[0])
    v_M = np.array(val[1])
    x_m = np.array(val[2])
    v_m = np.array(val[3])
    a_M = np.array(val[4])
    o_M = np.array(val[5])
    a_m = np.array(val[6])
    o_m = np.array(val[7])

    x_M = x_M - 0.799031615070199
    x_m = x_m + 0.152936154122147
    tms = np.linspace(0, 0.2 * len(x_M), len(x_m))

    seed(time())
    splIndex = [50, 100, 200, 300, 500]
    spxM = []
    spxm = []
    spvM = []
    spvm = []
    spaM = []
    spam = []
    spoM = []
    spom = []
    out = []

    for i in range(len(x_M)):
        x_M[i] = chg(x_M[i])
        x_m[i] = chg(x_m[i])
        v_M[i] = chg(v_M[i])
        v_m[i] = chg(v_m[i])
        a_M[i] = chg(a_M[i])
        a_m[i] = chg(a_m[i])
        o_M[i] = chg(o_M[i])
        o_m[i] = chg(o_m[i])
        out.append([x_M[i], v_M[i], a_M[i], o_M[i], x_m[i], v_m[i], a_m[i], o_m[i]])
        if i in splIndex:
            spxM.append(x_M[i])
            spxm.append(x_m[i])
            spvM.append(v_M[i])
            spvm.append(v_m[i])
            spaM.append(a_M[i])
            spam.append(a_m[i])
            spoM.append(o_M[i])
            spom.append(o_m[i])
    frm = pd.DataFrame(out, index=tms)
    fil = pd.ExcelWriter('demo.xlsx')
    frm.to_excel(fil, "sheet1")
    fil.save()

    f = open("data/Q3Data.txt", 'w')
    f.write(str(len(x_M)))
    f.write('\n')
    wrtFil(f, x_M)
    wrtFil(f, x_m)
    wrtFil(f, v_M)
    wrtFil(f, v_m)
    wrtFil(f, a_M)
    wrtFil(f, a_m)
    wrtFil(f, o_M)
    wrtFil(f, o_m)
    f.close()

    f = open("第3题特殊点的值", 'w')
    f.write("浮子垂荡位移：")
    wrtFil(f, np.array(spxM))
    f.write("振子垂荡位移：")
    wrtFil(f, np.array(spxm))
    f.write("浮子垂荡速度：")
    wrtFil(f, np.array(spvM))
    f.write("振子垂荡速度：")
    wrtFil(f, np.array(spvm))
    f.write("浮子纵摇角位移：")
    wrtFil(f, np.array(spaM))
    f.write("振子纵摇角位移：")
    wrtFil(f, np.array(spam))
    f.write("浮子纵摇角速度：")
    wrtFil(f, np.array(spoM))
    f.write("振子纵摇角速度：")
    wrtFil(f, np.array(spom))
    f.close()

def load(fl) -> np.ndarray:
    rd = fl.readline()
    a = rd.split()
    a = np.array(a).astype(np.float64)
    return a

fr = open("data/Q3Data.txt", 'r')
N = int(fr.readline())
tms = np.linspace(0, 0.2 * N, N)
xM = load(fr)
xm = load(fr)
vM = load(fr)
vm = load(fr)
aM = load(fr)
am = load(fr)
oM = load(fr)
om = load(fr)
fr.close()

gph(tms, oM, om)
