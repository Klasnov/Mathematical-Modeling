import numpy as np
import matplotlib.pyplot as plt

def gph():
    plt.title('$a$ of the float and the vibrator')
    plt.plot(t, aMs, c='b', label="$a_{Float}$")
    plt.plot(t, ams, c='r', linestyle=':', label='$a_{Vibrator}$')
    plt.legend()
    plt.xlabel('$t$')
    plt.ylabel('$a$')
    plt.savefig('a_q1_image2.png')
    plt.show()

def load(fl) -> np.ndarray:
    rd = fl.readline()
    a = rd.split()
    a = np.array(a).astype(np.float64)
    return a

f = open("Q1Data2.txt", 'r')
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

gph()
