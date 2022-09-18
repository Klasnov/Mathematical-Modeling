import random
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from mpl_toolkits.mplot3d import Axes3D


def load(fl) -> np.ndarray:
    rd = fl.readline()
    a = rd.split()
    a = np.array(a).astype(np.float64)
    return a

def gph1():
    f = open('data/Q2Data1_prc.txt', 'r')
    f.readline()
    cs = load(f)
    ps = load(f)
    plt.title("Output Power Under Different Damping Coefficients")
    plt.scatter(cs, ps)
    plt.xlabel('$c$')
    plt.ylabel('$p$')
    plt.savefig("img/变动阻尼系数下精确输出功率.png")
    plt.show()

def gph2():
    f = open("data/Q2Data2.txt", 'r')
    n = int(f.readline())
    f.readline()
    cs = load(f)
    es = load(f)
    f.readline()
    ps = np.zeros([n, n])
    for i in range(n):
        ps[i] = load(f)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    plt.title("Output power of dampers\nwith different proportional coefficients and power exponents")
    cs, es = np.meshgrid(cs, es)
    cs, es = cs.ravel(), es.ravel()
    height = np.zeros_like(ps.flatten())
    width = depth = 0.3
    ax.bar3d(es, cs, height, width, depth, ps.flatten(), color='c', shade=False, alpha=0.3)
    ax.set_xlabel('n')
    ax.set_ylabel('c')
    ax.set_zlabel('Output Power')
    plt.savefig("img/阻尼器不同比例系数和幂指数下的输出功率.png")
    plt.show()

gph2()
