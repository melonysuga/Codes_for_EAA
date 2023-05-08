from sympy import symbols, sqrt, Rational, fraction, exp, asin, pi, sin, Mod
import numpy as np
from math import ceil, floor
import sys


class GroverSearch:
    def __init__(self, N, M):
        # N: the size of the unstructured database
        # M: the size of target data
        # required: M < N/2
        self.N = N
        self.M = M
        self.goalRation = Rational(M, N)
        self.iterAngle = 2 * asin(sqrt(self.goalRation))
        self.ini_angle = Rational(1,2) * self.iterAngle
        self.error = None

        self.succProb_AQ = None
        self.succProb_MG = None
        self.potential_AQ = None
        self.potential_MG = None
        self.iter_AQ = 0

        print("########################  Grover Search with goal ratial", M,"/",N, " ########################")

        self.rationalRatio = [Rational(3,4), Rational(1,2), Rational(1,4)]
        try:
            if Rational(M,N) in self.rationalRatio:
                raise ValueError("the ratio of goal states leads to the finding the goals certainly")
        except ValueError as e:
            print(e)
            sys.exit(1)

        self.last_sector = None
        self.cur_sector = None

        self.last2_angle = None
        self.last_angle = None
        self.cur_angle = None

        self.total_iter_num = 0
        self.theory_iter = 0

    def setError(self, esp):
        # required: 0 <= esp <= 1
        try:
            if esp < 0 or esp > 1:
                raise ValueError("esp must be between 0 and 1")
        except ValueError as e:
            print(e)
            sys.exit(1)
        self.error = esp

    def addQubits(self):
        num_qubits = 0
        # catch the exception if the error is not given
        try:
            if self.error is None:
                raise ValueError("the error tolerance is not set yet!")
        except ValueError as e:
            print(e)
            exit(1)

        cur_angle = self.iterAngle
        iter_cnt = ceil((Rational(1, 2) * pi - Rational(1, 2) * cur_angle) / cur_angle)
        self.potential_AQ = (1 - sin(cur_angle / 2) ** 2)
        self.succProb_AQ = sin(cur_angle / 2 + (iter_cnt - 1) * cur_angle) ** 2 \
            if sin(cur_angle / 2 + (iter_cnt - 1) * cur_angle) ** 2 >= sin(cur_angle / 2 + iter_cnt * cur_angle) ** 2 \
            else sin(cur_angle / 2 + iter_cnt * cur_angle) ** 2
        self.iter_AQ = iter_cnt
        # while 1 - sin(cur_angle/2)**2 <= (1 - self.error):

        while self.succProb_AQ <= (1 - self.error):
            num_qubits += 1
            cur_angle = 2 * asin(sqrt(self.M / (self.N * (2 ** num_qubits))))
            iter_cnt = ceil((Rational(1,2)*pi - Rational(1,2)*cur_angle) / cur_angle)
            self.potential_AQ = (1 - sin(cur_angle / 2) ** 2)
            self.succProb_AQ = sin(cur_angle / 2 + (iter_cnt - 1) * cur_angle)**2 \
                if sin(cur_angle / 2 + (iter_cnt - 1) * cur_angle)**2 >= sin(cur_angle / 2 + iter_cnt * cur_angle)**2 \
                else sin(cur_angle / 2 + iter_cnt * cur_angle)**2
            self.iter_AQ = iter_cnt
        print("added qubits:\t", num_qubits)




    def moreGrover(self):
        # catch the exception if the error is not given
        try:
            if self.error is None:
                raise ValueError("the error tolerance is not set yet!")
        except ValueError as e:
            print(e)
            exit(1)

        # basic step of refinement
        T0 = floor((Rational(1, 2) * pi - Rational(1, 2) * self.iterAngle) / self.iterAngle)
        cur_s = 1

        self.cur_angle = self.iterAngle
        self.cur_sector = (self.ini_angle + T0 * self.cur_angle, self.ini_angle + (T0 + 1) * self.cur_angle)

        self.total_iter_num += T0
        self.theory_iter += T0
        print("================ basic step of refinement ================")
        print("current_angle:\t", (self.cur_angle*180/pi).evalf(), "\t",
              "current_sector:\t", ((self.cur_sector[0]*180/pi).evalf(),(self.cur_sector[1]*180/pi).evalf()))
        print("iterations to achieve the current sector:\t", self.total_iter_num + 1)
        succ_prob = sin(self.cur_sector[0])**2 \
                    if sin(self.cur_sector[0])**2 >= sin(self.cur_sector[1])**2 \
                    else sin(self.cur_sector[1])**2
        print("potential:\t", (1 - sin(self.cur_angle/2)**2).evalf(),"\t", "success probability:\t", succ_prob.evalf())

        if succ_prob >= (1 - self.error):
            self.total_iter_num += 1
            self.theory_iter += 1
        else:
            # the first round of refinement
            self.last_angle = self.cur_angle
            self.last_sector = self.cur_sector
            last_s = cur_s
            last_reverse = False

            self.cur_angle = ceil(pi / self.iterAngle) * self.iterAngle - pi
            if self.cur_angle >= self.last_angle / 2:
                cur_reverse = True
                self.cur_angle = self.last_angle - self.cur_angle

                self.total_iter_num += 1
                cur_s = ceil(pi / self.iterAngle) - 1

                addition_t = 1
                self.cur_sector = (self.last_sector[1], self.last_sector[1])
                while self.cur_sector[0] > pi / 2 or self.cur_sector[1] < pi / 2:
                    addition_t += 1
                    self.cur_sector = (
                    Mod(self.cur_sector[0] + cur_s * self.iterAngle, pi), Mod(self.cur_sector[0], pi))
                self.total_iter_num += (addition_t - 2) * cur_s
            else:
                cur_reverse = False
                cur_s = ceil(pi / self.iterAngle)

                addition_t = 1
                self.cur_sector = (self.last_sector[0], self.last_sector[0])
                while self.cur_sector[0] > pi / 2 or self.cur_sector[1] < pi / 2:
                    addition_t += 1
                    self.cur_sector = (
                    Mod(self.cur_sector[1], pi), Mod(self.cur_sector[1] + cur_s * self.iterAngle, pi))
                self.total_iter_num += (addition_t - 2) * cur_s

            print("================ first round of refinement ================")
            print("current_angle:\t", (self.cur_angle * 180 / pi).evalf(),
                  "current_sector:\t",
                  ((self.cur_sector[0] * 180 / pi).evalf(), (self.cur_sector[1] * 180 / pi).evalf()))
            print("iterations to achieve the current sector:\t", self.total_iter_num + cur_s)

            self.theory_iter += floor(self.last_angle / self.cur_angle) * ceil(pi / self.iterAngle)


            theo_last2_s = 0
            theo_last_s = 1
            theo_s = ceil(pi / self.iterAngle)
            print("theoretical iteration times:\t", self.theory_iter + theo_s)

            print("cur_s:\t", cur_s, "theoretical_s:\t", theo_s)

            cnt = 2

            succ_prob = sin(self.cur_sector[0]) ** 2 \
                if sin(self.cur_sector[0]) ** 2 >= sin(self.cur_sector[1]) ** 2 \
                else sin(self.cur_sector[1]) ** 2

            print("potential:\t", (1 - sin(self.cur_angle / 2) ** 2).evalf(), "\t", "success probability:\t",
                  succ_prob.evalf())

            # inductive rounds of refinement
            # while 1 - sin(self.cur_angle/2)**2 <= (1 - self.error):
            while succ_prob <= (1 - self.error):
                print('===========================', cnt, '-th refinement===========================')
                cnt += 1
                last2_reverse = last_reverse
                last_reverse = cur_reverse
                cur_reverse = False

                # reassign angles
                self.last2_angle = self.last_angle
                self.last_angle = self.cur_angle
                self.cur_angle = ceil(self.last2_angle / self.last_angle) * self.last_angle - self.last2_angle

                # judge whether the rotation is anti-clockwise or clockwise
                if last_reverse:
                    if self.cur_angle >= self.last_angle / 2:
                        self.cur_angle = self.last_angle - self.cur_angle
                    else:
                        cur_reverse = True
                else:
                    if self.cur_angle >= self.last_angle / 2:
                        cur_reverse = True
                        self.cur_angle = self.last_angle - self.cur_angle

                print("last_angle:\t", (self.last_angle * 180 / pi).evalf(), "current_angle:\t",
                      (self.cur_angle * 180 / pi).evalf())

                # calculate the theoretical bound of iterations
                # theo_last2_s = theo_last_s
                theo_last_s = theo_s
                # theo_s = ceil(self.last2_angle / self.last_angle) * theo_last_s - theo_last2_s
                theo_s = ceil(self.last2_angle / self.last_angle) * theo_last_s
                self.theory_iter += floor(self.last_angle / self.cur_angle) * theo_s

                print("theoretical_times:\t", floor(self.last_angle / self.cur_angle))

                # reassign the value of s , s_{i+1} = ceil( theta_{i-1} / theta_{i} ) * s_{i} - s_{i-1}
                last2_s = last_s
                last_s = cur_s
                # the current s_{i+1} depends on the... last rotation's and the last two rotation's direction
                cur_s = ceil(self.last2_angle / self.last_angle) * last_s - last2_s \
                    if last_reverse == last2_reverse \
                    else ceil(self.last2_angle / self.last_angle) * last_s + last2_s

                # reassign the sectors
                self.last_sector = self.cur_sector

                addition_t = 1

                if cur_reverse:
                    if last_reverse == False:
                        cur_s -= last_s
                        self.total_iter_num += last_s

                    self.cur_sector = (self.last_sector[1], self.last_sector[1])
                    print("last sector:\t",
                          ((self.last_sector[0] * 180 / pi).evalf(), (self.last_sector[1] * 180 / pi).evalf()))

                    while self.cur_sector[0] > pi / 2 or self.cur_sector[1] < pi / 2:
                        aux_degree = self.last_sector[1] - addition_t * self.cur_angle
                        self.cur_sector = (
                        Mod(self.cur_sector[0] + cur_s * self.iterAngle, pi), Mod(self.cur_sector[0], pi))
                        print("current sector after refinement:\t",
                              ((self.cur_sector[0] * 180 / pi).evalf(), (self.cur_sector[1] * 180 / pi).evalf()))
                        addition_t += 1
                    self.total_iter_num += (addition_t - 2) * cur_s
                    print("practical_times:\t", addition_t - 2)
                else:
                    if last_reverse == True:
                        cur_s -= last_s
                        self.total_iter_num += last_s

                    self.cur_sector = (self.last_sector[0], self.last_sector[0])
                    print("last sector:\t",
                          ((self.last_sector[0] * 180 / pi).evalf(), (self.last_sector[1] * 180 / pi).evalf()))

                    while self.cur_sector[0] > pi / 2 or self.cur_sector[1] < pi / 2:
                        aux_degree = self.cur_sector[0] + addition_t * self.cur_angle
                        self.cur_sector = (
                        Mod(self.cur_sector[1], pi), Mod(self.cur_sector[1] + cur_s * self.iterAngle, pi))
                        print("current sector after refinement:\t",
                              ((self.cur_sector[0] * 180 / pi).evalf(), (self.cur_sector[1] * 180 / pi).evalf()))
                        addition_t += 1
                    self.total_iter_num += (addition_t - 2) * cur_s
                    print("practical_times:\t", addition_t - 2)
                succ_prob = sin(self.cur_sector[0]) ** 2 \
                    if sin(self.cur_sector[0]) ** 2 >= sin(self.cur_sector[1]) ** 2 \
                    else sin(self.cur_sector[1]) ** 2
                print("potential probability:\t", (1 - sin(self.cur_angle / 2) ** 2).evalf(), "success probability:\t",
                      succ_prob.evalf())
                print("theoretical s:\t", theo_s)
                print("current s:\t", cur_s)

            self.total_iter_num += cur_s
            self.theory_iter += theo_s



        self.succProb_MG = sin(self.cur_sector[0]) ** 2 \
            if sin(self.cur_sector[0]) ** 2 >= sin(self.cur_sector[1]) ** 2 \
            else sin(self.cur_sector[1]) ** 2
        self.potential_MG = 1 - sin(self.cur_angle / 2) ** 2






