from matplotlib import pyplot as plt
import numpy as np
import pickle
import math
import seaborn as sns
from matplotlib.ticker import MaxNLocator
plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))

file1 = pickle.load(open('data_for_figure/pic_a1','rb'))
file2 = pickle.load(open('data_for_figure/pic_a2','rb'))
file3 = pickle.load(open('data_for_figure/pic_a3','rb'))

line1 = []
line11 = []
for i in range(10):
    line1.append((file1[i+1]/file1[i]+file2[i+1]/file2[i]+file3[i+1]/file3[i])/3)
    if i >= 1:
        line11.append((file1[i+1]/file1[i-1]+file2[i+1]/file2[i-1]+file3[i+1]/file3[i-1])/3)
# print(line1)
# print(line11)

file4 = pickle.load(open('data_for_figure/pic_b1','rb'))
file5 = pickle.load(open('data_for_figure/pic_b2','rb'))
file6 = pickle.load(open('data_for_figure/pic_b3','rb'))

line2 = []
line21 = []
for i in range(10):
    line2.append((file4[i+1]/file4[i]+file5[i+1]/file5[i]+file6[i+1]/file6[i])/3)
    if i >= 1:
        line21.append((file4[i+1]/file4[i-1]+file5[i+1]/file5[i-1]+file6[i+1]/file6[i-1])/3)


file7 = pickle.load(open('data_for_figure/pic_c1','rb'))
file8 = pickle.load(open('data_for_figure/pic_c2','rb'))
file9 = pickle.load(open('data_for_figure/pic_c3','rb'))

line3 = []
line31 = []
for i in range(10):
    line3.append((file7[i+1]/file7[i]+file8[i+1]/file8[i]+file9[i+1]/file9[i])/3)
    if i >= 1:
        line31.append((file7[i+1]/file7[i-1]+file8[i+1]/file8[i-1]+file9[i+1]/file9[i-1])/3)

xlime = [i + 1 for i in range(10)]
xlime1 = [i + 2 for i in range(9)]
plt.ylabel("the ratios between the angles of two sectors", fontsize = 10)
print(len(line11),len(xlime1))
average1 = 0
for i in range(len(line1)):
    average1 = average1 + line1[i] + line2[i] + line3[i]
average1 = average1 / (len(line1)+len(line2)+len(line3))
average11 =0
for i in range(len(line11)):
    average11 = average11 + line11[i] + line21[i] + line31[i]
average11 = average11 / (len(line11)+len(line21)+len(line31))
print(average1,average11)

plt.plot(xlime,line1,c='cornflowerblue',linewidth=1,label=r'$N=2^{20}$',marker='^',markersize=3)
plt.plot(xlime1,line11,linestyle='-.',c='cornflowerblue',linewidth=1,label=r'$N=2^{20}$',marker='^',markersize=2)
plt.plot(xlime,line2,c='chocolate',linewidth=1,marker='o',label=r'$N=2^{30}$',markersize=3)
plt.plot(xlime1,line21,linestyle='-.',c='chocolate',linewidth=1,label=r'$N=2^{30}$',marker='o',markersize=2)
plt.plot(xlime,line3,c='burlywood',linewidth=1,marker='s',label=r'$N=2^{40}$',markersize=3)
plt.plot(xlime1,line31,linestyle='-.',c='burlywood',linewidth=1,label=r'$N=2^{40}$',marker='s',markersize=2)
plt.plot(np.arange(1, 11, 1), [0.5 for i in range(10)],c='r', linewidth=1, linestyle='--')
plt.plot(np.arange(1, 11, 1), [0 for i in range(10)],c='black', linewidth=1, linestyle='--')
plt.plot(np.arange(1, 11, 1), [average1 for i in range(10)],c='purple', alpha=0.4, linewidth=1, linestyle='-.')
plt.plot(np.arange(1, 11, 1), [average11 for i in range(10)],c='purple', alpha=0.4, linewidth=1, linestyle=':')

plt.legend()
plt.show()




