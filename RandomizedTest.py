from EAA import GroverSearch
from Logger import Logger
from getRandomePrimeInteger import getRandomPrimeInteger
import sys
import time
from primes import primes

x = []
y = []
z = []


x1,x2,x3=[],[],[]
t = time.strftime("-%Y%m%d-%H%M%S", time.localtime())
filename = 'log'+t+'.txt'
log = Logger(filename)

file_x = 'data_for_pic_practical'
file_y = 'data_for_pic_theoretic'
file = 'instances'

sys.stdout = log
for m in primes:
    # if m >= 3:
    #     break
    # m = getRandomPrimeInteger([0, 10000])

    test = GroverSearch(N=1024 ** 4, M=m)
    test.setError(0.000000000001)
    # print(m)
    # print("Error:\t", test.error)
    #
    #
    test.moreGrover()
    # # x1.append(test.varied_angle)
    #
    print("=========================== method of more Grover iterations ===========================")
    print("iteration times:\t", test.total_iter_num)
    print("theoretical iteration times:\t", test.theory_iter)
    print("final potential:\t", test.potential_MG.evalf())
    print("final success probability:\t", test.succProb_MG.evalf())
    print("theoretical iteration:\t", test.theory_iter)
    print("=========================== method of adding qubits ===========================")
    test.addQubits()

    print("iteration times:\t", test.iter_AQ)
    print("final potential:\t", test.potential_AQ.evalf())
    print("final success probability:\t", test.succProb_AQ.evalf())
    # x.append(test.total_iter_num)
    # y.append(test.theory_iter)
    # z.append(test)

    # test = GroverSearch(1024 ** 2, 47)
    # test.setError(0.0000000000000001)
    # test.moreGrover()
    # x1 = test.varied_angle
    #
    # test = GroverSearch(1024 ** 2, 709)
    # test.setError(0.0000000000000001)
    # test.moreGrover()
    # x2=test.varied_angle
    #
    # test = GroverSearch(1024 ** 2, 9059)
    # test.setError(0.0000000000000001)
    # test.moreGrover()
    # x3=test.varied_angle



import matplotlib.pyplot as  plt
import pickle
# pickle.dump(x1,open('pic_c1','wb'))
# pickle.dump(x2,open('pic_c2','wb'))
# pickle.dump(x3,open('pic_c3','wb'))


