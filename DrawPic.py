import matplotlib.pyplot as plt
from sympy import sqrt
import numpy as np
import pickle
import math
#
# x = np.loadtxt(open('data_for_figure/data_for_pic_x3.txt','rb'))
# y = np.loadtxt(open('data_for_figure/data_for_pic_y3.txt','rb'))
# y = pickle.load(open('data_for_pic_x','rb'))
# x = pickle.load(open('data_for_pic_y','rb'))
x = pickle.load(open('data_for_figure/data_for_pic_x','rb'))
y = pickle.load(open('data_for_figure/data_for_pic_y','rb'))
print(len(x))



x = [math.log(item,sqrt(3)) for item in x]
y = [math.log(item,sqrt(2)) for item in y]


plt.xlabel(r"#iter. required for MQI ($\log_{\sqrt{2}})$", fontsize = 10)
plt.ylabel(r"#iter. required for MIP ($\log_{\sqrt{3}})$",fontsize = 10)


plt.scatter(y, x, s=1)
plt.ylim(np.min(x), np.max(x))
plt.xlim(np.min(y), np.max(y))
# plt.ylim(15,40,5)
# plt.xlim(15,40,5)
xlime = [i for i in range(41)]
line = [i for i in range(41)]
plt.plot(xlime,line,c='chocolate',linewidth=1)

plt.show()