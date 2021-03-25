import numpy as np
import matplotlib.pylab as plt

f=open("output","rb")
byte = f.read()
f.close()
 
print(byte)

y=np.frombuffer(byte, np.uint8)

plt.figure(1)
plt.plot(y)
plt.show()