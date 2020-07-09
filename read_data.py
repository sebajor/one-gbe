import struct
import numpy as np
import matplotlib.pyplot as plt

f = file('data', 'r')

data = np.zeros([100,100])
for i in range(100):
    try:
        raw_data = f.read(100)
        dat = struct.unpack('>100B', raw_data)
        data[i,:] = dat
    except:
        print('issue at i=%i'%i)
        break


data = data.flatten()
plt.title('1Gbeth data')
plt.ylabel('read values')
plt.grid()
plt.plot(data)
plt.show()
