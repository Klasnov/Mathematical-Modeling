import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def gph():
    plt.title('$x$ of the float and the vibrator')
    plt.plot(tms, xMs, c='b', label="$x_{Float}$")
    plt.plot(tms, xms, c='r', linestyle=':', label='$x_{Vibrator}$')
    plt.legend()
    plt.xlabel('$t$')
    plt.ylabel('$x$')
    plt.savefig("img/问题1第1问位移.png")
    plt.show()

def testDraw(tm, rf, name):
    plt.title("Change Trend of {}".format(name))
    plt.plot(tm, rf)
    plt.xlabel('$t$')
    plt.ylabel('$var$')
    plt.savefig("img/test/测试数集：{}".format(name))
    plt.show()

def valRcd():
    out = list()
    tm = list()
    splT = [10, 20, 40, 60, 100]
    spl_x_M = list()
    spl_x_m = list()
    spl_v_M = list()
    spl_v_m = list()
    for i in range(len(xMs)):
        if i % 2 == 0:
            out.append([xMs[i], xms[i], vMs[i], vms[i]])
            tm.append(0.1 * i)
            if 0.1 * i in splT:
                spl_x_M.append(str(xMs[i]))
                spl_x_m.append(str(xms[i]))
                spl_v_M.append(str(vMs[i]))
                spl_v_m.append(str(vms[i]))
    frm = pd.DataFrame(out, index=tm)
    fil = pd.ExcelWriter('demo.xlsx')
    frm.to_excel(fil, "sheet1")
    fil.save()

    fw = open("data/Q1Out2.text", 'w')
    wrtFil(fw, spl_x_M)
    wrtFil(fw, spl_x_m)
    wrtFil(fw, spl_v_M)
    wrtFil(fw, spl_v_m)
    fw.close()

def load(fl) -> np.ndarray:
    rd = fl.readline()
    a = rd.split()
    a = np.array(a).astype(np.float64)
    return a

def wrtFil(fl, a):
    for elm in a:
        fl.write(elm + ", ")
    fl.write('\n')

fr = open("data/Data_test.txt", 'r')
tmTol = int(fr.readline())
N = int(fr.readline())
tms = load(fr)
aMs = load(fr)
vMs = load(fr)
xMs = load(fr)
ams = load(fr)
vms = load(fr)
xms = load(fr)
fel = load(fr)
fdp = load(fr)
st = [aMs, vMs, xMs, ams, vms, xms, fel, fdp]
nm = ['a_M', 'v_M', 'x_M', 'a_m', 'v_m', 'x_m', 'f_elastic', 'f_damper']
for i in range(len(st)):
    testDraw(tms, st[i], nm[i])
