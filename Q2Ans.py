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
    '''fig = plt.figure()
    ax = fig.gca(projection='3d')
    x, y = np.meshgrid(es, cs)
    X, Y = x.ravel(), y.ravel()
    height = np.zeros_like(ps.flatten())
    width = depth = 0.3
    color = plt.cm.Set2(random.choice(range(plt.cm.Set2.N)))
    c = ['r'] * len(ps)
    ax.bar3d(X, Y, height, width, depth, ps.flatten(), color=c, shade=False)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()'''
    mpl.rcParams['font.size'] = 10
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    z = 2011
    xs = range(1, 13)
    ys = 1000 * np.random.rand(12)
    color = plt.cm.Set2(random.choice(range(plt.cm.Set2.N)))
    ax.bar(xs, ys, zs=z, zdir='y', color=color, alpha=0.8)
    ax.xaxis.set_major_locator(mpl.ticker.FixedLocator(xs))
    ax.yaxis.set_major_locator(mpl.ticker.FixedLocator(ys))
    ax.set_xlabel('Month')
    ax.set_ylabel('Year')
    ax.set_zlabel('Sales Net [usd]')
    plt.show()

gph2()
