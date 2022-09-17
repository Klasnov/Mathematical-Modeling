import numpy as np
import matplotlib.pyplot as plt

f = open("Q1Data", 'r')
t = np.linspace(0, 100, 1000)

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

plt.plot(t, xMs, 'b', label="$x_{浮子}$")
plt.plot(t, xms, 'r--', label='$x_{振子}$')
plt.xlabel('$t$')
plt.ylabel('$x$')
plt.savefig('x_image.png')
plt.show()
