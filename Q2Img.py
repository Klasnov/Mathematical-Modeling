import numpy as np
import matplotlib.pyplot as plt

def load(fl) -> np.ndarray:
    rd = fl.readline()
    a = rd.split()
    a = np.array(a).astype(np.float64)
    return a

f = open('Q2Data1_stp1000.txt', 'r')
stp_n = int(f.readline())
cs = load(f)
ps = load(f)

plt.plot(cs[3:33], ps[3:33])
plt.show()
