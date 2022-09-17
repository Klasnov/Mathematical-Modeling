import numpy as np
import matplotlib.pyplot as plt

def gph():
    plt.title('$x$ of the float and the vibrator')
    plt.plot(t, xMs, c='b', label="$x_{Float}$")
    plt.plot(t, xms, c='r', linestyle=':', label='$x_{Vibrator}$')
    plt.legend()
    plt.xlabel('$t$')
    plt.ylabel('$x$')
    plt.savefig('x_q1_image2.png')
    plt.show()

def load(fl) -> np.ndarray:
    rd = fl.readline()
    a = rd.split()
    a = np.array(a).astype(np.float64)
    return a

f = open("data/Q1Data2.txt", 'r')
tmTol = int(f.readline())
N = int(f.readline())
t = np.linspace(0, tmTol, N)

aMs = load(f)
vMs = load(f)
xMs = load(f)
ams = load(f)
vms = load(f)
xms = load(f)
fel = load(f)
fdp = load(f)


