import numpy as np
import matplotlib.pylab as plt

f=open("C:\Users\JPL\Desktop\deploy_coned\boutput.dat","rb")
byte = f.read()
f.close()
 

y=np.frombuffer(byte, np.uint8)

plt.figure(1)
plt.plot(y)
plt.show()