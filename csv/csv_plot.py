import numpy as np
import matplotlib.pyplot as plt

data=np.loadtxt(fname="data.csv", delimiter = ",")
x=data[:,0]
y=data[:,1]

plt.plot(x,y,color="red")

plt.xlabel("Time[s]", fontsize=18)
plt.ylabel("Output[rpm]", fontsize=18)
#plt.ylabel("speed [m/s]", fontsize=18)
plt.xlim(0,)
plt.ylim(0,70)
plt.subplots_adjust(bottom=0.15)
plt.tick_params(labelsize=15)
plt.grid()
plt.legend()
plt.show()