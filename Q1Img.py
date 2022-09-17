import numpy as np
import matplotlib.pyplot as plt


f = open("Q1Data.txt", 'r')
tmTol = int(f.readline())
N = int(f.readline())
t = np.linspace(0, tmTol, N)

def load(fl) -> np.ndarray:
    rd = fl.readline()
    a = rd.split()
    a = np.array(a).astype(np.float64)
    return a

aMs = load(f)
vMs = load(f)
xMs = load(f)
ams = load(f)
vms = load(f)
xms = load(f)
fel = load(f)
fdp = load(f)

plt.title('$X$ of the float and the vibrator')
plt.plot(t, xMs, c='b', label="$x_{Float}$")
plt.plot(t, xms, c='r', linestyle=':', label='$x_{Vibrator}$')
plt.legend()
plt.xlabel('$t$')
plt.ylabel('$x$')
plt.savefig('x_image.png')
plt.show()
